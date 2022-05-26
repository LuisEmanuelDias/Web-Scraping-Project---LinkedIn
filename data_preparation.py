import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS

palabras_linkedin = pd.read_csv("word_frecuency",delimiter=';',names=["Job","Count"])
palabras_related_to_job = pd.read_csv("list_technical_words",names = ["words"])

palabras_extras = ["java","scala","warehouse"]
palabras_related_to_job["words"].append(pd.Series(palabras_extras))

palabras_linkedin_s_outliers = palabras_linkedin[(palabras_linkedin["Count"]< ((palabras_linkedin["Count"].mean())+ 3*(palabras_linkedin["Count"].std())))]


palabras_filtradas = pd.merge(palabras_linkedin_s_outliers,palabras_related_to_job,left_on='Job',right_on='words')

texto = ""

for x in palabras_filtradas["Job"]:
    texto += f"{x} "*int(palabras_filtradas["Count"][palabras_filtradas["Job"] == x])

stopwords = ["data","engineer","engineering","analytics","science","plan","developer","user","visualization","business","management","learning"]
# Create and generate a word cloud image:
wordcloud = WordCloud(collocations=False,stopwords= stopwords).generate(texto)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Palabras comunes en postulaciones para Jr. Data Engineer")
plt.savefig("cloud.png", format="png")
plt.show()

