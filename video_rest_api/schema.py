from flask_restful import reqparse

# schema using reqparse
video_schema_parser = reqparse.RequestParser()
video_schema_parser.add_argument("name", type=str,  required=True, help="Please provide name of the video")
video_schema_parser.add_argument("views", type=str, required=True, help="Please provide views of the video")
video_schema_parser.add_argument("likes", type=str, required=True, help="Please provide likes of the video")


video_update_schema = reqparse.RequestParser()
video_update_schema.add_argument("name", type=str,  required=False, help="Please provide name of the video")
video_update_schema.add_argument("views", type=str, required=False, help="Please provide views of the video")
video_update_schema.add_argument("likes", type=str, required=False, help="Please provide likes of the video")
