import sqlite3

from flask import Flask
from flask_restful import Resource, Api, reqparse
from enum import Enum

app = Flask(__name__)
api = Api(app)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class ErrorCode(Enum):
    UNKNOWN_ERROR = 1,
    UNKNOWN_METHOD = 2,
    INVALID_REQUEST = 8,
    INTERNAL_ERROR = 10,
    INVALID_REQUIRED_ARG = 100,


def error_msg(code: ErrorCode):
    if code == ErrorCode.INVALID_REQUIRED_ARG:
        return "One of the parameters specified was missing or invalid: count should be positive"
    elif code == ErrorCode.INVALID_REQUEST:
        return "Invalid request"


def error(code: ErrorCode, args):
    if code == ErrorCode.INVALID_REQUIRED_ARG:
        return {"error": {
            "error_code": ErrorCode.INVALID_REQUIRED_ARG,
            "error_msg": error_msg(ErrorCode.INVALID_REQUIRED_ARG),
            "request_params": {**args}
        }}
    elif code == ErrorCode.INVALID_REQUEST:
        return {
            "error": {
                "error_code": ErrorCode.INVALID_REQUEST,
                "error_msg": error_msg(ErrorCode.INVALID_REQUEST),
                "request_params": {**args}
            }
        }


allowed_fields = ["stream_url", "img_url", "category"]


def check_fields(fields: list[str]):
    return not any([1 for field in fields if field not in allowed_fields])


conn = sqlite3.connect("database.db")
c = conn.cursor()
c.row_factory = dict_factory


def get_station(cursor, station_ids=[], fields=[], constraints={}, count=None, offset=None):
    if not check_fields(fields):
        return False

    constraints_list = []
    if "stream_url" in constraints:
        constraints_list.append("stream_url = {}".format(constraints["stream_url"]))
    if "img_url" in constraints:
        constraints_list.append("img_url = {}".format(constraints["img_url"]))

    p_cons_cat = "category_id" in constraints
    if p_cons_cat:
        constraints_list.append("category_id = {}".format(constraints["category_id"]))

    get_fields = ["id", "name"]
    if "stream_url" in fields:
        get_fields.append("stream_url")
    if "img_url" in fields:
        get_fields.append("img_url")
    p_sel_cat = "category_id" in fields
    if p_sel_cat:
        get_fields.append("category_id")

    statement = "SELECT {} FROM station WHERE".format(",".join(get_fields))
    if station_ids:
        statement += " id IN ({})".format(",".join(station_ids))
    if constraints_list:
        if station_ids:
            statement += " AND"
        statement += " {}".format("AND ".join(constraints_list))

    if p_sel_cat or p_cons_cat:
        statement += " INNER JOIN categories ON categories.station_id = station.id"
    if count:
        statement += " LIMIT" + count
    if offset:
        statement += " OFFSET" + offset

    return cursor.execute(statement).fetchall()


class StationGet(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument("station_ids", type=str, required=True)
        parser.add_argument("fields", type=str)

        args = parser.parse_args()

        station_ids = args["station_ids"].split(",")
        fields = args["fields"].split(",") if "fields" in args else []

        if not check_fields(fields):


        where_statement = "ID IN ({})".format(",".join(station_ids))
        selected_columns = ["id, name", *fields]

        statement = "SELECT ({}) FROM station WHERE {}".format(selected_columns, where_statement)
        stations = c.execute(statement).fetchall()

        response = {
            "response": [
                {
                    **station
                } for station in stations
            ]
        }
        return response, 200


class StationSearch(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument("count", type=int, default=100)
        parser.add_argument("offset", type=int, default=0)

        parser.add_argument("category_id", type=int)
        parser.add_argument("stream_url", type=str)
        parser.add_argument("img_url", type=str)

        parser.add_argument("fields", type=str)

        args = parser.parse_args()
        if not (args["category_id"] or args["stream_url"] or args["img_url"]):
            return error(ErrorCode.INVALID_REQUIRED_ARG, args)

        where_list = []
        if "category_id" in args:
            where_list.append("category_id = {}".format(args["category_id"]))
        if "stream_url" in args:
            where_list.append("stream_url = {}".format(args["stream_url"]))
        if "img_url" in args:
            where_list.append("img_url = {}".format(args["img_url"]))
        where_statement = ", ".join(where_list)

        count = args["count"]
        offset = args["offset"]
        fields = args["fields"] if "fields" in args else []

        if not check_fields(fields):
            return error(ErrorCode.INVALID_REQUEST, args)
        selected_columns = ", ".join(fields)






api.add_resource(StationGet, "/method/stations.get")
api.add_resource(StationSearch, "/method/stations.search")

if __name__ == "__main__":
    app.run()
