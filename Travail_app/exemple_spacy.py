import spacy
from fuzzywuzzy import fuzz
nlp = spacy.load('fr_core_news_md')
doc="Tu peux allumer la lampe du salon?"
doc = nlp(doc)
cool=[]
for token in doc:
    cool.append(token.lemma_)
cool=' '.join(cool)    
print(cool)
Str1 = "allumer les lampes"
Str2 = "partir a la peche"
Partial_Ratio = fuzz.partial_ratio(Str1.lower(),Str2.lower())
print(Partial_Ratio)
