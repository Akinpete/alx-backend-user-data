#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import bcrypt

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password) -> User:
        """
        add user instance to db
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        try:
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            print(f"Error adding user: {e}")
            return None
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user by arbitrary keyword arguments.

        Raises:
            NoResultFound: If no user is found matching the criteria.
            InvalidRequestError: If an invalid query argument is passed.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found with the provided arguments.")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query argument(s) provided.")
        return user

    def update_user(self, user_id, **kwargs) -> None:
        """
        Updates a user by user_id &
        arbitrary keyword arguments.
        """
        finder = {"id": user_id}
        user = self.find_user_by(**finder)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError(f"{key} is not a valid attribute of User")
            try:
                self._session.commit()
            except Exception as e:
                self._session.rollback()
                print(f"Error adding user: {e}")
        return None
