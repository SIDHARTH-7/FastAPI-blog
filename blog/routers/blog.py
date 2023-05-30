from fastapi import APIRouter,Depends,status,HTTPException
from typing import List
from sqlalchemy.orm import Session

import schemas,models,database
from outh2 import get_current_user

get_db=database.get_db

router=APIRouter(
    prefix="/blog",
    tags=['blogs']
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog,db: Session = Depends(get_db),current_user: schemas.User=Depends(get_current_user)):
    new_blog = models.Blog(title=request.title,body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/',response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db),current_user: schemas.User=Depends(get_current_user)):
    blogs=db.query(models.Blog).all()
    return blogs

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.Blog)
def show(id,db: Session = Depends(get_db),current_user: schemas.User=Depends(get_current_user)):
    blog=db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"blog with ID {id} not found")
       #response.status_code=status.HTTP_404_NOT_FOUND
       #return{'detail':f"blog with ID {id} not found"}
    return blog

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete(id,db: Session = Depends(get_db),current_user: schemas.User=Depends(get_current_user)):   
    blog=db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"blog with ID {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request:schemas.Blog,db: Session = Depends(get_db),current_user: schemas.User=Depends(get_current_user)):
    blog=db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"blog with ID {id} not found")
    blog.update(request)
    db.commit()
    return request


