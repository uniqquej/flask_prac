from gogglekaap import db
from sqlalchemy import func

class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'user.id',
            ondelete = 'CASCADE'
        ),
        nullable=False
    )
    content = db.Column(db.String(10), nullable=False, unique=False)
    created_at = db.Column(db.DateTime(), default=func.now())
    
    #한 유저의 라벨은 유니크함 ( 같은 라벨 여러개 존재 X)
    __table_args__ = (
        db.UniqueConstraint(
            "content",
            "user_id",
            name = "uk_content_user_id"
        ),
    )