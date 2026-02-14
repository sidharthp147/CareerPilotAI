from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
DATABASE_URL="mysql://root:hxZjBNImsbxSRYZCGymKQMSRBzWmGEGh@metro.proxy.rlwy.net:34527/railway"
engine=create_engine(DATABASE_URL)
sessionLocal=sessionmaker(bind=engine)
Base=declarative_base()
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
