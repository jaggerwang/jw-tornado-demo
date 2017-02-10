from datetime import datetime

from pymongo import MongoClient
from pymongo.collection import Collection
from bson import ObjectId

from pyserver.config.db import MONGODB
from .error import Error

_mongo_databases = {}

_mysql_connections = {}


def get_mongo_database(alias):
    if alias not in _mongo_databases:
        params = MONGODB[alias]
        name = params.pop('name')
        auth = params.pop('auth', None)
        _mongo_databases[alias] = MongoClient(**params)[name]
        if auth:
            _mongo_databases[alias].authenticate(**auth)
    return _mongo_databases[alias]


class PyserverMongoModel(Collection):
    _fields = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self._fields:
            self._fields.update({
                '_id': (ObjectId, False),
                'create_time': (datetime, False),
                'update_time': (datetime, False),
            })

    def create(self, doc_or_docs):
        '''插入文档
        相比于MongoDB原生的insert，增加了none值字段过滤和模型字段验证。

        :Parameters:
          - `doc_or_docs`: ``dict`` or ``list``，单个文档或文档列表

        :Returns:
          - 同原生insert接口
        '''
        if isinstance(doc_or_docs, dict):
            self._filter_none_value(doc_or_docs)
            self._validate(doc_or_docs)
            if 'create_time' not in doc_or_docs:
                doc_or_docs['create_time'] = datetime.now()
            doc_or_docs['update_time'] = doc_or_docs['create_time']
            ret = super().insert_one(doc_or_docs)
            return ret.inserted_id
        elif isinstance(doc_or_docs, list):
            for v in doc_or_docs:
                self._filter_none_value(v)
                self._validate(v)
                if 'create_time' not in v:
                    v['create_time'] = datetime.now()
                v['update_time'] = v['create_time']
            ret = super().insert_many(doc_or_docs)
            return ret.inserted_ids

    def modify(self, spec, document, multi=False, upsert=False, validate=True,
               sort=None, return_document=None):
        '''部分更新文档
        只更新置顶字段的值，如果值为空字符串则表示删除该字段，未指定的字段值保持不变

        :Parameters:
          - `spec`: ``dict``，更新条件
          - `document`: ``dict``，要更新的字段和值，如果字段值为''，则删除该字段，
          字段值为None或不在document里的字段保持不变
          - `multi`: ``bool``，更新所有匹配文档还是仅第一个
          - `upsert`: ``bool``，没有匹配文档时是否插入
          - `validate`: ``bool``，是否验证文档合法性
          - `sort`: ``list``，multi为False，更新按此顺序匹配的第一个
          - `return_document`: ``ReturnDocument``，multi为False时，是否返回更新前或更新后的文档

        :Returns:
          - 更新的文档个数
        '''
        self._filter_none_value(document)
        set_fields = {k: v for k, v in document.items() if v != ''}
        unset_fields = {k: v for k, v in document.items() if v == ''}
        if validate:
            self._validate(set_fields, False)

        doc = {}
        if set_fields:
            doc['$set'] = set_fields
        if unset_fields:
            doc['$unset'] = unset_fields
        if not doc:
            return 0
        if '$set' in doc:
            doc['$set']['update_time'] = datetime.now()
        else:
            doc['$set'] = {'update_time': datetime.now()}
        if multi:
            ret = super().update_many(spec, doc, upsert=upsert)
            return ret.modified_count
        else:
            if return_document is None:
                ret = super().update_one(spec, doc, upsert=upsert)
                return ret.modified_count
            else:
                return super().find_one_and_update(
                    spec, doc, sort=sort, return_document=return_document)

    def find_by_ids(self, ids, keep_order=True):
        if not ids:
            return []

        docs = list(self.find({'_id': {'$in': ids}}))

        if keep_order:
            d = {v['_id']: v for v in docs}
            docs = [d.get(v) for v in ids]

        return docs

    @staticmethod
    def _filter_none_value(doc):
        if not isinstance(doc, dict):
            raise Error(message='doc should be a dict')

        for k, v in list(doc.items()):
            if v is None:
                del doc[k]

        return doc

    @classmethod
    def _validate(cls, doc, required=True):
        if cls._fields is None:
            return

        for k, v in doc.items():
            if '.' in k:
                continue

            if k not in cls._fields:
                raise Error(message='unexpected field {}'.format(k))

            type_, _ = cls._fields[k]
            if type_ is not None and not isinstance(v, type_):
                raise Error(
                    message='field {} should be a {}'.format(k, type_)
                )

        if required:
            fields = [k for k, v in cls._fields.items() if v[1]]
            for v in fields:
                if v not in doc:
                    raise Error(message='field {} is required'.format(v))
