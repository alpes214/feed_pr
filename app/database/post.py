import uuid

from sqlalchemy import UUID, Boolean, CheckConstraint, Column, Integer, String, and_
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import text as al_text

from app.database.base_model import EntityMeta


class Post(EntityMeta):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    title = Column(String, nullable=False)
    author = Column(String(10), nullable=False)
    link = Column(String, nullable=True)
    text = Column(String, nullable=True)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    is_ad = Column(Boolean, default=False)
    nsfw = Column(Boolean, default=False)
    category = Column(String, nullable=True)

    __table_args__ = (
        CheckConstraint(
            and_(
                al_text(
                    "text IS NOT NULL OR link IS NOT NULL"
                ),  # At least one of them is NOT NULL
                al_text("text IS NULL OR link IS NULL"),  # At least one of them is NULL
            )
        ),
    )

    @hybrid_property
    def score(self):
        return self.likes - self.dislikes

    def __repr__(self):
        return f"<Post(id='{self.id}', is_ad={self.is_ad}, nsfw={self.nsfw})>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
