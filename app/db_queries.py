# This module is for bulky SQL queries/ subqueries so it does not clutter any other module 
 
# Below is the subquery for joining the votes and posts tables so you also get the number of total likes when seeing a post
def likes_subquery():
    likes_subquery = """(WITH cte_likes AS (
                                        SELECT 
                                            post_id,
                                            COUNT(post_id) AS post_likes
                                        FROM 
                                            public.votes
                                        GROUP BY
                                            post_id
                                        ) 
                                        SELECT 
                                            p.*,
                                            COALESCE(c.post_likes,0) AS post_likes 
                                        FROM
                                            public.posts p
                                        LEFT JOIN cte_likes c
                                        ON p.id = c.post_id) sub"""
    return likes_subquery