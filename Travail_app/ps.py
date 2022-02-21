from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import spacy
nlp = spacy.load("fr_core_news_sm")


stemmer = SnowballStemmer(language='french')

def return_stem(sentence):
    doc = nlp(sentence)
    return [stemmer.stem(X.text) for X in doc]
return_stem('je suis entrain d\'ecire une choses remarquable')
