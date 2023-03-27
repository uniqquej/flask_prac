from gogglekaap import db
from sqlalchemy import func

class Memo(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey(
            'user.id',
            ondelete = 'CASCADE'
        ),
        nullable = False
        )
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime(), default = func.now())
    updated_at = db.Column(db.DateTime(), default = func.now(), onupdate = func.now())