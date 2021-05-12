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

# /home/tumi/anaconda374/PKL/en_sentiment_review.pkl

import string
import langdetect
# from sklearn.externals import joblib
import joblib
import pickle
import warnings
import time
import sys, os

# import fasttext

AUTOLOAD = True
models_4_sentiment = dict()
models_4_trend = dict()


# predictions = en_clf.predict(texts_en)
def uprint(*objects, sep=' ', end='', file=sys.stdout):
	""" this func can print UTF-8 on consoles """
	enc = file.encoding
	if enc == 'UTF-8':
		print(*objects, sep=sep, end=end, file=file)
	else:
		f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
		print(*map(f, objects), sep=sep, end=end, file=file)


def load_models(language_list: list) -> (bool, int):
	"""	 Loading models into global dicts: models_4_sentiment, models_4_trend
	:param language_list: list of languages ['en', 'ro', 'ru', ...]
	:return: (success, time in seconds)
	"""
	global models_4_sentiment, models_4_trend
	data_dir = os.path.join(os.path.dirname(__file__), 'tests', 'data')
	print('', os.path.join(sys.prefix, 'PKL'))
	path = os.path.join(sys.prefix, 'PKL')
	print("[X] SENTI_TREND: loading sentiment/trend models from dir  '" + path + "/*' ... ", end="")
	tic = time.perf_counter()
	with warnings.catch_warnings():
		# ignore all caught warnings
		warnings.filterwarnings("ignore")
		num = 0
		if 'en' in language_list:
			num += 1
			uprint('en, ')
			models_4_sentiment['en'] = joblib.load(path + '/en_sentiment_review.pkl')
			models_4_trend['en'] = joblib.load(path + '/en_trend.pkl')
		if 'ru' in language_list:
			num += 1
			uprint('ru, ')
			models_4_sentiment['ru'] = joblib.load(path + '/ru_sentiment_review.pkl')
			models_4_sentiment['bg'] = models_4_sentiment['ru']  # bug in langdetect
			models_4_trend['ru'] = joblib.load(path + '/ru_trend.pkl')
		if 'ro' in language_list:
			num += 1
			uprint('ro, ')
			models_4_sentiment['ro'] = joblib.load(path + '/ro_sentiment_review.pkl')
		if 'es' in language_list:
			num += 1
			uprint('es, ')
			models_4_sentiment['es'] = joblib.load(path + '/es_sentiment_review.pkl')
		if 'vi' in language_list:
			num += 1
			uprint('vi, ')
			models_4_sentiment['vi'] = joblib.load(path + '/vi_sentiment_review.pkl')

		toc = time.perf_counter()
		print(f"done with {toc - tic:0.2f} seconds")
		load_time_in_sec = toc - tic
		if num == len(language_list):
			return True, load_time_in_sec
		else:
			return False, load_time_in_sec


def detect_lang(text_: string) -> string:
	""" return:  'ro' | 'ru' | 'en', etc.. """
	# predictions = lang_model.predict([text_])
	# ([[lang]], [arr]) = predictions
	# lang = predictions
	# return lang.replace('__label__', '')
	return langdetect.detect(text_)


def sentiment(text_: string) -> int:
	""" return:  1 - positive |  0 - negative """
	global models_4_sentiment, models_4_trend, autoload
	lang = detect_lang(text_)
	if (not lang in models_4_sentiment) and AUTOLOAD:
		load_models([lang])
	try:
		predictions = models_4_sentiment[lang].predict([text_])
	except:
		raise Exception("No sentiment model for lang: " + lang)
	return predictions[0]


def trend(text_: string) -> int:
	""" return:  1 - UP | 0 - DOWN  """
	# lang = langdetect.detect(text_)
	lang = detect_lang(text_)
	if (not lang in models_4_trend) and AUTOLOAD:
		load_models([lang])
	try:
		predictions = models_4_trend[lang].predict([text_])
	except Exception as e:
		# raise Exception("No trend model for lang: " + lang) from e
		raise RuntimeError("No trend model for lang: " + lang, e)

	return predictions[0]


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
	success, load_time = load_models(['ru', 'ro', 'en'])
	# print(success, load_time)

	sentiment(texts_en[0])
	sentiment(texts_ru[0])

	tic = time.perf_counter()
	sentiment(texts_en[0])
	toc = time.perf_counter()
	print(f"  Sentiment calc from sentence takes:  {toc - tic:0.8f} seconds")

	tic = time.perf_counter()
	sentiment(texts_ru[0])
	toc = time.perf_counter()
	print(f"  Sentiment calc from sentence takes:  {toc - tic:0.8f} seconds")

	tic = time.perf_counter()
	trend(texts_en[0])
	toc = time.perf_counter()
	print(f"  Trend calc from sentence  takes:  {toc - tic:0.8f} seconds")

	tic = time.perf_counter()
	# langdetect.detect(texts_en[0])
	detect_lang(texts_en[0])
	toc = time.perf_counter()
	print(f"  Language detection from sentence  takes:  {toc - tic:0.8f} seconds")

	trend(texts_ro[0])
# for txt in texts_en:
# 	print("sentiment: ", str(sentiment(txt)) + " trend: " + str(sentiment(txt)) + " #  " + txt)
#
# for txt in texts_ru:
# 	print("sentiment: ", str(sentiment(txt)) + " trend: " + str(sentiment(txt)) + " #  " + txt)

# print("trend: ", [trend(txt) for txt in texts_en])
# print( [sentiment(txt) for txt in texts_ro] )
# print( [sentiment(txt) for txt in texts_ru] )

# print(sentiment(texts_en[1]))
# print(sentiment(" ".join(texts_ro)))
