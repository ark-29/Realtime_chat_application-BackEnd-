from sqlmodel import SQLModel, create_engine, Session

database_url = "mysql+pymysql://root:<password>@<hostname>/<dbname>"

Engine = create_engine(database_url, echo=True)

async def get_session():
    with Session(Engine) as session:
        yield session

async def create_db_tables():
    SQLModel.metadata.create_all(Engine)

