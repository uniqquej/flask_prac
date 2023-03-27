from gogglekaap.models.memo import Memo
from flask_restx import Namespace, reqparse, fields, Resource

ns = Namespace(
    'memos',
    description='메모 관련 API'
)

memo = ns.model('Memo',{
    'id' : fields.Integer(required = True, decription='메모 고유 번호'),
    'title' : fields.String(required = True, description = '메모 제목'),
    'content' : fields.String(required = True, description ='메모 내용'),
    'created_at' : fields.DateTime(description ='작성 일자'),
    'updated_at' : fields.DateTime(description ='수정 일자')
})

post_parser = reqparse.RequestParser()
post_parser.add_argument('title', required = True, help = '메모 제목')
post_parser.add_argument('content', required = True, help = '메모 내용')

@ns.route('')
class MemoList(Resource):
    @ns.marshal_list_with(memo, skip_none=True)
    def get(self):
        data = Memo.query.all()
        return data