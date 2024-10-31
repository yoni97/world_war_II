from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base


#todo: can be converted to env variable via os.environ.get('DB_URL')
connection_url = 'postgresql://admin:1234@localhost:5437/missions_db'
engine = create_engine(connection_url, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()

def test_connection():
    try:
        with sessionmaker() as session:
            session.execute(text('SELECT 1'))
            print('\n\n----------- Connection successful !')
    except Exception as e:
        print('\n\n----------- Connection failed ! ERROR : ', e)
