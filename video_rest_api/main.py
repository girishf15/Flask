import os

from flask import Flask
from flask_restful import Resource, Api, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

from dao.video import VideoModel
from schema import video_schema_parser, video_update_schema

app = Flask(__name__)

# restful
api = Api(app)

# db config
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'

db = SQLAlchemy(app)
db.init_app(app)
db.create_all()

resource_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'views' : fields.Integer,
    'likes' : fields.Integer
    }


# define resources
class Video(Resource):

    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result: 
            abort(404, message=f"Video with {video_id} doesn't exists..")

        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_schema_parser.parse_args()
        if not VideoModel.query.filter_by(id=video_id).first():
            video = VideoModel(id=video_id, name=args["name"], views=args["views"], likes=args["likes"])
            db.session.add(video)
            db.session.commit()
            return video, 201
        abort(404, message="VideoId already exists..")


    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_schema.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message=f"Video with {video_id} doesn't exists..")

        if "name" in args and args["name"]:
            result.name = args["name"]

        if "likes" in args and args["likes"]:
            result.likes = args["likes"]

        if "views" in args and args["views"]:
            result.views = args["views"]

        db.session.commit()

        return result


    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message=f"Video with {video_id} doesn't exists..")
        result = VideoModel.query.filter_by(id=video_id).delete()
        print("result", result)
        db.session.commit()
        return 204
        

# add resource to api
api.add_resource(Video, '/video/<int:video_id>')

if __name__ == "__main__":
    if not os.path.exists('database.db'):
        db.create_all()
    app.run(debug=True, use_reloader=True)