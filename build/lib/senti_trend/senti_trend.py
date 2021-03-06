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
import joblib  # from sklearn.externals import joblib
import pickle
import warnings, time, sys, os, re

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


def split(delimiters: list, str: string, maxsplit: int = 0) -> list:
	"""
		Example: array: list = split(['.', '?', '!', '"', ";", "\n"], text_)
		:param delimiters: ['.', '?', '!', '"', ";", "\n"]
		:param str:
		:param maxsplit:
		:return: list of sentences
		"""

	regex_pattern = '|'.join(map(re.escape, delimiters))
	res = re.split(regex_pattern, str, maxsplit)
	res = [item for item in res if item.strip('\n\t ') != '']
	return res


def load_models(language_list: list) -> (bool, int):
	"""	 Loading models into global dicts: models_4_sentiment, models_4_trend
	:param language_list: list of languages ['en', 'ro', 'ru', ...]
	:return: (success, time in seconds)
	"""
	global models_4_sentiment, models_4_trend
	# data_dir = os.path.join(os.path.dirname(__file__), 'tests', 'data')
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
			models_4_sentiment['es'] = joblib.load(path + '/es_sentiment_twitter.pkl')
		if 'vi' in language_list:
			num += 1
			uprint('vi, ')
			models_4_sentiment['vi'] = joblib.load(path + '/vi_sentiment_twitter.pkl')

		toc = time.perf_counter()
		print(f"done with {toc - tic:0.2f} seconds")
		load_time_in_sec = toc - tic
		if num == len(language_list):
			return True, load_time_in_sec
		else:
			return False, load_time_in_sec


def detect_lang(text_: string) -> string:
	"""
	detect language of text
	return:  'ro' | 'ru' | 'en', etc..
	"""
	# predictions = lang_model.predict([text_])
	# ([[lang]], [arr]) = predictions
	# lang = predictions
	# return lang.replace('__label__', '')
	return langdetect.detect(text_)


def sentiment_bi(text_: string, lang=None) -> int:
	""" return:  1 - positive |  -1 - negative """
	global models_4_sentiment, models_4_trend, AUTOLOAD
	if lang is None: lang = detect_lang(text_)
	if (not lang in models_4_sentiment) and AUTOLOAD:
		load_models([lang])
	try:
		predictions = models_4_sentiment[lang].predict([text_])
	except:
		raise Exception("No sentiment model for lang: " + lang + " " + text_[:20])
	return predictions[0]


def trend_bi(text_: string, lang=None) -> int:
	""" return:  1 - UP | -1 - DOWN  """
	global models_4_sentiment, models_4_trend, AUTOLOAD
	# lang = langdetect.detect(text_)
	if lang is None: lang = detect_lang(text_)
	if (not lang in models_4_trend) and AUTOLOAD:
		load_models([lang])
	try:
		predictions = models_4_trend[lang].predict([text_])
	except Exception as e:
		# raise Exception("No trend model for lang: " + lang) from e
		raise RuntimeError("No trend model for lang: " + lang + " " + text_[:20], e)

	return predictions[0]


def sentiment(text_: string, for_entity=None, lang=None):
	"""
	:param text_: text for splitting in sentences
	:param for_entity: required entity for filtering
	:param lang: 'ru' | 'en' | 'vi' etc...
	:return: negative, positive
	"""
	if lang is None: lang = detect_lang(text_)
	delimiters: list = ['.', '?', '!', '"', ";", "\n", "\t"]
	array: list = split(delimiters, text_)
	if for_entity is not None:  # filter lines without entity
		array = [line for line in array if for_entity.lower() in line.lower()]
	if array == []: return 0.0, 0.0
	pos, neg = 0, 0
	for sentence in array:
		if sentiment_bi(sentence, lang=lang) == 1:
			pos += 1
		else:
			neg += 1
	return neg / (neg + pos), pos / (neg + pos)


def trend(text_: string, for_entity=None, lang=None):
	"""
	:param text_: text for splitting in sentences
	:param for_entity: required entity for filtering
	:param lang: 'ru' | 'en' | 'vi' etc...
	:return: negative, positive
	"""
	if lang is None: lang = detect_lang(text_)
	delimiters: list = ['.', '?', '!', '"', ";", "\n", "\t"]
	array: list = split(delimiters, text_)
	if for_entity is not None:  # filter lines without entity
		array = [line for line in array if for_entity.lower() in line.lower()]
	if array == []: return 0.0, 0.0
	pos, neg = 0, 0
	for sentence in array:
		if trend_bi(sentence, lang=lang) == 1:
			pos += 1
		else:
			neg += 1
	return neg / (neg + pos), pos / (neg + pos)


