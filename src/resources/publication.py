import json
import datetime as dt

from bson import ObjectId, json_util
from flask_restplus import Resource, reqparse
from pymongo import MongoClient, ReturnDocument

from src.config.database import db_env_config
from src.models.publication import news, news_edit
from src.server.application import server


app, api, req = server.app, server.api, server.req

ns_news = api.namespace('news', description='Newspaper API')

parser = reqparse.RequestParser()
parser.add_argument('q', type=str, required=True, action='append', location='args')

client = MongoClient(host=db_env_config["host"], port=db_env_config["port"])
mydb = client["newspaper"]


@ns_news.route('/')
class PublicationList(Resource):

    def get(self):
        """
            Displays a list of publications
        :return:
        """
        cursor = mydb.publication.find({}, {"_id": 0})
        data = []
        for pub in cursor:
            data.append(pub)
        docs_sanitized = json.loads(json_util.dumps(data))
        return {"response": docs_sanitized}

    @ns_news.expect(news, validate=True)
    def post(self):
        """
            Adds a new publication
        :return:
        """
        data = req.get_json()
        data['author'] = ObjectId(data['author'])
        if not data:
            return {"response": "error"}, 404
        else:
            title = data.get('title')
            if title:
                if mydb.publication.find_one({"title": title}):
                    return {"response": 'publication already exists'}, 403
                else:
                    if mydb.author.find_one({"_id": data['author']}):
                        obj_id = mydb.publication.insert_one(data).inserted_id
                        doc_sanitized = json.loads(json_util.dumps(obj_id))
                        return {"response": doc_sanitized}, 200


@ns_news.route('/<string:id>')
class PublicationResource(Resource):

    @ns_news.doc(
        params={
            'id': 'Specify the Id associated'},
        responses={
            200: 'OK',
            400: 'Invalid Argument',
            500: 'Mapping Key Not Found'})
    def get(self, id):
        """
            Displays a publications details
        :param id: identifier
        :return:
        """
        try:
            document = mydb.publication.find_one({"_id": ObjectId(id)})
            doc_sanitized = json.loads(json_util.dumps(document))
            return {"response": doc_sanitized}, 200
        except KeyError as e:
            api.abort(500, e.__doc__, status="Could not retrieve information", statusCode="500")
        except Exception as e:
            api.abort(400, e.__doc__, status="Could not retrieve information", statusCode="400")

    @ns_news.doc(
        params={
            'id': 'Specify the Id associated'},
        responses={
            200: 'OK',
            400: 'Invalid Argument',
            500: 'Mapping Key Error'})
    @api.expect(news_edit, validate=True)
    def put(self, id):
        """
            Update a publication
        :param id:
        :return:
        """
        try:
            data = req.get_json()
            document = mydb.publication.find_one_and_update({"_id": ObjectId(id)},
                                                            {
                                                                '$set': {
                                                                    "title": data['title'],
                                                                    "summary": data['summary'],
                                                                    "text": data['text'],
                                                                    "datetime": dt.datetime.now().isoformat()
                                                                }
                                                            },
                                                            projection={'_id': False, 'author': False},
                                                            return_document=ReturnDocument.AFTER)
            doc_sanitized = json.loads(json_util.dumps(document))
            return {"response": doc_sanitized}, 200
        except KeyError as e:
            api.abort(500, e.__doc__, status="Could not retrieve information", statusCode="500")

    @ns_news.doc(
        params={
            'id': 'Specify the Id associated'},
        responses={
            200: 'OK',
            400: 'Invalid Argument',
            500: 'Mapping Key Error'})
    def delete(self, id):
        """
            Delete a publication
        :param id:
        :return:
        """
        try:
            document = mydb.publication.delete_one({"_id": ObjectId(id)})
            if document.deleted_count != 0:
                return {"response": 'deleted'}, 200
        except KeyError as e:
            api.abort(500, e.__doc__, status="Could not retrieve information", statusCode="500")
        except Exception as e:
            api.abort(400, e.__doc__, status="Could not retrieve information", statusCode="400")


@ns_news.route('/search')
class NewsResourceSearch(Resource):

    @ns_news.doc(
        params={'q': 'Query a title, text and author'}
    )
    def get(self):
        """
            Search by publications
        :return:
        """
        data = parser.parse_args()
        documents = mydb.publication.find(
            {
                '$or': [
                    {"title": {'$regex': data['q'][0]}},
                    {"text": {'$regex': data['q'][0]}},
                    {"author": {'$regex': data['q'][0]}}
                ]
            }
        )
        doc_sanitized = json.loads(json_util.dumps(documents))

        return {"response": doc_sanitized}, 200
