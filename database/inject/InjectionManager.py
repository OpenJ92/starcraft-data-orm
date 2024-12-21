from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from collections import defaultdict, deque

from database.inject.Injectable import Injectable

class InjectionManager():
    def __init__(self, base):
        """
        Initialize the InjectionManager.
        :param metadata: SQLAlchemy metadata (Base.metadata).
        """
        self.base = base
        self.metadata = base.metadata
        ## self.sorted_relations = self._topological_sort()


    async def inject(self, replay, session):
        """
        Perform the injection process for a replay.
        :param replay: Parsed replay object to inject.
        :param session: Database session supporting flush, commit and rollback:
        """
        try:
            for relation in self.metadata.sorted_tables:
                name = f"{relation.schema}.{relation.name}"
                relation_cls = self.base.injectable.get(name)
                if relation_cls and issubclass(relation_cls, Injectable):
                    await relation_cls.process(replay, session)
                    await session.flush()  # Flush after each relation
            await session.commit()  # Commit transaction after all relations
        except SQLAlchemyError as e:
            breakpoint()
            await session.rollback()  # Rollback transaction on error
            raise e  # Optionally re-raise or log the error


## ## Consider Supplying a "Base" at each level of the database via __init__.py file
## class InjectionManagerFactory():
##     def __init__(self):
##         pass
## 
##     @classmethod
##     def WAREHOUSE(cls):
##         return InjectionManager(WareshouseBase)
## 
##     @classmethod
##     def ANALYTICS(cls):
##         return InjectionManager(AnalyticsBase)
## 
##     @classmethod
##     def MACHINE_LEARNING(cls):
##         return InjectionManager(MachineLearningBase)
