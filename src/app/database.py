# from sqlalchemy import Column, Integer, String, create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "sqlite:///./test.db"

# Base = declarative_base()
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)

# Base.metadata.create_all(bind=engine)


# def get_db():
#     print("Ouverture d'une session de base de données")  # Debug
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         print("Fermeture de la session de base de données")  # Debug
#         db.close()

