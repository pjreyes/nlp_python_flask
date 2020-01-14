from flask_restful import Resource, Api, abort,reqparse
from flask import jsonify, request
import json

class NLP(Resource):
    def post(self):
        from package.EntitiesMessage import EntitiesMessage
        from package.CorpusIntents import CorpusIntents
        from package.GoogleSentiments import GoogleSentiments
        from pandas.io.json import json_normalize 

        import logging
        import requests
        import sys
        sys.path.append('../')
        import json,re,os

        try:
            logging.basicConfig(level = logging.INFO)
            args = request.get_json(force=True)
            logging.info("request : "+str(args))
            listIntents = os.listdir(os.getcwd()+"/corpus")
            entities = []
            intents = []
            if ( args['message'] is not None ):
                entidad = ['traslado','jefe','maricon','lento']
                mensaje = args['message']
                print(os.getcwd())
                entities = EntitiesMessage(entidad,mensaje)
                for nombresIntents in listIntents: 
                    print(nombresIntents)
                    pathFile = str(os.getcwd()+"/corpus/")+nombresIntents
                    temp = CorpusIntents(mensaje,pathFile)
                    intents.append(temp.resultado)
            df = json_normalize(intents)
            jsonDF = df.sort_values(['score'],ascending=False)
            listIntents = jsonDF.query('score > 0').to_json(orient='records')
            response = {
                        'intents':{
                            'top_intent':json.loads(listIntents)[0],
                            'list_intents':json.loads(listIntents)
                            },
                        'entities':entities.resultado
                        }
            
            logging.info("response : "+str(response))
            
        except Exception as e:
            logging.error("Exception {}".format(e))
            
        return response
    # def sorting_frequence(self,freqIn):
    #     df = json_normalize(freqIn['ListFreq'])
    #     jsonDF = df.sort_values(['frequence'],ascending=False)
    #     bestFreq = jsonDF.query('frequence > 1').to_json(orient='records')
    #     return {'SortFreq': json.loads(bestFreq)}