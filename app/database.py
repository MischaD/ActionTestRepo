from rethinkdb import RethinkDB


class RDB:
    def __init__(self):

        self.dbname = "DB"
        self.r = RethinkDB()
        self.connection = self.r.connect(
            "127.0.0.1", "28015"
        ).repl()
        self.connection.use(self.dbname)

        self._init_db()

    def _init_db(self):
        if not self.dbname in self.r.db_list().run(self.connection):
            self.r.db_create(self.dbname).run(self.connection)

        tables = self.r.table_list().run(self.connection)
        if "meta" not in tables:
            # table with meta data independant of each blockchain
            self.r.table_create("meta", primary_key="key").run(self.connection)
        if "accounts" not in tables:
            # address table
            self.r.table_create("accounts", primary_key="account_id").run(self.connection)
        if "pseudo_ids" not in tables:
            # table for pseudo_ids for mapping back-end wallets to front-end user
            self.r.table_create("pseudo_ids").run(self.connection)
        if "transactions" not in tables:
            # transaction table
            self.r.table_create("transactions", primary_key="operation_id").run(self.connection)
