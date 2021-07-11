import re
import unicodedata


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