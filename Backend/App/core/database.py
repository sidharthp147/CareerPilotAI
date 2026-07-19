from sqlalchemy import create_engine,text
from core.config import DATABASE_URL
from sqlalchemy.orm import sessionmaker,declarative_base
import time

DATABASE_URL=DATABASE_URL
MAX_RETRIES=5
RETRY_DELAY=20
for attempt in range(MAX_RETRIES):
    try:
        engine=create_engine(DATABASE_URL,connect_args={"ssl":{"ca":"core/ca.pem"}})
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            break
    except Exception:
        if attempt==MAX_RETRIES-1:
            raise
        time.sleep(RETRY_DELAY)
sessionLocal=sessionmaker(bind=engine)
Base=declarative_base()
def get_db():
    db=sessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise 
    finally:
        db.close()
