from typing import List, Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from app.configs.database import get_db_connection
from app.database.post import Post


class PostRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def list_regular_posts(
        self,
        page: Optional[int],
        pageSize: Optional[int],
    ) -> (int, list[Post]):
        query = (
            self.db.query(Post).filter(Post.is_ad == False).order_by(Post.score.desc())
        )
        return query.count(), query.offset(page * pageSize).limit(pageSize).all()

    def list_ads_posts(
        self,
        page: Optional[int],
        pageSize: Optional[int],
    ) -> (int, list[Post]):
        query = (
            self.db.query(Post).filter(Post.is_ad == True).order_by(Post.score.desc())
        )
        return query.count(), query.offset(page * pageSize).limit(pageSize).all()

    def get(self, post: Post) -> Post:
        return self.db.get(Post, post.id)

    def create(self, post: Post) -> int:
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post
