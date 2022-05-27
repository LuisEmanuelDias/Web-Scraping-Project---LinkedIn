import requests
import re

def job_check(job_in):
    """Comprueba si el titulo del trabajo es para "junior data engineer" con sus variantes en español o abreviaturas

    Args:
        job_in (str): titulo del trabajo

    Returns:
        boolean: True si el trabajo es para "junior data engineer"
    """
    import re
    if not re.search('jr|junior|práctica|prácticas',job_in.lower()): return False
    if not re.search('data|datos',job_in.lower()): return False
    if not re.search('engineer|ingeniero',job_in.lower()): return False
    return True

   
def info_preciosa(pais,pages=40):
    """Extrae las palabras que aparecen los trabajos publicados para Jr. Data Engineer en LinkedIn

    Args:
        pais (str): país sobre el cual se hara la busqueda. ADVERTENCIA: Escribalo bien
        pages (int): cantidad de paginas de LinkedIn.Por defecto es 40. NOTA: Si pone mas de 40 no explota.
        
    Returns:
        dict: retorna el diccionario de palabras
    """
    dict_words = {} 
    number_page = 1  
    number_jobs = 0

    while number_page<pages: 
        
        #Extrae la informacion de la primera pagina
        website = f'https://www.linkedin.com/jobs/search/?geoId=&keywords=jr%20data%20engineer&location={pais.capitalize()}&start={25*(number_page-1)}'
        response = requests.get(website)
        content = response.text
        #Expresion regular para obtener [(url_trabajo,nombre_trabajo),...]
        jobs = re.findall('<a class="base-card__full-link absolute.+href="(.+public_jobs_jserp-result_search-card)" data-tracking-control-name.+\s*<span class="sr-only">\s+(.+)\s+</span>',content)
        
        
        print(f"Se van a analizar {25*number_page} trabajos...")
        #Iteracion sobre todos los trabajos de la pagina "number_page"
        for url_job,name_job in jobs:
            #Checkeo de si el trabajo es Junior Data Engineer
            if not job_check(name_job): continue
            number_jobs +=1
            
            #Se introduce dentro de la url de la postulacion
            respuesta = requests.get(url_job)
            contenido = respuesta.text
            #Extrae el texto de la convocatoria
            text = str(re.findall('\@context.+"description":"(.+)","employmentType"',contenido))

            #Extracción de palabras html
            html_words = ["/strong&gt;","strong&gt;","/p&gt;","p&gt;","/li&gt;","li&gt;","/&lt;","&lt;","/ul&gt;","ul&gt;","/br&gt;","br&gt;","/u&gt;","u&gt;"]
            for x in html_words:
                text = re.sub(x," ",text)
            
            #Lista con las palabras del texto
            palabras = re.findall("[a-zA-Z]+",text)
            
            #Conteo de palabras
            for palabra in palabras:
                palabra = palabra.lower()
                if palabra in dict_words.keys():
                    dict_words[palabra] += 1
                else:
                    dict_words[palabra] = 1
            print(f"Trabajo Jr n° {number_jobs} analizado...")
        print("¡SIGUIENTE PÁGINA!\n")
        number_page += 1        #Pasamos a la siguiente página
        
    print(f"¡Proceso terminado! Se analizaron {number_jobs} postulaciones para Jr.")
    return dict_words
        
def carga_dict_linkedin(dict_words,nombre="word_frecuency"):
    """Carga los datos del diccionario de frecuencia de palabras en un archivo

    Args:
        dict_words (dict): diccionario con frecuencia de palabras. {palabra:cantidad}
        nombre (str): nombre que se le desea poner al archivo. Por defecto: "word_frecuency".
    """
    with open(nombre,"w") as file:
        for word,value in dict_words.items():
            file.write(f"{word};{value}\n") 