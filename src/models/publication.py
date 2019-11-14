from flask_restplus import fields
from src.server.application import server

news = server.api.model('News', {
    'title': fields.String(required=True, min_length=1, max_length=300, description='Publication title'),
    'summary': fields.String(required=True, min_length=1, max_length=300, description='Publication summary'),
    'text': fields.String(required=True, min_length=1, description='Publication text'),
    'author': fields.String(required=True, min_length=1, max_length=300, description='Publication author'),
    'datetime': fields.DateTime(required=False, dt_format='iso8601')
})

news_edit = server.api.model('News_edit', {
    'title': fields.String(required=True, min_length=1, max_length=300, description='Publication title'),
    'summary': fields.String(required=True, min_length=1, max_length=300, description='Publication summary'),
    'text': fields.String(required=True, min_length=1, description='Publication text')
})
