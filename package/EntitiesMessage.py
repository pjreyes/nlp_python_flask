import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from pandas.io.json import json_normalize 
import spacy, json,sys
# from CorpusIntents import CorpusIntents


class EntitiesMessage(object):
    sys.path.append('../')

    def __init__(self,entidades,mensaje):
        self.entidades = entidades
        self.mensaje = mensaje
        self.resultado = self.here_we_go(self.entidades,self.mensaje) 

    def get_sinonyms(self,dataIn):
        response = requests.get("http://sesat.fdi.ucm.es:8080/servicios/rest/sinonimos/json/{}".format(str(dataIn)))
        array = [data["sinonimo"] for data in response.json()["sinonimos"]]
        return array

    # print(get_sinonyms("reclamo"))
    # print(type(get_sinonyms("reclamo")))
    # REEMPLAZAR SINONIMOS

    # sinonimos = ['a','b']
    # for ind,sin in enumerate(sinonimos):
    #     clean_tokens_sin = [word.replace(sinonimos[ind],'palabra') for word in clean_tokens]

    def clean_tokenizer(self,contentIn):
        tokens = word_tokenize(contentIn,"spanish")
        tokens = [word.lower() for word in tokens if word.isalpha()]
        clean_tokens = tokens [:]
        for token in tokens:
            if  token in stopwords.words('spanish'):
                clean_tokens.remove(token)
        return clean_tokens

    def lemma_tokens(self,cleanTokens):
        nlp = spacy.blank('es')
        clean_tokens_sin_lem = []
        separador = ' '
        for token in nlp(separador.join(cleanTokens)):
            clean_tokens_sin_lem.append(token.lemma_)
        return clean_tokens_sin_lem

    def sinonyms_replacer(self,arrayIn,cleanTokens):
        clean_tokens_sin = []
        for root in arrayIn:
            sinonimos=self.get_sinonyms(str(root))
            temp = []
            print(root,sinonimos)
            for ind, sin in enumerate(sinonimos):
                if not clean_tokens_sin :
                    clean_tokens_sin = [word.replace(sinonimos[ind],str(root)) for word in cleanTokens]
                else:
                    clean_tokens_sin = [word.replace(sinonimos[ind],str(root)) for word in clean_tokens_sin]
        return clean_tokens_sin

    def critical_entities(self,sinoTokens,entidades):
        sinoTokens = set(sinoTokens)
        entidades = set(entidades)
        unique_list = sinoTokens.intersection(entidades)
        temp = []
        for i in unique_list:
            temp.append(i)
        
        return temp

    def frequence_calculate(self,tokenIn):
        freq = nltk.FreqDist(tokenIn)
        json_parse = [{'token' : str(key),'frequence': val} for key,val in freq.items()]
        # inyectar a la bd
        return {'list_freq':json_parse}

    def sorting_frequence(self,freqIn,critical):
        df = json_normalize(freqIn['list_freq'])
        jsonDF = df.sort_values(['frequence'],ascending=False)
        bestFreq = jsonDF.query('frequence > 1').to_json(orient='records')
        return {'criticals': critical,'sort_freq': json.loads(bestFreq)}
    
        # print(type(json))

    # entidad = ['traslado','jefe','maricon','lento']
    # frase= "alo alo maricon conchetumadre sernac falabella Hola buenas tardes Lic Reynaldo Sambueza en este numero con el no lo he no lo estamos llamando de transporte para delante por una entrega de un seccional exactamente un sofa que se llama confirmar que es entrego en perfectas condiciones no se si usted estan al tanto pero yo hice un mal momento que llego al rato pues hice un cambio de un cambio de producto bonita por la vagina por internet ya Cual fue el problema El problema fue que llego la mitad por eso estoy llamando directamente del transporte y a la otra parte del sofa esta aca en la bodega del transporte ya se queria entregar manana el faltante verdad Mira te guste bueno el servicio que se presento ayer en mi hogar pues voy a dejar claro iban a ir con Rober cada uno esta embarazada y ella le dijo a lo lamento persona que con esto le digo si voy a revisarlo frente a ellos ellos llegaron despues laburar y no quisieron que lo abrieras entre ellos hicieron Cualquier cosa ahi esta el numero ya menos despues ya entonces para rematar todo esto aparte de que le pone pozol agrio cierto y por ejemplo respaldo novia no venia la parte de la evolucion sillon tipo l excepcional Tampoco tampoco viene por ahi entonces como como no se burlan con la tripulacion de ayer que ya por favor porque yo llame yo Bueno yo te mando mis datos y todo lo que"
    def here_we_go(self,entidad,frase):
        tokens = self.clean_tokenizer(frase)
        lemmatizar = self.lemma_tokens(tokens)
        categorizar = self.sinonyms_replacer(entidad,lemmatizar)
        freq = self.frequence_calculate(categorizar)
        critical = self.critical_entities(categorizar,entidad)
        result = self.sorting_frequence(freq,critical)
        return result

    # prueba = CorpusIntents(frase,"Denuncia")
    # print("RESULTADO")
    # print(prueba.resultado)
