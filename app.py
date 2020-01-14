from flask import Flask, request, Response
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify
import logging
import sys, os
import json
from servicios.NLPServices import NLP

sys.path.append('../')


app = Flask(__name__)
api = Api(app)


api.add_resource(NLP,'/api/v1/nlpservices')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0',port=port)
