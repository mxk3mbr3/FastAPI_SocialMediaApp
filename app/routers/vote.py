from fastapi import HTTPException, APIRouter, Depends
from .. import schemas, database, oauth2
from psycopg2.extras import RealDictCursor

# Users should be able to like and delete a liked post
# Should only be able to like a post once
# Retrieving posts should also fetch the total number of likes 

router = APIRouter(prefix="/votes", tags = ['Votes'])

# Getting global variables con and cur
con = database.setup_connection()
cur = con.cursor(cursor_factory=RealDictCursor)

# Setting up vote endpoint

@router.post("/", status_code=201)
def vote(vote:schemas.Vote, current_user=Depends(oauth2.get_current_user)):

    # Tackles the issue of liking/ unliking a post that does not exist
    cur.execute("SELECT id FROM posts WHERE id = %s",(vote.post_id,))
    post = cur.fetchone()

    if post is None:
        raise HTTPException(status_code=404, detail = f"Post does not exist")

    cur.execute("SELECT * FROM votes WHERE post_id = %s AND user_id = %s",(vote.post_id,current_user['id']))
    vote_query = cur.fetchone()

    # To like a post
    if vote.dir == 1:
        if vote_query: # if True it is already in votes db so we raise an error
            raise HTTPException(status_code=409, detail = f"user {current_user['id']} has already voted on post {vote.post_id}")
        # else
        cur.execute("INSERT INTO votes(post_id,user_id) VALUES (%s,%s) RETURNING *;",(vote.post_id,current_user['id']))
        con.commit()

        return {"message":"successfully added vote"}

    # To delete a like from a post
    if vote.dir == 0:
        if vote_query is None: # if False it is not in votes db (i.e. post was never liked) so an error is raised 
            raise HTTPException(status_code=404, detail = f"Vote does not exist")
        # else 
        cur.execute("DELETE FROM votes WHERE post_id = %s AND user_id = %s",(vote.post_id,current_user['id']))
        con.commit()

        return {"message":"successfully deleted vote"}
    
