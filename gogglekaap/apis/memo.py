from gogglekaap.models.memo import Memo
from gogglekaap.models.users import User
from flask_restx import Namespace, reqparse, fields, Resource
from flask import g

ns = Namespace(
    'memos',
    description='메모 관련 API'
)

memo = ns.model('Memo',{
    'id' : fields.Integer(required = True, decription='메모 고유 번호'),
    'user_id' : fields.Integer(required = True, decription='유저 고유 아이디'),
    'title' : fields.String(required = True, description = '메모 제목'),
    'content' : fields.String(required = True, description ='메모 내용'),
    'created_at' : fields.DateTime(description ='작성 일자'),
    'updated_at' : fields.DateTime(description ='수정 일자')
})

post_parser = reqparse.RequestParser()
post_parser.add_argument('title', required = True, help = '메모 제목')
post_parser.add_argument('content', required = True, help = '메모 내용')

put_parser = post_parser.copy()
put_parser.replace_argument('title', required=False, help = ' 제목 수정')
put_parser.replace_argument('content', required=False, help='수정 내용')

get_parser = reqparse.RequestParser()
get_parser.add_argument('page', required=False, type=int, help='메모 페이지 번호')
get_parser.add_argument('needle', required=False, help='메모 검색')

@ns.route('')
class MemoList(Resource):
    
    @ns.marshal_list_with(memo, skip_none=True )
    @ns.expect(get_parser)
    def get(self):
        '''메모 복수 조회'''
        args = get_parser.parse_args()
        page = args['page']
        needle = args['needle']
        per_page = 5

        base_query = Memo.query.join(
            User,
            User.id == Memo.user_id,
        ).filter(
            User.id ==g.user.id
        )
        
        if needle:
            needle=f'%{needle}%'
            base_query = Memo.query.filter(
                Memo.title.ilike(needle)|Memo.content.ilike(needle)
            )
            
        pages = base_query.order_by(
            Memo.created_at.desc()
        ).paginate(
            page = page,
            per_page = per_page
        )
        return pages.items
    
    @ns.marshal_list_with(memo, skip_none=True )
    @ns.expect(post_parser)  
    def post(self):
        args = post_parser.parse_args()
        memo = Memo(
            title = args['title'],
            content = args['content'],
            user_id = g.user.id
        )
        g.db.add(memo)
        g.db.commit()
        return memo, 201        

@ns.param("id", '메모 고유 번호')
@ns.route("/<int:id>")
class OneMemo(Resource):
    @ns.marshal_list_with(memo, skip_none=True)
    def get(self, id):
        '''메모 단수 조회'''
        memo = Memo.query.get_or_404(id)
        if g.user.id != memo.user_id:
            ns.abort(403)
        return memo
    
    
    @ns.marshal_list_with(memo, skip_none = True)
    @ns.expect(put_parser)
    def put(self, id):
        '''메모 수정'''
        args = put_parser.parse_args()
        memo = Memo.query.get_or_404(id)
        if g.user.id != memo.user_id:
            ns.abort(403)
            
        if args['title'] is not None:
            memo.title = args['title']
        
        if args['content'] is not None:
            memo.content = args['content']
        
        g.db.commit()
        return memo
    
    def delete(self, id):
        memo = Memo.query.get_or_404(id)
        if g.user.id != memo.user_id:
            ns.abort(403)
        
        g.db.delete(memo)
        g.db.commit()
        return '', 204