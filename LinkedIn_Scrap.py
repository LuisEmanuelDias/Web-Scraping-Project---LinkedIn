import requests
import re

def job_check(job_in):
    import re
    if not re.search('jr|junior|práctica|prácticas',job_in.lower()): return False
    if not re.search('data|datos',job_in.lower()): return False
    if not re.search('engineer|ingeniero',job_in.lower()): return False
    return True

def requirements_check(word):
    req_list = ["requirements","requirements","minimum","requerimos","requisitos","expected","minimos","requerida","skill","skills"]
    if word in req_list: return True
    return False
    
number_page = 1     #Determina la cantidad de trabajos que quiero usar para contar

while number_page<40: 
    
    website = f'https://www.linkedin.com/jobs/search/?geoId=&keywords=jr%20data%20engineer&location=España&start={25*(number_page-1)}'
    response = requests.get(website)
    content = response.text
    jobs = re.findall('<a class="base-card__full-link absolute.+href="(.+public_jobs_jserp-result_search-card)" data-tracking-control-name.+\s*<span class="sr-only">\s+(.+)\s+</span>',content)
    
    number_page += 1        #Pasamos a la siguiente página
    if len(jobs[0][0])==0: break
    for name_job,url_job in jobs:
        if not job_check(name_job): continue
        
        respuesta = requests.get(url_job)
        contenido = respuesta.text
        
        print("Anuncio:",name_job)
        with open('start_words',"r") as file:
            list_start_words = re.split('\n',file.read())
        with open('no_start_words',"r") as file:
            list_no_start_words = re.split('\n',file.read())
        with open('finish_words',"r") as file:
            list_finish_words = re.split('\n',file.read())
        with open('garbage_words',"r") as file:
            list_garbage_words = re.split('\n',file.read())
        with open('technical_words',"r") as file:
            list_technical_words = re.split('\n',file.read())

        start_words_len = len(list_start_words)
        no_start_words_len = len(list_no_start_words)
        finish_words_len = len(list_finish_words)
        garbage_words_len = len(list_garbage_words)
        technical_words_len = len(list_technical_words)

        inicio = False
        for x in re.findall('[ ?¿?]([a-zA-Z]+)[ ?:?\??]',respuesta):
            x= x.strip().lower()
            if not inicio:
                if x in list_start_words:               #Si la palabra ya es una palabra de inicio i.e. "Requisitos" inicia la seccion de filtrado
                    inicio = True
                    continue
                if x in list_no_start_words: continue
            
                respuesta = input(f"¿Esta palabra '{x}' marca el inicio? s/n: ").lower()
                if respuesta == "s":
                    inicio = True
                    list_start_words += [x]
                    continue
                list_no_start_words += [x]
                continue
                
            if x in list_finish_words: break
            if x in list_garbage_words: continue
            if x in list_technical_words:
                list_technical_words += [x]
                continue
            
            respuesta = input(f"¿Esta palabra '{x}' es una skill técnica? s/n (si es el final de la seccion de requisitos coloque f): ").lower()
            if respuesta== 's':
                list_technical_words += [x]
                continue
            elif respuesta== "f":
                list_finish_words += [x]
                break
            else:
                list_garbage_words += [x]

        with open('no_start_words',"a") as file:
            for word in list_no_start_words[no_start_words_len-1:]:
                file.write(word+"\n")
        with open('start_words',"a") as file:
            for word in list_start_words[start_words_len-1:]:
                file.write(word+"\n")
        with open('finish_words',"a") as file:
            for word in list_finish_words[finish_words_len-1:]:
                file.write(word+"\n")
        with open('garbage_words',"a") as file:
            for word in list_garbage_words[garbage_words_len-1:]:
                file.write(word+"\n")
        with open('technical_words',"a") as file:
            for word in list_technical_words[technical_words_len-1:]:
                file.write(word+"\n")