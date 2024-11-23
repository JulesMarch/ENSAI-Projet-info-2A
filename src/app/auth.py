from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from database import User, SessionLocal
from sqlalchemy.orm import Session
from routes import get_db

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def get_current_user(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token invalide")
        
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Utilisateur non trouvé")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")


