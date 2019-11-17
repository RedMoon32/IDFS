import requests
from flask import Flask, request, Response, jsonify
import os
from flask_api import status

app = Flask(__name__)

PORT = 2020
FILE_STORE = "./data"


# @TODO
# rewrite all methods using Flask Restful


@app.route("/ping")
def ping():
    return "Hello, Data Node is Alive!"


@app.route("/filesystem", methods=["GET"])
def filesystem():
    if request.method == "GET":
        # @TODO - recursively check file on filesystem
        def recursive_file_get(path):
            pass

        files = recursive_file_get(FILE_STORE)
        # for now - just files in current directory
        return jsonify(os.listdir(FILE_STORE))


@app.route("/file", methods=["GET", "POST", "DELETE"])
def file():
    filename = request.args["filename"]

    if '/' in filename:
        return Response('/ are not allowed in file name!', 400)

    fpath = os.path.join(FILE_STORE, filename)

    if request.method == "GET":
        if not os.path.exists(fpath):
            return Response(f"File not found", 404)
        f = open(fpath, 'r')
        content = f.read()
        return Response(content, 200, mimetype='text/plain')

    elif request.method == "POST":
        try:
            if os.path.exists(fpath):
                return Response(f"File already exists", 400)
            f = open(fpath, 'wb')
            f.write(request.data)
            return Response(status=201)

        except Exception as e:
            return Response(f"Error opening file ", 400)

    elif request.method == "DELETE":
        if not os.path.exists(fpath):
            return Response(f"File not found", 404)
        else:
            os.remove(fpath)
            return Response(status=200)


def init_node():
    if not os.path.exists(FILE_STORE):
        os.mkdir(FILE_STORE)
    # run master node first
    requests.post("http://localhost:3030/datanode?ip=http://127.0.0.1&port=2020")
    app.run(host='0.0.0.0', port=PORT)


if __name__ == "__main__":
    init_node()