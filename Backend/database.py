from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
DATABASE_URL="mysql+pymysql://root:12345@localhost:3306/jobportal"
engine=create_engine(DATABASE_URL)
sessionLocal=sessionmaker(bind=engine)
Base=declarative_base()
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
