import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

def generar_wordcloud(dict_words,nombre="cloud"):
    """Muestra y genera el wordcloud a partir de un diccionario

    Args:
        dict_words (str): diccionario con formato {palabra(str):frecuencia(int)}
        nombre (str): opcional. Coloque el nombre al archivo png, por defecto es cloud
    """
    stop_words = ["ad","big","data","engineer","engineering","open","analytics","science","plan","developer","user","visualization","business","management","learning","functions","customer","operations"]
    dict_words = {k: v for k,v in dict_words.items() if (k not in stop_words)}
    
    print("\n¡Generando imagen!\n")
    # Create and generate a word cloud image:
    wordcloud = WordCloud(collocations=False,min_font_size=8,max_words=700).generate_from_frequencies(dict_words)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    #plt.title("Palabras comunes en postulaciones para Jr. Data Engineer")
    plt.savefig(f"{nombre}.png", format="png",dpi=1000,bbox_inches = "tight")
    plt.show()
