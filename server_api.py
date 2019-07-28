import json
import inspect
from datetime import datetime
from models import News, Comments, session
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp.web import Request, Response
from sqlalchemy import func, desc, and_
from aiohttp.web_urldispatcher import UrlDispatcher

__version__ = '0.1.0'
DEFAULT_METHODS = ('GET',)


class RestEndpoint:
    """
    This is base class for Entities in News API.
    Provides dispatch method for processing available HTTP methods for entities.
    """
    def __init__(self):
        self.methods = {}

        for method_name in DEFAULT_METHODS:
            method = getattr(self, method_name.lower(), None)
            if method:
                self.register_method(method_name, method)

    def register_method(self, method_name, method):
        self.methods[method_name.upper()] = method

    async def dispatch(self, request: Request):
        """
        This method is used in calling HTTP methods in subclasses.
        :param request: HTTP method. In this API it is GET.
        """
        method = self.methods.get(request.method.upper())
        if not method:
            raise HTTPMethodNotAllowed('', DEFAULT_METHODS)

        method_args = list(inspect.signature(method).parameters)
        received_request_args = request.match_info.copy()
        ordered_method_arguments = {arg_name: received_request_args[arg_name] for arg_name in method_args}

        return await method(**ordered_method_arguments)


class CollectionEndpoint(RestEndpoint):
    """
    This class is used to get all available news.
    Resource param — RestResource instance(News).
    """
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    async def get(self) -> Response:
        all_news = session.query(News, func.count(Comments.id).label('comments_count'))\
            .outerjoin(Comments)\
            .filter(and_(News.deleted == False, News.date <= datetime.now()))\
            .group_by(Comments.news_id)\
            .order_by(desc(News.date))\
            .all()

        return Response(
            status=200,
            body=self.resource.encode({
                'news': [
                    {
                        'id': news.id,
                        'title': news.title,
                        'date': news.date.isoformat(),
                        'body': news.body,
                        'deleted': news.deleted,
                        'comments_count': comments_count
                    }
                    for news, comments_count in all_news
                ],
                'news_count': len(all_news),
            }),
            content_type='application/json')


class InstanceEndpoint(RestEndpoint):
    """
    This class is responsible for getting news with specified identifier.
    Resource -- same RestResource instance as in CollectionEndpoint (News).
    """
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    async def get(self, id) -> Response:
        requested_news = session.query(News)\
            .filter(and_(News.id == id, News.deleted == False, News.date <= datetime.now()))\
            .first()

        if not requested_news:
            return Response(
                status=404,
                body=json.dumps({'not found': 404}),
                content_type='application/json'
            )

        comments_for_requested_news = session.query(Comments)\
            .filter(and_(Comments.news_id == id, Comments.date <= datetime.now()))\
            .order_by(desc(Comments.date))\
            .all()

        return Response(
            status=200,
            body=self.resource.encode({
                'id': requested_news.id,
                'title': requested_news.title,
                'date': requested_news.date.isoformat(),
                'body': requested_news.body,
                'deleted': requested_news.deleted,
                'comments': [
                    {
                        'id': comment.id,
                        'news_id': comment.news_id,
                        'title': comment.title,
                        'date': comment.date.isoformat(),
                        'comment': comment.comment,
                    } for comment in comments_for_requested_news
                ],
                'comments_count': len(comments_for_requested_news),
            }),
            content_type='application/json')


class RestResource:
    def __init__(self, news):
        self.news = news
        self.collection_endpoint = CollectionEndpoint(self)
        self.instance_endpoint = InstanceEndpoint(self)

    def register(self, router: UrlDispatcher):
        router.add_route('*', '/', self.collection_endpoint.dispatch)
        router.add_route('*', f'/{self.news}/{{id}}', self.instance_endpoint.dispatch)

    @staticmethod
    def encode(data):
        return json.dumps(data, indent=4).encode('utf-8')




