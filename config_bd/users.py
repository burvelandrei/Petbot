from sqlalchemy import insert, select, update, MetaData, Table, delete
import config_bd.BaseModel as e


class SQL:
    def __init__(self):
        self.engine = e.engine()
        metadata = MetaData()
        self.users = Table(
            "users", metadata, autoload_replace=True, autoload_with=self.engine
        )

    def INSERT(
        self,
        telegram_id: str,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
        phone_number: str = None,
    ):
        conn = self.engine.connect()
        try:
            s = insert(self.users).values(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
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

    def SELECT_ALL(self, telegram_id: str) -> list:
        conn = self.engine.connect()
        try:
            s = select(self.users)
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

    def UPGRADE_username(self, telegram_id: str, username: str):
        conn = self.engine.connect()
        try:
            s = update(self.users).where(self.users.c.telegram_id == telegram_id).values(username=username)
            conn.execute(s)
            conn.commit()
            conn.close()
            self.engine.dispose()
        except Exception as e:
            conn.rollback()
            conn.close()
            self.engine.dispose()
            print(str(e))

    def UPGRADE_firstname(self, telegram_id: str, first_name: str):
        conn = self.engine.connect()
        try:
            s = update(self.users).where(self.users.c.telegram_id == telegram_id).values(first_name=first_name)
            conn.execute(s)
            conn.commit()
            conn.close()
            self.engine.dispose()
        except Exception as e:
            conn.rollback()
            conn.close()
            self.engine.dispose()
            print(str(e))

    def UPGRADE_lastname(self, telegram_id: str, last_name: str):
        conn = self.engine.connect()
        try:
            s = update(self.users).where(self.users.c.telegram_id == telegram_id).values(last_name=last_name)
            conn.execute(s)
            conn.commit()
            conn.close()
            self.engine.dispose()
        except Exception as e:
            conn.rollback()
            conn.close()
            self.engine.dispose()
            print(str(e))

    def UPGRADE_phonenumber(self, telegram_id: str, phone_number: str):
        conn = self.engine.connect()
        try:
            s = update(self.users).where(self.users.c.telegram_id == telegram_id).values(phone_number=phone_number)
            conn.execute(s)
            conn.commit()
            conn.close()
            self.engine.dispose()
        except Exception as e:
            conn.rollback()
            conn.close()
            self.engine.dispose()
            print(str(e))