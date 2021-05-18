import os
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

DB_URI = os.environ.get('DB_URI')

Base = declarative_base()

class Counter(Base):
    __tablename__ = 'counter'

    id = Column(Integer, primary_key=True)
    val = Column(Integer)

    def __repr__(self):
        return f"id: {self.id} val: {self.val}"

error_count = [0, 0, 0]
error_log = list()

def get_db_conn(error_count, error_log):
    while True:
        try:
            engine = create_engine(
                        DB_URI,
                        echo=False, # set this to True to see the SQL being emitted
                        future=True,
                        # isolation level determines how SQLite handles transactions
                        # options are SERIALIZABLE, READ UNCOMMITTED, AUTOCOMMIT
                        isolation_level="SERIALIZABLE") 
            Base.metadata.create_all(engine)
            return engine
        except Exception as e:
            error_count[0] += 1
            error_log.append(e)
            continue

def increment_counter(engine, error_count, error_log):
    while True:
        try:
            with Session(engine, future=True) as session:

                res = session.execute(
                    select(Counter).where(Counter.id == 1)
                ).scalar_one()

                res.val += 1
                session.add(res)
                session.commit()

                return # success, so break the loop
        except Exception as e:
            error_log.append(e)
            error_count[1] += 1

def get_results(engine, error_count, error_log):
    while True:
        try:
            with Session(engine, future=True) as session:
                    # read value
                    res = session.execute(
                        select(Counter).where(Counter.id == 1)
                    ).scalar_one_or_none()
                    return res.val
        except Exception as e:
            error_count[2] += 1
            error_log.append(e)

# connect
engine = get_db_conn(error_count, error_log)
# run transactions
[increment_counter(engine, error_count, error_log) for _ in range(100)]
# get results
final_count = get_results(engine, error_count, error_log)

print('*' * 79)
print(f'Final count is {final_count}')

print(f'error count: {error_count}')
print('*' * 79)
# for e in error_log:
#    print(e)
