from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

import schemas,database,models

get_db=database.get_db

router=APIRouter(
    tags=['Authentication']
)

@router.post('/login',response_model=schemas.ShowUser)
def login(request:schemas.Login,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"your username {request.username} is invalid")
    return user