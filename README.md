# senti_trend

English, Romanian, Russian, Spanish, Vietnamese (EN, RO, RU, ES, VI ) sentiment and EN, RU trends extractor.

### How to install:
    pip install git+git://github.com/tumikosha/senti_trend/
    or
    pip install dist/senti_trend_tumikosha-1.0.0-py3-none-any.whl


###  Usage example 

    from senti_trend import senti_trend
    success, load_time = senti_trend.load_models(['ru', 'ro', 'en']) # not necessary, senti_trend.AUTOLOAD=True
    print(f"  Loaded in:  {load_time:0.4f} seconds")
    print( senti_trend.sentiment('Hello! We will rise it', lang='en'))  # neg, pos
    print( senti_trend.trend('Hello! We will rise it', lang='en'))      # neg, pos


