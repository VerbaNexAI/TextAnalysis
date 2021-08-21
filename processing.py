import re
import unicodedata
import preprocessor as p
import requests
from bs4 import BeautifulSoup
import nltk
nltk.download('punkt')
from nltk.util import ngrams

class Processing(object):

    def __init__(self, lang: str = 'es'):
        self._lang = lang

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
    def delete_special_patterns(text: str):
        result = ''
        try:
            text = re.sub(r'\©|\×|\⇔|\_|\»|\«|\~|\#|\$|\€|\Â|\�|\¬', '', text)# Elimina caracteres especilaes
            text = re.sub(r'\,|\;|\:|\!|\¡|\’|\‘|\”|\“|\"|\'|\`', '', text)# Elimina puntuaciones
            text = re.sub(r'\}|\{|\[|\]|\(|\)|\<|\>|\?|\¿|\°|\|', '', text)  # Elimina parentesis
            text = re.sub(r'\/|\-|\+|\*|\=|\^|\%|\&|\$', '', text)  # Elimina operadores
            text = re.sub(r'\b\d+(?:\.\d+)?\s+', '', text)  # Elimina número con puntuacion
            result = text.lower()
        except Exception as e:
            print('Error delete_special_patterns: {0}'.format(e))
        return result

    @staticmethod
    def make_ngrams(text: str,num: int):
        result = ''
        try:
            n_grams = ngrams(nltk.word_tokenize(text), num)
            result = [ ' '.join(grams) for grams in n_grams]
        except Exception as e:
            print('Error delete_special_patterns: {0}'.format(e))
        return result

    @staticmethod
    def get_URL_Tittle(text: str):
        result = ''
        patern = '\([0-9]*:[0-9]*\) => '  #Definimos los patrones a buscar y variables
        patern2 = '\[|\]'                 #con las que manipularemos los datos
        patern3 = '[\-\?\:\;\$\%\^\&\*\(\)\|\!\`\'\"\,\<\.\>]'
        URL_cont = ''
        
        try:
            text = p.parse(text)
            urx = re.sub(patern2,'',re.sub(patern,'',str(text.urls)))
            if urx != "None":  #Se leeran los urls para obtener el titulo de las paginas
                if "," in urx:    # aqui se revisa si existe mas de 1 url
                 tado = urx.split(",")
                else:
                 tado = urx + "," + "https://www.google.com"
                 tado = tado.split(",") # en caso contrario se agrega una direccion default
                for cor in tado:
                    link = cor #para evitar errores en este ciclo
                    reqs = requests.get(link)
                    soup = BeautifulSoup(reqs.text , 'html.parser')
                    for title in soup.find_all('title'):
                        if title.getText() == "Google":
                            URL_cont += "Null"  #aqui se elimina la pagina default
                        elif title.getText() != "Página no encontrada":
                            var = title.getText() # en caso de obtener el titulo de la pagina
                            temp0 = re.sub(patern3,'',var)#aqui normalizaremos el
                            temp0 = temp0.lower()
                            URL_cont += ""+ str(temp0)   #Se guarda en el contenido
                        else:
                            URL_cont += "Null" # si la pagina no es encontrada
                URL_cont += "~"
            elif urx == "None":
                URL_cont += "Null" + "~"  #En caso de no haber urls , se agrega null
                result = URL_cont.split("~")
        except Exception as e :
            print('Error delete_special_patterns: {0}'.format(e))
        return result
    
    @staticmethod
    def get_normalized_text(folder_path: str, file_name: str) -> str:
        """Extrae el texto de un archivo de texto plano y lo normaliza

        Parameters
        ----------
        ruta_carpeta : str
            string con la ruta de la carpeta donde se encuentre el archivo a normalizar
        nombre_archivo : str
            nombre del archivo que desea normalizar

        Returns
        -------
        posicion 1 : str
            texto normalizado con encoding utf-8
        """
        text = ''
        try:
            with open(f'{folder_path}/{file_name}', 'r', encoding='latin1') as file:
                text = file.read()
                text = self.proper_encoding(text)
                return text
        except Exception as e:
            print(f'Error: {e}')