texts_ro = [
	'Comunicat InfoTrafic ora 08:00\n07.04.2021 \nServiciul ???InfoTrafic??? al INSP, informeaz??:\nLa aceast?? or??, la nivel na??ional, se circul?? f??r?? careva impedimente, drumurile sunt accesibile, careva obstacole nu se atest??.\n Actualmente ??n mun. Chi??in??u flux sporit de transport, se ??nregistreaz?? la intr??rile ??n ora?? ??i pe arterele principale de transport:\nSectorul BUIUCANI:\n???   str.V.Lupu intersec??ie cu str.Belinski direc??ia de deplasare str.Coca;\nSectorul CENTRU:\n???   intersec??ia str??zior ??os.H??nce??ti ??? str.Sihastrului; \n???   str.Pan Halippa direc??ia de deplasare str.Ismail;\nSectorul CIOCANA:\n??? str. Uzinelor tronsonul str??zilor Voluntarilor ??? Lunca B??cului.\nSectorul R????CANI:\n???    str.Calea Mo??ilor direc??ia de deplasare str.Ismail;\n???    str.Calea Orheiului ??? Studen??ilor, direc??ia intrare ??n ora??;\n???    intersec??ia cu sens giratoriu Calea Orheiului ??? T.Vladimirescu.\n??? Serviciul ???InfoTrafic??? al INSP recomand?? conduc??torilor auto:  \n??? s?? se informeze despre starea ??i situa??ia rutier??;\n??? s?? circule cu o vitez?? redus??, adaptat?? condi??iilor meteo-rutiere ??i de trafic; \n??? s?? m??reasc?? distan??a ??ntre vehicule, pentru a putea fr??na ??i opri ??n condi??ii de siguran????;\n??? s?? nu efectueze manevre periculoase ??n trafic. \nReduce??i viteza, Via??a are prioritate!!!\nhttps://politia.md/node/38600',
	'Precipita??ii sub form?? de ploaie ??i lapovi????\n07.04.2021 \nServiciul ???InfoTrafic??? al INSP, informeaz??: \n La momentul pe ??ntreg teritoriul ????rii c??t ??i ??n mun. Chi??in??u cad precipita??ii slabe sub form?? de ploaie ??i lapovi????, se circul?? ??n condi??iile unui carosabil umed.\n Serviciul ???InfoTrafic??? recomand?? conduc??torilor auto: \n??? s?? se informeze despre starea ??i situa??ia rutier??;\n??? s?? circule cu o vitez?? redus??, adaptat?? condi??iilor meteo-rutiere ??i de trafic; \n??? s?? m??reasc?? distan??a ??ntre vehicule, pentru a putea fr??na ??i opri ??n condi??ii de siguran????;\n??? s?? utilizeze ??n mod corespunz??tor sistemele de iluminare-semnalizare ??i ventila??ie-climatizare;\n??? s?? nu efectueze manevre periculoase ??n trafic. \nConduce??i cu pruden????, Via??a are prioritate!!!\nhttps://politia.md/node/38605',
	'Trafic intens\n07.04.2021 \nServiciul ???InfoTrafic??? al INSP, informeaz??:\n La aceast?? or??, la nivel na??ional se circul?? f??r?? careva impedimente, careva obstacole nu se atest??.\nActualmente ??n mun. Chi??in??u se atest?? flux sporit de transport, pe urm??toarele str??zi:\nSectorul BUIUCANI:\n??? intersec??ia cu sens giratoriu str.Calea Ie??ilor ??? I.Creang?? ??? bd.??tefan cel Mare.\nSectorul BOTANICA:\n??? intersec??ia str??zilor bd.Dacia ??? Hristo Botev;\nSectorul CENTRU:\n??? str.Grenoble tronsonul str??zilor Coste??ti ??? N.Testemi??eanu;\n??? str.Ismail de la str. D.Cantemir p??n?? la str.Calea Basarabiei;\n??? str.Bucure??ti tronsonul str??zilor Ismail ??? Armeneasc??.\nSectorul CIOCANA:\n??? nodul rutier ,,Tutun CTC???.\nSectorul R????CANI:\n??? str. Bogdan Voievod direc??ia de deplasare sens giratoriu A.Russo ??? bd.Moscova;\n??? intersec??ia cu sens giratoriu str. Calea Orheiului ??? T.Vladimirescu;\n??? bd.Rena??terii Na??ionale de la str.Albi??oara direc??ia str.T.Vladimirescu.\nV?? inform??m c?? ??ncep??nd cu data de 05.04.2021 p??n?? pe 30.04.2021 se suspend?? traficul rutier din str. N.Titulescu 4 ??? 6, pentru executarea lucr??rilor a apeductului ??i a canaliz??rii menajer. \nUrmare celor vizate supra, pe segmentele de drum predispuse form??rii ambuteiajelor, sunt prezen??i agen??ii de circula??ie care asigur?? buna desfa??urare a circula??iei rutiere.\n Serviciul ???InfoTrafic??? al INSP recomand?? conduc??torilor auto: s?? adepteze viteza de deplasare la condi??iile de drum, s?? foloseasc?? luminile de ??nt??lnire, s?? m??reasc?? distan??a de siguran???? ??ntre vehicule ??i s?? nu efectueze manevre periculoase ??n trafic, iar ??n caz c??nd ave??i nevoie de ajutor, pute??i apela la num??rul de urgen???? ,,112??? sau s?? v?? adresa??i la cel mai apropiat echipaj de poli??ie.\n \nConduce??i cu pruden???? ??? Via??a are prioritate!!!\nhttps://politia.md/node/38614',
	'15.03.2021\nServiciul ???InfoTrafic??? al INSP, informeaz??:\nPe str.Kiev intersec??ie cu str. Nadejda Russo, este ??nregistrat accident rutier cu implicarea a 3 vehicule, se circul?? cu dificultate pe:\n???  str.Kiev direc??ia bd.Rena??terii Na??ionale;\nServiciul ,,InfoTrafic??? recomand?? conduc??torilor auto: s?? evite deplasarea pe acest tronson de drum, iar ??nainte de a pleca la drum sa se informeze despre starea ??i situa??ia rutier??.',
	'Comunicat InfoTrafic ora 17:00\n20.04.2021 \nServiciul ???InfoTrafic??? al INSP, informeaz??:\n La aceast?? or??, la nivel na??ional, se circul?? ??n condi??iile unui carosabil uscat, drumirile sunt accesibile, careva obstacole sau alte evenimente rutiere nu sunt ??nregistrate.\n Actualmente ??n mun. Chi??in??u se atest?? flux sporit de transport, pe urm??toarele str??zi:\nSectorul BOTANICA:\n??? bd.Iu. Gagarin direc??ia intersec??ia sens giratoriu str.Albi??oara ??? C. Negruzzi;\nSectorul BUIUCANI: \n??? str.Vasile Lupu intersec??ie cu str. V.Belinski, direc??ia str.E.Coca.\nSectorul CENTRU:\n??? str. Ismail direc??ia str. Calea Basarabiei;\n??? intersec??ia str??zilor Bucure??ti ??? Ismail;\nSectorul CIOCANA:\n??? intersec??ia str??zilor Uzinelor ??? Voluntarilor.\nSectorul R????CANI:\n??? bd.Rena??terii Na??ionale direc??ia bd.Gr.Vieru;\n??? intersec??ia cu sens giratoriu Calea Orheiului ??? T.Vladimirescu.\n Serviciul ???InfoTrafic??? al INSP recomand?? conduc??torilor auto: s?? respecte semnalizarea rutier?? temporar??, s?? circule cu o vitez?? redus?? adaptat?? condi??iilor meteo-rutiere ??i de trafic, s?? m??reasc?? distan??a ??ntre vehicule pentru a putea fr??na ??i opri ??n condi??ii de siguran????, ??i s?? nu efectueze manevre periculoase ??n trafic.\nConduce??i cu pruden????, Via??a are prioritate!!!\nhttps://politia.md/node/38846',
]

