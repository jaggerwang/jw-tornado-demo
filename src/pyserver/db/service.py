import re
import logging

from bson import ObjectId

from pyserver.common.model import get_mongo_database
from .mongodbindex import MONGODB_INDEXES


def create_mongodb_index(db_alias, coll=None, drop_indexes=False,
                         background=False, drop_dups=False):
    logger = logging.getLogger('app')
    indexes = MONGODB_INDEXES

    if db_alias is None and coll is not None:
        logger.error("db connection alias needed when specify coll")
        return False

    if db_alias is not None:
        indexes = {k: v for k, v in indexes.items() if k == db_alias}
        if coll is not None:
            indexes = {
                k: {k1: v1 for k1, v1 in v.items() if k1 == coll}
                for k, v in indexes.items()
            }

    for db_alias, colls in indexes.items():
        db = get_mongo_database(db_alias)
        logger.info("begin process db {} ...".format(db.name))

        for coll, coll_indexes in colls.items():
            coll = db[coll]
            logger.info(
                "  begin process collection {} ...".format(coll.name))

            if drop_indexes:
                logger.info("    begin drop indexes ...")
                coll.drop_indexes()
                logger.info("    end drop indexes")

            for index in coll_indexes:
                keys = index[0]
                index_options = index[1] if len(index) >= 2 else {}
                index_options.update({
                    'background': background
                })
                while True:
                    try:
                        index_name = coll.create_index(
                            keys, **index_options)
                    except Exception as e:
                        m = re.match(
                            r"exception: E11000 duplicate key error collection: .+ (.+) dup key: { (.+) }", str(e))
                        if m and drop_dups:
                            index_keys = m.group(1).rstrip('_1').rstrip(
                                '_-1').replace('_1_', ' ').replace(
                                '_-1_', ' ').split()
                            index_values = []
                            for v in m.group(2).split(', '):
                                v = v.lstrip(': ')
                                if v.startswith('ObjectId'):
                                    v = ObjectId(
                                        re.match(r"ObjectId\('(.+)'\)", v).group(1))
                                elif v.startswith('"'):
                                    v = v.strip('"')
                                elif re.match(r"\d+", v):
                                    v = int(v)
                                index_values.append(v)
                            query = {
                                k: v for k, v in zip(index_keys, index_values)}
                            logger.info(
                                "duplicate docs: {}".format(list(coll.find(query))))
                            coll.delete_many(query)
                            logger.info(
                                "droped duplicate doc: {}".format((query)))
                            continue
                        logger.error("create index failed: {}".format(e))
                        break
                    if index_name is not None:
                        logger.info(
                            "    created index {}".format(index_name))
                    else:
                        logger.info(
                            "    index {} already exists".format(keys))
                    break

            logger.info(
                "  end process collection {}".format(coll.name))

        logger.info("end process db {}".format(db.name))
