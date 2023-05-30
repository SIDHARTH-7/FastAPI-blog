from fastapi import APIRouter,Depends,status,Response,HTTPException
from typing import List
from sqlalchemy.orm import Session

import schemas,models,database,hashing

get_db=database.get_db

router=APIRouter(
    prefix="/user",
    tags=['users']
)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.ShowUser)
def create_user(request: schemas.User,db: Session = Depends(get_db)):
    new_user = models.User(name=request.name,
                           email=request.email,
                           password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ShowUser)
def show(id,response: Response,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"blog with ID {id} not found")
       #response.status_code=status.HTTP_404_NOT_FOUND
       #return{'detail':f"user with ID {id} not found"}
    return user
