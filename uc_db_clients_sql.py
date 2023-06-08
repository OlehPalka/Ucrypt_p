import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import *



log = logging.getLogger(__name__)


def get_database():
    """
    Connects to database.
    Returns:
        engine
    """
    try:
        engine = get_engine_from_settings()
        log.info("Connected to PostgreSQL database!")
    except IOError:
        log.exception("Failed to get database connection!")
        return None, 'fail'

    return engine


def get_engine_from_settings():
    """
    Sets up database connection from local settings.
    Input:
        Dictionary containing pghost, pguser, pgpassword, pgdatabase and pgport.
    Returns:
        Call to get_database returning engine
    """
    keys = ['pguser', 'pgpasswd', 'pghost', 'pgport', 'pgdb']
    if not all(key in keys for key in settings.keys()):
        raise Exception('Bad config file')

    return get_engine(settings['pguser'],
                      settings['pgpasswd'],
                      settings['pghost'],
                      settings['pgport'],
                      settings['pgdb'])


def get_engine(user, passwd, host, port, db):
    """
    Get SQLalchemy engine using credentials.
    Input:
        db: database name
        user: Username
        host: Hostname of the database server
        port: Port number
        passwd: Password for the database
    Returns:
        Database engine
    """

    url = 'postgresql://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=user, passwd=passwd, host=host, port=port, db=db)
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return engine


def get_session():
    """
    Return an SQLAlchemy session
    Input:
        engine: an SQLAlchemy engine
    """
    engine = get_database()
    session = sessionmaker(bind=engine)()
    #session = Session()
    return session


db = get_database()
session = get_session()
Base = declarative_base()


class Clients(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(200), nullable=False)
    password = Column(String, nullable=False)
    pin = Column(Integer, nullable=False)
    image = Column(String(500), nullable=False)
    name = Column(String(200), nullable=False)


def create():
    Base.metadata.create_all(db)


create()


def add_client(email, password, pin):
    client = Clients(email=email, password=password,
                     pin=pin, image='-', name='-')
    session.add(client)
    session.commit()


def change_image(id, image):
    user = session.query(Clients).filter(Clients.id == id).first()
    user.image = image
    session.commit()


def change_name(id, name):
    user = session.query(Clients).filter(Clients.id == id).first()
    user.name = name
    session.commit()


def find_user_by_email(email):
    user_data = session.query(Clients).filter(Clients.email == email).first()
    return [user_data.id, user_data.email, user_data.password, user_data.pin, user_data.name, user_data.image]


def find_user_by_id(id):
    user_data = session.query(Clients).filter(Clients.id == id).first()
    return [user_data.id, user_data.email, user_data.password, user_data.pin, user_data.name, user_data.image]


def update_user_email(actualemail, email_to_change):
    user = session.query(Clients).filter(Clients.email == actualemail).first()
    user.email = email_to_change
    session.commit()


def update_user_id(actual_id, new_id):
    user = session.query(Clients).filter(Clients.id == actual_id).first()
    user.email = new_id
    session.commit()


def update_user_password(email, new_password):
    user = session.query(Clients).filter(Clients.email == email).first()
    user.password = new_password
    session.commit()


def delete_user(email):
    user = session.query(Clients).filter(Clients.email == email).first()
    session.delete(user)
    session.commit()
