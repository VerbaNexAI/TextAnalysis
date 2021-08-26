import re
import nltk
import spacy
import unicodedata
import preprocessor as p
import requests
from bs4 import BeautifulSoup
from nltk import TweetTokenizer
from spacy.lang.es import Spanish
from spacy.lang.en import English

nltk.download('punkt')
from nltk.util import ngrams


class TextProcessing(object):
    name = 'Text Processing'
    lang = 'es'

    def __init__(self, lang: str = 'es'):
        self.lang = lang

    @staticmethod
    def proper_encoding(text: str):
        result = ''
        try:
            text = unicodedata.normalize('NFD', text)
            text = text.encode('ascii', 'ignore')
            result = text.decode("utf-8")
        except Exception as e:
            print('Error proper_encoding: {0}'.format(e))
        return result

    @staticmethod
    def stopwords(text: str):
        result = ''
        try:
            nlp = Spanish()if TextProcessing == 'es' else English()
            doc = nlp(text)
            token_list = [token.text for token in doc]
            sentence = []
            for word in token_list:
                lexeme = nlp.vocab[word]
                if not lexeme.is_stop:
                    sentence.append(word)
            result = ' '.join(sentence)
        except Exception as e:
            print('Error stopwords: {0}'.format(e))
        return result

    @staticmethod
    def remove_patterns(text: str):
        result = ''
        try:
            text = re.sub(r'\©|\×|\⇔|\_|\»|\«|\~|\#|\$|\€|\Â|\�|\¬', '', text)
            text = re.sub(r'\,|\;|\:|\!|\¡|\’|\‘|\”|\“|\"|\'|\`', '', text)
            text = re.sub(r'\}|\{|\[|\]|\(|\)|\<|\>|\?|\¿|\°|\|', '', text)
            text = re.sub(r'\/|\-|\+|\*|\=|\^|\%|\&|\$', '', text)
            text = re.sub(r'\b\d+(?:\.\d+)?\s+', '', text)
            result = text.lower()
        except Exception as e:
            print('Error remove_patterns: {0}'.format(e))
        return result

    @staticmethod
    def transformer(text: str, stopwords: bool = False):
        result = ''
        try:
            text_out = TextProcessing.proper_encoding(text)
            text_out = text_out.lower()
            text_out = re.sub("[\U0001f000-\U000e007f]", ' ', text_out) if '[EMOJI]' else text_out
            text_out = re.sub(
                r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+'
                r'|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
                ' ', text_out) if '[URL]' else text_out
            text_out = re.sub("@([A-Za-z0-9_]{1,40})", ' ', text_out) if '[MENTION]' else text_out
            text_out = re.sub("#([A-Za-z0-9_]{1,40})", ' ', text_out) if '[HASTAG]' else text_out
            text_out = TextProcessing.remove_patterns(text_out)
            # text_out = TextAnalysis.lemmatization(text_out) if lemmatizer else text_out
            text_out = TextProcessing.stopwords(text_out) if stopwords else text_out
            text_out = re.sub(r'\s+', ' ', text_out).strip()
            text_out = text_out.rstrip()
            result = text_out if text_out != ' ' else None
        except Exception as e:
            print('Error transformer: {0}'.format(e))
        return result

    @staticmethod
    def tokenizer(text: str):
        val = []
        try:
            text_tokenizer = TweetTokenizer()
            val = text_tokenizer.tokenize(text)
        except Exception as e:
            print('Error make_ngrams: {0}'.format(e))
        return val

    @staticmethod
    def make_ngrams(text: str, num: int):
        result = ''
        try:
            n_grams = ngrams(nltk.word_tokenize(text), num)
            result = [' '.join(grams) for grams in n_grams]
        except Exception as e:
            print('Error make_ngrams: {0}'.format(e))
        return result

    @staticmethod
    def get_URL_Tittle(text: str):
        result = ''
        pattern = '\([0-9]*:[0-9]*\) => '  # Definimos los patrones a buscar y variables
        patern2 = '\[|\]'  # con las que manipularemos los datos
        patern3 = '[\-\?\:\;\$\%\^\&\*\(\)\|\!\`\'\"\,\<\.\>]'
        URL_cont = ''

        try:
            text = p.parse(text)
            urx = re.sub(patern2, '', re.sub(pattern, '', str(text.urls)))
            if urx != "None":  # Se leeran los urls para obtener el titulo de las paginas
                if "," in urx:  # aqui se revisa si existe mas de 1 url
                    tado = urx.split(",")
                else:
                    tado = urx + "," + "https://www.google.com"
                    tado = tado.split(",")  # en caso contrario se agrega una direccion default
                for cor in tado:
                    link = cor  # para evitar errores en este ciclo
                    reqs = requests.get(link)
                    soup = BeautifulSoup(reqs.text, 'html.parser')
                    for title in soup.find_all('title'):
                        if title.getText() == "Google":
                            URL_cont += "Null"  # aqui se elimina la pagina default
                        elif title.getText() != "Página no encontrada":
                            var = title.getText()  # en caso de obtener el titulo de la pagina
                            temp0 = re.sub(patern3, '', var)  # aqui normalizaremos el
                            temp0 = temp0.lower()
                            URL_cont += "" + str(temp0)  # Se guarda en el contenido
                        else:
                            URL_cont += "Null"  # si la pagina no es encontrada
                URL_cont += "~"
            elif urx == "None":
                URL_cont += "Null" + "~"  # En caso de no haber urls , se agrega null
                result = URL_cont.split("~")
        except Exception as e:
            print('Error delete_special_patterns: {0}'.format(e))
        return result
