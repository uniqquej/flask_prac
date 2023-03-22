from gogglekaap import db
from sqlalchemy import func


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(20), unique = True, nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=func.now()) #server_default > 값이 없던 데이터들도 같이 update // default > 이후 부터 적용
    
    @classmethod
    def find_one_by_user_id(cls, user_id):
        return User.query.filter_by(user_id=user_id).first()