texts_en = [
	"I don't know if it can help someone, but this solution works for me:",
	"I should add a setter for BaseBlob class, feel free to send me a PR Meanwhile, you can always inherit the class and override it the property  you do not like :).",
	"Has anyway to force to Polyglot use a language? Sometimes when you run the NER, and the pharse have a foreign language entities , it's classified wrong, for that example says that is:  (language code)."
]

texts_ru = [
	"?? ????????-???? ???? ?????? ?? ?????????????????? ?????????? ??????????",
	"?????????????? ?????????? ?????? ?????????????????? ?????????????????? ?? ???????? ??????????",
	"?? ?????????????? ?? ???????????? ???????????? ?????????????? ?????????????? ?????????????? ?????? ????????????????. ",
	"?????? ????????????",
	# "???????? ?????????????? ???????????????????? ???? ????????"
	" ???? ???????? and go to the Moon"
]

if __name__ == '__main__':
	success, load_time = load_models(['ru', 'ro', 'en'])
	# print(success, load_time)

	sentiment_bi(texts_en[0])
	sentiment_bi(texts_ru[0])

	tic = time.perf_counter()
	sentiment_bi(texts_en[0])
	toc = time.perf_counter()
	print(f"  Sentiment calc from sentence takes:  {toc - tic:0.8f} seconds")

	tic = time.perf_counter()
	sentiment_bi(texts_ru[0])
	toc = time.perf_counter()
	print(f"  Sentiment calc from sentence takes:  {toc - tic:0.8f} seconds")

	tic = time.perf_counter()
	trend_bi(texts_en[0])
	toc = time.perf_counter()
	print(f"  Trend calc from sentence  takes:  {toc - tic:0.8f} seconds")

	tic = time.perf_counter()
	# langdetect.detect(texts_en[0])
	detect_lang(texts_en[0])
	toc = time.perf_counter()
	print(f"  Language detection from sentence  takes:  {toc - tic:0.8f} seconds")

	trend_bi(texts_ro[0])
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
