#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" EN, RO, RU sentiment and EN, RU trends extractor """

__author__ = "Veaceslav Kunitki"
__copyright__ = "Copyright 2021, Trend extractor project"
__credits__ = ["Veaceslav Kunitki"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Veaceslav Kunitki"
__email__ = "tumikosha@gmail.com"
__status__ = "Production"

import string
import langdetect
# from sklearn.externals import joblib
import joblib
import pickle
import warnings
import time
# import fasttext

print("[X] SENTI_TREND: loading sentiment/trend models from dir PKL/* ... ", end="")
tic = time.perf_counter()
with warnings.catch_warnings():
	# ignore all caught warnings
	warnings.filterwarnings("ignore")
	# execute code that will generate warnings
	ro_clf = joblib.load('PKL/ro_sentiment_review.pkl')
	en_clf = joblib.load('PKL/en_sentiment_review.pkl')
	ru_clf = joblib.load('PKL/ru_sentiment_review.pkl')
	ru_trend_clf = joblib.load('PKL/ru_trend.pkl')
	en_trend_clf = joblib.load('PKL/en_trend.pkl')
	# fasttext.FastText.eprint = lambda x: None  # supress fasttext warnings
	# lang_model = fasttext.load_model('PKL/lid.176.bin')

toc = time.perf_counter()
print(f"done  with {toc - tic:0.2f} seconds")


def detect_lang(text_: string) -> string:
	""" return:  'ro' | 'ru' | 'en', etc.. """
	# predictions = lang_model.predict([text_])
	# ([[lang]], [arr]) = predictions
	# lang = predictions
	# return lang.replace('__label__', '')
	return langdetect.detect(text_)


def universal_sentiment(text_: string) -> int:
	""" return:  1 - positive |  0 - negative | 9999 - unsupported language """
	lang = detect_lang(text_)
	if lang == "en":
		predictions = en_clf.predict([text_])
		return predictions[0]
	if lang == "ro":
		predictions = ro_clf.predict([text_])
		return predictions[0]
	if lang == "ru" or lang == "bg":
		predictions = ru_clf.predict([text_])
		return predictions[0]
	return 9999


def universal_trend(text_: string) -> int:
	""" return:  1 - UP, 0 - DOWN, 9999 - unsupported language  """
	# lang = langdetect.detect(text_)
	lang = detect_lang(text_)
	if lang == "en":
		predictions = en_trend_clf.predict([text_])
		return predictions[0]

	if lang == "ru" or lang == "bg":
		predictions = ru_trend_clf.predict([text_])
		return predictions[0]
	return 9999


texts_ro = [
	'Comunicat InfoTrafic ora 08:00\n07.04.2021 \nServiciul ”InfoTrafic” al INSP, informează:\nLa această oră, la nivel național, se circulă fără careva impedimente, drumurile sunt accesibile, careva obstacole nu se atestă.\n Actualmente în mun. Chişinău flux sporit de transport, se înregistrează la intrările în oraș și pe arterele principale de transport:\nSectorul BUIUCANI:\n•   str.V.Lupu intersecţie cu str.Belinski direcţia de deplasare str.Coca;\nSectorul CENTRU:\n•   intersecția străzior șos.Hîncești – str.Sihastrului; \n•   str.Pan Halippa direcția de deplasare str.Ismail;\nSectorul CIOCANA:\n• str. Uzinelor tronsonul străzilor Voluntarilor – Lunca Bîcului.\nSectorul RÎȘCANI:\n•    str.Calea Moșilor direcția de deplasare str.Ismail;\n•    str.Calea Orheiului – Studenţilor, direcția intrare în oraş;\n•    intersecția cu sens giratoriu Calea Orheiului – T.Vladimirescu.\n• Serviciul ”InfoTrafic” al INSP recomandă conducătorilor auto:  \n• să se informeze despre starea și situația rutieră;\n• să circule cu o viteză redusă, adaptată condițiilor meteo-rutiere și de trafic; \n• să mărească distanța între vehicule, pentru a putea frâna și opri în condiții de siguranță;\n• să nu efectueze manevre periculoase în trafic. \nReduceți viteza, Viața are prioritate!!!\nhttps://politia.md/node/38600',
	'Precipitații sub formă de ploaie și lapoviță\n07.04.2021 \nServiciul ”InfoTrafic” al INSP, informează: \n La momentul pe întreg teritoriul țării cît și în mun. Chișinău cad precipitații slabe sub formă de ploaie și lapoviță, se circulă în condițiile unui carosabil umed.\n Serviciul ”InfoTrafic” recomandă conducătorilor auto: \n• să se informeze despre starea și situația rutieră;\n• să circule cu o viteză redusă, adaptată condițiilor meteo-rutiere și de trafic; \n• să mărească distanța între vehicule, pentru a putea frâna și opri în condiții de siguranță;\n• să utilizeze în mod corespunzător sistemele de iluminare-semnalizare și ventilație-climatizare;\n• să nu efectueze manevre periculoase în trafic. \nConduceți cu prudență, Viața are prioritate!!!\nhttps://politia.md/node/38605',
	'Trafic intens\n07.04.2021 \nServiciul ”InfoTrafic” al INSP, informează:\n La această oră, la nivel național se circulă fără careva impedimente, careva obstacole nu se atestă.\nActualmente în mun. Chişinău se atestă flux sporit de transport, pe următoarele străzi:\nSectorul BUIUCANI:\n• intersecția cu sens giratoriu str.Calea Ieșilor – I.Creangă – bd.Ștefan cel Mare.\nSectorul BOTANICA:\n• intersecția străzilor bd.Dacia – Hristo Botev;\nSectorul CENTRU:\n• str.Grenoble tronsonul străzilor Costești – N.Testemițeanu;\n• str.Ismail de la str. D.Cantemir pînă la str.Calea Basarabiei;\n• str.Bucureşti tronsonul străzilor Ismail – Armenească.\nSectorul CIOCANA:\n• nodul rutier ,,Tutun CTC”.\nSectorul RÎȘCANI:\n• str. Bogdan Voievod direcția de deplasare sens giratoriu A.Russo – bd.Moscova;\n• intersecția cu sens giratoriu str. Calea Orheiului – T.Vladimirescu;\n• bd.Renaşterii Naţionale de la str.Albişoara direcţia str.T.Vladimirescu.\nVă informăm că începînd cu data de 05.04.2021 pînă pe 30.04.2021 se suspendă traficul rutier din str. N.Titulescu 4 – 6, pentru executarea lucrărilor a apeductului și a canalizării menajer. \nUrmare celor vizate supra, pe segmentele de drum predispuse formării ambuteiajelor, sunt prezenţi agenţii de circulaţie care asigură buna desfaşurare a circulaţiei rutiere.\n Serviciul ”InfoTrafic” al INSP recomandă conducătorilor auto: să adepteze viteza de deplasare la condițiile de drum, să folosească luminile de întîlnire, să mărească distanța de siguranță între vehicule și să nu efectueze manevre periculoase în trafic, iar în caz cînd aveți nevoie de ajutor, puteți apela la numărul de urgență ,,112” sau să vă adresați la cel mai apropiat echipaj de poliție.\n \nConduceți cu prudență – Viața are prioritate!!!\nhttps://politia.md/node/38614',
	'15.03.2021\nServiciul ”InfoTrafic” al INSP, informează:\nPe str.Kiev intersecție cu str. Nadejda Russo, este înregistrat accident rutier cu implicarea a 3 vehicule, se circulă cu dificultate pe:\n•  str.Kiev direcția bd.Renașterii Naționale;\nServiciul ,,InfoTrafic” recomandă conducătorilor auto: să evite deplasarea pe acest tronson de drum, iar înainte de a pleca la drum sa se informeze despre starea și situația rutieră.',
	'Comunicat InfoTrafic ora 17:00\n20.04.2021 \nServiciul ”InfoTrafic” al INSP, informează:\n La această oră, la nivel național, se circulă în condițiile unui carosabil uscat, drumirile sunt accesibile, careva obstacole sau alte evenimente rutiere nu sunt înregistrate.\n Actualmente în mun. Chişinău se atestă flux sporit de transport, pe următoarele străzi:\nSectorul BOTANICA:\n• bd.Iu. Gagarin direcția intersecția sens giratoriu str.Albișoara – C. Negruzzi;\nSectorul BUIUCANI: \n• str.Vasile Lupu intersecție cu str. V.Belinski, direcția str.E.Coca.\nSectorul CENTRU:\n• str. Ismail direcția str. Calea Basarabiei;\n• intersecția străzilor București – Ismail;\nSectorul CIOCANA:\n• intersecția străzilor Uzinelor – Voluntarilor.\nSectorul RÎȘCANI:\n• bd.Renașterii Naționale direcția bd.Gr.Vieru;\n• intersecția cu sens giratoriu Calea Orheiului – T.Vladimirescu.\n Serviciul ”InfoTrafic” al INSP recomandă conducătorilor auto: să respecte semnalizarea rutieră temporară, să circule cu o viteză redusă adaptată condițiilor meteo-rutiere și de trafic, să mărească distanța între vehicule pentru a putea frâna și opri în condiții de siguranță, și să nu efectueze manevre periculoase în trafic.\nConduceți cu prudență, Viața are prioritate!!!\nhttps://politia.md/node/38846',
]

texts_en = [
	"I don't know if it can help someone, but this solution works for me:",
	"I should add a setter for BaseBlob class, feel free to send me a PR Meanwhile, you can always inherit the class and override it the property  you do not like :).",
	"Has anyway to force to Polyglot use a language? Sometimes when you run the NER, and the pharse have a foreign language entities , it's classified wrong, for that example says that is:  (language code)."
]

texts_ru = [
	"А кого-то он ещё и последних денег лишил",
	"Биткоин лишил нас романтики брошенных в рожу денег",
	"В субботу в Москве прошёл сольный концерт Валерии «До предела». ",
	"Все хорошо",
	# "Цена ракетой подпрыгнет на луну"
	" на Луну and go to the Moon"
] 

if __name__ == '__main__':
	# predictions = en_clf.predict(texts_en)
	# print(predictions)

	tic = time.perf_counter()
	universal_sentiment(texts_en[0])
	toc = time.perf_counter()
	print(f"  Sentiment calc from sentence takes:  {toc - tic:0.8f} seconds")

	tic = time.perf_counter()
	universal_trend(texts_en[0])
	toc = time.perf_counter()
	print(f"  Trend calc from sentence  takes:  {toc - tic:0.8f} seconds")

	tic = time.perf_counter()
	# langdetect.detect(texts_en[0])
	detect_lang(texts_en[0])
	toc = time.perf_counter()
	print(f"  Language detection from sentence  takes:  {toc - tic:0.8f} seconds")

	# for txt in texts_en:
	# 	print("sentiment: ", str(universal_sentiment(txt)) + " trend: " + str(universal_sentiment(txt)) + " #  " + txt)
	#
	# for txt in texts_ru:
	# 	print("sentiment: ", str(universal_sentiment(txt)) + " trend: " + str(universal_sentiment(txt)) + " #  " + txt)

	# print("trend: ", [universal_trend(txt) for txt in texts_en])
	# print( [universal_sentiment(txt) for txt in texts_ro] )
	# print( [universal_sentiment(txt) for txt in texts_ru] )

	# print(universal_sentiment(texts_en[1]))
	# print(universal_sentiment(" ".join(texts_ro)))
