from typing import Optional
from fastapi import HTTPException, APIRouter, Depends
from ..schemas import Post
from .. import database, oauth2, db_queries
from psycopg2.extras import RealDictCursor

router = APIRouter(prefix="/posts", tags = ['Posts'])

# Getting global variables con and cur
con = database.setup_connection()
cur = con.cursor(cursor_factory=RealDictCursor)

# Getting global variable/s for SQL query
likes_query = db_queries.likes_subquery()

# Setting up post endpoints 

# Note: current_user dependency ensures users to be logged in before they can create a post
# This is done by getting JWT token from UserLogin and using the token in the Authorization section
# of Postman. Set type to Bearer Token and past the token in the token field - Token can be replaced
# by a function, {{JWT}} in this case, so that you don't have to stay creating a new token each
# time it expires and copy and pasting it into the token field in Authorization.

# Get all (your) posts 
@router.get("/")
def get_your_posts(current_user = Depends(oauth2.get_current_user)):
    cur.execute(f"""SELECT sub.* FROM {likes_query} WHERE user_id = (%s)""",(current_user['id'],))
    posts = cur.fetchall()
    return posts

# Get all posts (of any user - even yours with filtering capability) 

# Here we define 3 Query Parameters (limit, skip & search)
# Query parameters are filters that help the user to specify a certain portion 
# Examples: UberEats: filter by restuarants in a particular city, Linkedin:jobs posted (created) in the last hour
# In this instance, we are going to set certain defaults, i.e.,:
# 1. Limit results to just the last 10 posts
# 2. Skip by default no posts
# 3. Search posts by title (optional)

# In postman the querying can be done as follows, for example get posts(any user)
# In this example user 2 --> {{URL}}posts/2?limit=3&skip=0&search=again
# ?: quetsion mark is needed as the 'start' of the query parameters
# You can then use as many query parameters as you want. To use together, use '&'

@router.get("/{id}")
def get_any_posts(id:int, current_user = Depends(oauth2.get_current_user), limit:int = 10, skip:int = 0, search:Optional[str] = ""):
    cur.execute(f"""SELECT sub.* FROM {likes_query} WHERE user_id = %s AND title ILIKE %s ORDER BY 
                    created_at DESC LIMIT %s OFFSET %s""",(id,f'%{search}%',limit,skip))
    posts_by_id = cur.fetchall()
    if posts_by_id == []:
        raise HTTPException(status_code=404, 
                            detail = f"User with id {id} does not exist")
    return posts_by_id

# Create a post
@router.post("/",status_code=201)
def create_posts(post:Post, current_user = Depends(oauth2.get_current_user)):
    cur.execute("INSERT INTO posts(title, content, published, user_id) VALUES (%s,%s,%s,%s) RETURNING *;", 
                (post.title,post.content,post.published,current_user['id']))
    new_post = cur.fetchone()
    # commit changes to database
    con.commit()
    return new_post

# Get a particular post by post id - To be used for updating and deleting posts
def get_post(id:int, current_user = Depends(oauth2.get_current_user)):
    cur.execute("SELECT * FROM posts WHERE id = %s",(id,))
    post_by_id = cur.fetchone()
    if post_by_id is None:
        raise HTTPException(status_code=404, 
                            detail = f"User with id {id} does not exist")
    return post_by_id

# Delete a post
@router.delete("/{id}", status_code=204)
def delete_post(id:int, current_user = Depends(oauth2.get_current_user)):

    cur.execute("DELETE FROM posts WHERE id = %s AND user_id = %s RETURNING *", (id,current_user['id']))
    deleted_post = cur.fetchone()
    con.commit()

    # The below is for when id does not exist or you are not the author (user) of the post id
    if deleted_post is None:
        raise HTTPException(status_code=404, 
                        detail = f"Post with id {id} does not exist or you don't have the authorization to perform requested action")

# Update a post
@router.put("/{id}")
def update_post(id:int, post:Post, current_user = Depends(oauth2.get_current_user)):

    cur.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s AND user_id = %s RETURNING *", 
                (post.title, post.content, post.published, (id,),current_user['id']))
    updated_post = cur.fetchone()
    con.commit()

    # The below is for when id does not exist or you are not the author (user) of the post id
    if updated_post is None:
        raise HTTPException(status_code=404, 
                            detail = f"Post with id {id} does not exist or you don't have the authorization to perform requested action")

    return {f'id {id} was updated'}