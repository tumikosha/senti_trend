# import senti_trend
import time
from src.senti_trend import senti_trend
success, load_time = senti_trend.load_models(['ru', 'ro', 'en'])
r = senti_trend.sentiment('Hello! We will rise it')
print(r)

tic = time.perf_counter()
senti_trend.sentiment(senti_trend.texts_en[0])
toc = time.perf_counter()
print(f"  Sentiment calc from sentence takes:  {toc - tic:0.8f} seconds")


tic = time.perf_counter()
senti_trend.sentiment(senti_trend.texts_ro[0])
toc = time.perf_counter()
print(f"  Sentiment calc from sentence takes:  {toc - tic:0.8f} seconds")


tic = time.perf_counter()
senti_trend.sentiment(senti_trend.texts_ru[0])
toc = time.perf_counter()
print(f"  Sentiment calc from sentence takes:  {toc - tic:0.8f} seconds")

tic = time.perf_counter()
senti_trend.trend(senti_trend.texts_ru[0])
toc = time.perf_counter()
print(f"  Trend from sentence takes:  {toc - tic:0.8f} seconds")
