#!/usr/bin/python3
"""Mysql Database Storage Engine Module"""
from os import getenv
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.state import State
from models.place import Place
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.user import User
from models.base_model import Base


class DBStorage:
    """DBStorage Class"""
    __engine = None
    __session = None

    def __init__(self):

        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV ')

        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'
                .format(
                    HBNB_MYSQL_USER, HBNB_MYSQL_PWD,
                    HBNB_MYSQL_HOST, HBNB_MYSQL_DB),
                pool_pre_ping=True)

        if HBNB_ENV == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        clsObj = {}
        classes = [State, User, City, Amenity, Place, Review]
        if cls is None:
            for clss in classes:
                for obj in self.__session.query(clss).all():
                    if '_sa_instance_state' in obj.__dict__:
                        del obj.__dict__['_sa_instance_state']
                    clsObj[obj.__class__.__name__ + '.' + obj.id] = obj

            return clsObj
        else:
            if cls in classes:
                for obj in self.__session.query(cls).all():
                    if '_sa_instance_state' in obj.__dict__:
                        del obj.__dict__['_sa_instance_state']
                    clsObj[obj.__class__.__name__ + '.' + obj.id] = obj
                return clsObj
            else:
                return {}

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)
        self.__session.flush()

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.session.delete(obj)
            self.save()

    def reload(self):
        """
        create all tables in the database and
        current database session
        """
        Base.metadata.create_all(self.__engine)

        Session_fac = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(Session_fac)
        self.__session = Session()

    def close(self):
        """
        a public method
        """
        self.__session.close()
