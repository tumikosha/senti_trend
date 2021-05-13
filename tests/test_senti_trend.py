def test_sentiment():
	from senti_trend.senti_trend import sentiment
	text = """ 
	По мнению Бледсо, если подобная тенденция сохранится, то человечество может не достигнуть цели Парижского соглашения — углеродной нейтральности к 2050 году. Это, в свою очередь, повысит риск катастрофических климатических изменений.
	"""
	neg, pos = sentiment(text, lang='ru')
	# neg, pos = sentiment(text)
	print(neg, pos)
	assert neg==1/2


# def test_split():
# 	from senti_trend.senti_trend import sentiment
# 	text = """
# 	По мнению Бледсо, если подобная тенденция сохранится, то человечество может не достигнуть цели Парижского соглашения — углеродной нейтральности к 2050 году. Это, в свою очередь, повысит риск катастрофических климатических изменений.
# 	"""
# 	neg, pos = sentiment(text, lang='ru')
# 	# neg, pos = sentiment(text)
# 	print(neg, pos)
# 	assert neg==1/3
