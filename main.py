import LinkedIn_Scrap as ls
import dict_creation as dc
import data_preparation as dp
import data_visualization as dv

print("Este mini proyecto permite visualizar a través de un wordcloud las palabras técnicas comunes en búsquedas de Jr. Data Engineer")
pais = input("Escriba un país para realizar la búsqueda: ")
paginas = input("Escriba la cantidad de páginas de LinkedIn que desea analizar: (si está apura coloque 10 o menos) " )

#Inicia el proceso de extracción y conteo de palabras en postulaciones de LinkedIn
palabras_linkedin = ls.info_preciosa(pais,int(paginas))
#Carga el diccionario de palabras extraidas en "word_frecuency"
ls.carga_dict_linkedin(palabras_linkedin)

#Obtiene palabras claves relacionadas a Data Engineer
palabras_tecnicas = dc.paginas_glosario()
#Almacena dichas palabras
dc.carga_glosario(list_words= palabras_tecnicas)

#Filtra las palabras de LinkedIn de acuerdo a la lista de palabras claves
dict_palabras_filtro = dp.generar_texto(["java","scala","r"])
#GEnera el wordcloud
dv.generar_wordcloud(dict_palabras_filtro)


