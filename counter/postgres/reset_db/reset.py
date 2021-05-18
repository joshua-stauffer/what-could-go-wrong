"""
This script runs first and (mostly) ensures that the counter in the database 
exists and starts each run at 0. As a sanity check, it prints the value reset
from, which can be used to confirm that this actually ran before any of the
incrementing apps started. In practice, this might not always be the first 
app up, but it's a good enough guarantee for demonstration purposes.
"""
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

engine = create_engine(
            DB_URI,
            echo=False,
            future=True)
Base.metadata.create_all(engine)

with Session(engine, future=True) as session:
            # read value
            res = session.execute(
                select(Counter).where(Counter.id == 1)
            ).scalar_one_or_none()
            if res:
                old_val = res.val
                res.val = 0
            else:
                old_val = None
                res = Counter(val=0)
            session.add(res)
            session.commit()
if old_val:
    print(f'Database reset from {old_val}')
else:
    print(f'Counter not found -- initialized a new counter row in the database')