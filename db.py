from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import config

db = SQLAlchemy()
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)


class LocalSession:
    """
    A Session Manager to be used for db session
    """

    def __init__(self, session: sessionmaker, enable_foreign_key_support: bool = False) -> None:
        """
        Initializer of class

        Args:
            session (sessionmaker): session object
            enable_foreign_key_support (bool): bool value

        Returns:
            None
        """
        self.session = session()
        # setting it to False, to be able to use db query object records outside the context manager too
        self.session.expire_on_commit = False
        if enable_foreign_key_support:
            self.session.execute("PRAGMA foreign_keys=ON")

    def __enter__(self) -> Session:
        """
        Return session object

        Returns:
            Session: session object
        """
        return self.session

    def __exit__(self, exc_type: Exception, exc_val: str, exc_tb: str) -> None:
        """
        Exit the class

        Args:
            exc_type (Exception): Exception type
            exc_val (str): Exception value
            exc_tb (str): Exception traceback

        Returns:
            None
        """
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
            # expunge_all detaches the object from session thus the values are retained outside session scope
            self.session.expunge_all()
        self.session.close()
