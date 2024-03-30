from sqlalchemy import create_engine
from config_data.config import load_config, Config


config:Config = load_config()


def engine():
    engine = create_engine(f"mysql+pymysql://{config.db.bd_login}:{config.db.bd_password}@{config.db.bd_host}:3306/{config.db.bd_name}", echo=True, pool_recycle=2000)
    return engine


if __name__ == '__main__':
    print(engine())