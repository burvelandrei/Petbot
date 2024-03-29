from sqlalchemy import create_engine


def engine():
    engine = create_engine(f"mysql+pymysql://andre:bonaqua3064@127.0.0.1:3306/Petbot", echo=True, pool_recycle=2000)
    return engine


if __name__ == '__main__':
    print(engine())