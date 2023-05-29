from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import schemas

app = FastAPI()
@app.get('/')
def index():
    return 'hello world'

@app.post('/post')
def create(request:schemas.Blog):
    return request

@app.get('/blog')
def show(limit : int = 10,published : bool = True, sort: Optional[str] = None):      #default values are 10 and true
    if published:
        return{'data':f'showing {limit} published blogs from the database'}
    else:
        return{'data':f'showing {limit} unpublished blogs from the database'}

class Blog(BaseModel):
    title:str
    body:str
    published_at:Optional[bool]

@app.post('/blog')
def create_blog(blog:"Blog"):
    return {'data':f"Blog is creates with title {blog.title}"}

@app.get('/blog/{id}')
def show(id: int):
    return{'data':id}

@app.get('/blog/{id}/comments')
def comment(id):
    return{'data':{'test1','test2'}}