from gogglekaap.models.label import Label as LabelModel
from gogglekaap.models.users import User as UserModel
from flask_restx import Namespace, fields, Resource, reqparse
from flask import g


ns = Namespace(
    'labels',
    description='라벨 관련 api'
)

label = ns.model('Label',{
    'id' : fields.Integer(required=True, description='라벨 고유 번호'),
    'user_id' : fields.Integer(required=True, description='라벨 작성자 유저 아이디'),
    'content': fields.String(required=True, description='라벨 내용'),
    'created_at' : fields.DateTime(description='라벨 생성 일자')
})

post_parser = reqparse.RequestParser()
post_parser.add_argument('content', required=True, help='라벨 내용')

@ns.route('')
class LabelList(Resource):
    @ns.marshal_list_with(label, skip_none=True)
    def get(self):
        data = LabelModel.query.all()
        return data
    
    @ns.marshal_list_with(label, skip_none=True)
    @ns.expect(post_parser)
    def post(self):
        '''라벨 생성'''
        args = post_parser.parse_args()
        content = args['content']
        
        #라벨이 있는지 미리 확인
        label = LabelModel.query.join(
            UserModel,
            UserModel.id == LabelModel.user_id,
        ).filter(
            UserModel.id == g.user.id,
            LabelModel.content == content
        ).first()
        
        if label:
            ns.abort(409)
        
        label = LabelModel(
            user_id = g.user.id,
            content = content
        )    
        g.db.add(label)
        g.db.commit()
        return label, 201

