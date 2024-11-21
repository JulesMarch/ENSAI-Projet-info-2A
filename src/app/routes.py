from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import User, SessionLocal
from .models import UserCreate, UserLogin
from .utils import hash_password, verify_password
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .database import get_db
from ..dao.zonage_dao import ZonageDao



router = APIRouter()

# Créer un compte utilisateur
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")
    
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Utilisateur créé avec succès"}

# Connexion et génération de JWT
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    
    # Générer un token JWT
    access_token = jwt.encode(
        {"sub": db_user.username, "exp": datetime.utcnow() + timedelta(hours=1)},
        "your_secret_key",
        algorithm="HS256"
    )
    return {"access_token": access_token, "token_type": "bearer"}
