import aiomysql


class DatabaseConnection:
    def __init__(self, db_host, db_user, db_password, db_name):
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.connection = None  # can be hidden

    async def create_connection(self):
        try:
            self.connection = await aiomysql.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                db=self.db_name
            )
            return self.connection
        except aiomysql.Error as e:
            print(e)
            raise e

    async def close_connection(self):
        if self.connection:
            await self.connection.close()
