from sqlalchemy import create_engine, text
from core.config import DATABASE_URL
from sqlalchemy.orm import sessionmaker,declarative_base
DATABASE_URL=DATABASE_URL
engine=create_engine(DATABASE_URL,connect_args={"ssl":{"ca":"core/ca.pem"}})
try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("Database connection successful.")
except Exception as e:
    print(f"Database connection failed: {e}")
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
