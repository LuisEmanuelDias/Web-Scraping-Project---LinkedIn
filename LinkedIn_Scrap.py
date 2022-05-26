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

dict_words = {} 
number_page = 1     


while number_page<40: 
    
    website = f'https://www.linkedin.com/jobs/search/?geoId=&keywords=jr%20data%20engineer&location=España&start={25*(number_page-1)}'
    response = requests.get(website)
    content = response.text
    jobs = re.findall('<a class="base-card__full-link absolute.+href="(.+public_jobs_jserp-result_search-card)" data-tracking-control-name.+\s*<span class="sr-only">\s+(.+)\s+</span>',content)
    
    print(f"Se han analizado datos de {25*number_page} trabajos...")
    for url_job,name_job in jobs:
        if not job_check(name_job): continue
        
        respuesta = requests.get(url_job)
        contenido = respuesta.text
        
        text = str(re.findall('\@context.+"description":"(.+)","employmentType"',contenido))
        html_words = ["/strong&gt;","strong&gt;","/p&gt;","p&gt;","/li&gt;","li&gt;","/&lt;","&lt;","/ul&gt;","ul&gt;","/br&gt;","br&gt;","/u&gt;","u&gt;"]
        for x in html_words:
            text = re.sub(x," ",text)
        
        palabras = re.findall("[a-zA-Z]+",text)
        
        for palabra in palabras:
            palabra = palabra.lower()
            if palabra in dict_words.keys():
                dict_words[palabra] += 1
            else:
                dict_words[palabra] = 1
    print("Guardando datos...")
    with open('word_frecuency.csv',"w") as file:
            for word,value in dict_words.items():
                file.write(f"{word};{value}\n") 
    number_page += 1        #Pasamos a la siguiente página
    
    print("¡Proceso terminado!")