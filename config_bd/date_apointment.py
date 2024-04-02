from sqlalchemy import insert, select, update, MetaData, Table, delete
import config_bd.BaseModel as e


class SQL_D_A:
    def __init__(self):
        self.engine = e.engine()
        metadata = MetaData()
        self.users = Table(
            "date_appointment", metadata, autoload_replace=True, autoload_with=self.engine
        )

    def INSERT(
        self,
        telegram_id: str,
        date: str
    ):
        conn = self.engine.connect()
        try:
            s = insert(self.users).values(
                telegram_id=telegram_id,
                date=date
            )
            conn.execute(s)
            conn.commit()
            conn.close()
            self.engine.dispose()
        except Exception as e:
            conn.rollback()
            conn.close()
            self.engine.dispose()
            print(str(e))

    def SELECT_apointment(self, telegram_id: str) -> list:
        conn = self.engine.connect()
        try:
            s = select(self.users).where(self.users.c.telegram_id == telegram_id)
            re = conn.execute(s)
            result = re.fetchall()
            conn.commit()
            conn.close()
            self.engine.dispose()
            return result
        except Exception as e:
            conn.rollback()
            conn.close()
            self.engine.dispose()
            print(str(e))