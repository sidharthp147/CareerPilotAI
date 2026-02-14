from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker,declarative_base
DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)
sessionLocal=sessionmaker(bind=engine)
Base=declarative_base()
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
