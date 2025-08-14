from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas,oauth2
# The 'oauth2' import is no longer needed
# from .. import oauth2 
from ..database import get_db
from typing import List,Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)

# 1. Getting all posts
@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip) .all()
    # print(results)
    return [
    {"post": post, "votes": votes} 
    for post, votes in results
]

# 2. Creating a post (Authentication Removed)
@router.post("/", status_code=201, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id,**post.dict())  # set owner_id here
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# 3. Getting an individual post
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # test_post = db.query(models.Post).filter(models.Post.id == id).first()
    test_post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    post,vote=test_post
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=403,detail="Not Authorized to Perform requested action")
    return {"post": post, "votes": vote} 

# 4. Deleting a post
@router.delete("/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if post is None:
        raise HTTPException(status_code=404, detail=f"post with id:{id} does not exist")
    
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=403,detail="Not Authorized to Perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)

# 5. Updating a post
@router.put("/{id}", response_model=schemas.Post)
def update_posts(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=404, detail=f"post with id:{id} does not exist")
    
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=403,detail="Not Authorized to Perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    db.refresh(post)
    return post