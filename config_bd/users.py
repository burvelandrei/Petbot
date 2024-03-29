from sqlalchemy import insert, select, update, MetaData, Table, delete
import config_bd.BaseModel as e


class SQL:
    def __init__(self):
        self.engine = e.engine()
        metadata = MetaData()
        self.users = Table("users", metadata, autoload_replace=True, autoload_with=self.engine)

    def SELECT_USER(self, telegram_id: str) -> list:
        conn = self.engine.connect()
        try:
            s = select(self.users).where(self.users.c.telegram_id == telegram_id)
            re = conn.execute(s)
            result = re.fetchall()
            conn.commit()
            conn.close()
            self.engine.dispose()
            return result[0]
        except Exception as e:
            conn.rollback()
            conn.close()
            self.engine.dispose()
            print(str(e))
