from gogglekaap import db
from sqlalchemy import func

memos_labels= db.Table(
    'memos_labels',
    db.Column('memo_id',db.Integer, db.ForeignKey('memo.id'),primary_key=True),
    db.Column('label_id',db.Integer, db.ForeignKey('label.id'),primary_key=True)
)

class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey(
            'user.id',
            ondelete = 'CASCADE'
        ),
        nullable = False
        )
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    linked_image = db.Column(db.String(200),  nullable = True)
    is_deleted = db.Column(db.Boolean(), nullable=False, default=False)
    created_at = db.Column(db.DateTime(), default = func.now())
    updated_at = db.Column(db.DateTime(), default = func.now(), onupdate = func.now())
    labels = db.relationship(
        'Label', #라벨 모델과 연관성을 가져라
        secondary = memos_labels, #다대다 관계 테이블 참조
        backref = db.backref('memos') #Label 객체에서도 memo 객체에 접근하도록 처리
    )

