from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm


import schemas,database,models,hashing
from . import JWTtokens

get_db=database.get_db

router=APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(),db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"your username {request.username} is invalid")
    if hashing.Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"your password is invalid")
    
    access_token = JWTtokens.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}