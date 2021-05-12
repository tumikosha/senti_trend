# senti_trend

English, Romanian, Russian, Spanish, Vietnamese (EN, RO, RU, ES, VI ) sentiment and EN, RU trends extractor.

---=== usage example ===----
from senti_trend import senti_trend 
success, load_time = senti_trend.load_models(['ru', 'ro', 'en']) # not necessary, senti_trend.AUTOLOAD=True 
print( senti_trend.sentiment('Hello! We will rise it'))  # returns: 0 | 1
print( senti_trend.trend('Hello! We will rise it'))      # returns: 0 | 1
