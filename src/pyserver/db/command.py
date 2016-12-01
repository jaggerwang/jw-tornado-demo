from cement.core import controller

from pyserver.common.const import *
from pyserver.common.command import PyserverController

from .service import *


class CreateMongoDBIndexController(PyserverController):

    class Meta:
        label = "create_mongodb_index"
        stacked_on = "base"
        stacked_type = "nested"
        description = "Create mongodb index."
        arguments = [
            (["-d", "--db_alias"], dict(
                help="database connection alias")),
            (["-c", "--coll"], dict(
                help="collection name")),
            (["-b", "--background"], dict(
                action='store_true',
                help="run in background.")),
            (["--drop_indexes"], dict(
                action="store_true",
                help="drop collection indexes before creation")),
            (["--drop_dups"], dict(
                action='store_true',
                help="drop duplicate docs")),
        ]

    @controller.expose()
    def default(self):
        create_mongodb_index(
            self.app.pargs.db_alias, self.app.pargs.coll,
            self.app.pargs.drop_indexes, self.app.pargs.background,
            self.app.pargs.drop_dups)
