from sqlalchemy.ext.declarative import as_declarative, declared_attr, DeclarativeMeta
from sqlalchemy.orm import declarative_base
from abc import ABCMeta

# Combine DeclarativeMeta and ABCMeta into a single metaclass
class DeclarativeABCMeta(DeclarativeMeta, ABCMeta):
    pass

@as_declarative(metaclass=DeclarativeABCMeta)
class Base:
    injectable = {}  # Dictionary to map table names to classes

    @declared_attr
    def __tablename__(cls):
        """Generate table names automatically if not explicitly set."""
        return cls.__name__.lower()

    def __init_subclass__(cls, **kwargs):
        """Automatically register subclasses."""
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "process"):
            name = f"{cls.__tableschema__}.{cls.__tablename__}"
            Base.injectable[name] = cls
