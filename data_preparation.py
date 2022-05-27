import pandas as pd
import re

def generar_texto(extras=[]):
    """Genera diccionario de palabras con la interseccion de los contenidos en
    los archivos 'word_frecuency' y 'list_technical_words'

    Args:
        extras (list, str): lista de palabras tecnicas que se quieran agregar). Por defecto es [].

    Returns:
        dict: retorna el diccionario de palabras
    """
    palabras_linkedin = pd.read_csv("word_frecuency",delimiter=';',names=["Job","Count"])
    palabras_related_to_job = pd.read_csv("list_technical_words",names = ["words"])

    palabras_extras = extras
    palabras_related_to_job["words"].append(pd.Series(palabras_extras))
    
    palabras_linkedin_s_outliers = palabras_linkedin[(palabras_linkedin["Count"]< 
                                                    ((palabras_linkedin["Count"].mean())+ 3*(palabras_linkedin["Count"].std())))]


    plink = palabras_linkedin_s_outliers.to_dict()

    for k,v in plink.items():
        if re.match("[^s]$",k):
            plink[k] += plink[k+"s"]
            plink[k+"s"] = plink[k]

    palabras_linkedin_s_outliers = pd.DataFrame.from_dict(plink)
    
    palabras_filtradas = pd.merge(palabras_linkedin_s_outliers,palabras_related_to_job,left_on='Job',right_on='words')
    
    dict_words = {}

    for word in palabras_filtradas["Job"]:
        dict_words[word]= int(palabras_filtradas["Count"][palabras_filtradas["Job"] == word])
    return dict_words


