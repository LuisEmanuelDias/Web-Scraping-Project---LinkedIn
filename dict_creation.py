#Aquí crearemos el diccionario DATA ENGINEER
import requests
from bs4 import BeautifulSoup
import re

def paginas_glosario():
    """Extrae de tres páginas palabras tecnicas relacionadas a Data Engineer y retorna una lista con las mismas.

    Returns:
        list,str : retorna la lista de palabras técnicas.
    """
    #Páginas a cargar
    pagina_1 = "https://www.silect.is/blog/data-engineering-glossary/"
    pagina_2 = "https://towardsdatascience.com/complete-data-engineers-vocabulary-87967e374fad"
    pagina_3 = "https://www.trifacta.com/data-engineering-glossary/#:~:text=Data%20Engineers%20are%20the%20individuals,store%2C%20manage%2C%20..."

    list_words = []     #Variable que almacena las palabras

    #Carga de primer página
        #header para evitar el error 403
    header1 = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 OPR/87.0.4390.25'
    }
    response = requests.get(pagina_1,headers=header1)
    content = response.text

    list_words += re.findall('<td><strong>([^_=."<>]+)</strong></td>',content)
    list_words += re.findall('<td><strong><a\n.+>(.+)</a></strong></td>',content)

    #Carga de segunda página
    response = requests.get(pagina_2)
    content = response.text
    list_words += re.findall('<strong class="ma kk">(\w+ ?\w+?)</strong></a>',content)

    #Carga de tercera página
    response = requests.get(pagina_3)
    content = response.text
    soup = BeautifulSoup(content,"lxml")
    list_words += re.findall('<div class="glossaryTerm" data-alpha="\w" data-term="(.+)">',soup.prettify())
                
    list_words_uncopled = []

    for word in list_words:
        list_words_uncopled += re.findall("\w+",word.lower())

    aux_list = []
    for word in list_words_uncopled:
        if word in aux_list: continue
        aux_list += [word]
    
    return aux_list

def carga_glosario(nombre="list_technical_words",list_words=[]):
    """Almacena en un archivos las palabras ingresadas como lista

    Args:
        nombre (str): Nombre del archivo a guardar. Por defecto "list_technical_words".
        list_words (list,str): Lista de palabras a ingresar. Por defecto []
        
    """
    with open(nombre,"w") as file:
        for word in list_words:
            file.write(word+"\n")