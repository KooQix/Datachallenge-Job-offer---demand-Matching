

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import unidecode
import spacy
nlp = spacy.load("fr_core_news_md")
lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words('french')
stop_words += ["bon", "qualite", "devoir", "quel", "profil", "competence", "salarie", "necessaire", "avoir", "etre", "être", "faire", "connaissance", "connaitre", "devenir", "embauche", "tant", "metier", "requis", "exercer", "afin", "outre", "dote", "grand", "savoir", "dispose", "egalement", "aimer", "aime", "surtout", "requérir", "necessite", "necessiter", "posseder", "comme", "falloir", "reclame", "beaucoup", "tres", "travaille", "preuve", "tout", "parfait", "travail", "maitriser", "capacite", "indispensable", "plus", "bien", "car", "different", "plus", "obligatoire"]


def preprocessing(data: str, spacy: bool, more_stop_words=[]):
	
	# Remove html tags & other
	data = unidecode.unidecode(data) # Remove accents
	data = re.sub(re.compile('<.*?>'), '', data)
	data = re.sub("[^a-zA-Z]+", " ", data)

	# Lower case
	data = data.lower()

	# Tokenization
	tokens = word_tokenize(data)
	
	data = [lemmatizer.lemmatize(word) for word in tokens]


	# Join words in preprocessed data, to return a string
	data = " ".join(data)

	if (spacy):
		_data = nlp(data)
		data_tok = [token.lemma_ for token in _data]

		# Stop words removal
		data = [word for word in data_tok if word not in (stop_words + more_stop_words)]
		data = " ".join(data)

	return data