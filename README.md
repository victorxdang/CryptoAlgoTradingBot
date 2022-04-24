# Algorithmic Trading Bot via Kraken API

[![Screen-Shot-2022-04-24-at-1-49-16-PM.png](https://i.postimg.cc/cJGvxBtC/Screen-Shot-2022-04-24-at-1-49-16-PM.png)](https://postimg.cc/sMKjKScC)

# Background

We will be creating an algorithmic crypto trading bot that will use the Kraken API to get crypto prices. We will use machine learning to determine the trend of the market from historical data and determine the best strategies/indicators to use.

Our bot will also be deployed to a server doing paper trading runs to see how well the bot could do if it was in a live setting. During the paper trading run, it will also utilize machine learning to determine if the entries/exits are appropriate or not.

---

## Technologies

The data we're analyzing comes from a jupyter notebook that we'll create and import files to. We'll also be using Python to run and read our data. 

* [Google Colab](https://colab.research.google.com/) - Online jupyter notebook that enables us to run the code.

* [SVM](https://scikit-learn.org/stable/modules/svm.html) - Machine Learning techniques to train our model data.
  
* [Niave Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html) - Machine Learning techniques to train our model data.

---

## Installation Guide

A list of imports and calls made for our code to run successfully.

```python
import base64
import fire
import hashlib
import hmac
import importlib
import json
import krakenex
import numpy as np
import pandas as pd
import questionary
import requests
import re
import Source.Bot as bot
import urllib.parse

from pykrakenapi import KrakenAPI
from API.Endpoints import KrakenEndpoints
from API import KrakenRequests
from finta import TA
from Helper import Utilities as util
from matplotlib.pyplot import plot
from pandas import DataFrame
from pandas.tseries.offsets import DateOffset
from pykrakenapi import KrakenAPI
from os import listdir
from os.path import isfile
from sklearn import svm
from sklearn import naive_bayes
from sklearn.naive_bayes import ComplementNB
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from Source.BaseStrategy import BaseStrategy
from Source.Kraken import Kraken
```
---

## Data Preparation

* Pulled data from the Kraken Public API.
* Grabbed all OHLC data and created a list within a dataframe for analysis.

[![BTC-OHLC-CHART.png](https://i.postimg.cc/kgdp8wGK/BTC-OHLC-CHART.png)](https://postimg.cc/YhbRB61C)


---

## Machine / Deep Learning Modeling
* Our strategy will utilize SVC to predict ideal entry and exit signals for the trading bot.

* We decided on using Support Vector Machines, more precisely, Support Vector Classifiers (SVC),  in our trading algorithm as it handles large datasets effectively and efficiently.


[![ADA-ML-Backtest.png](https://i.postimg.cc/GtPCjvh7/ADA-ML-Backtest.png)](https://postimg.cc/zHf6zbhK)

---
## Evaluation Report
* Major Findings
  * Based on some backtesting runs, the bot did not perform too well, but there is room for improvement.

  * As for optimization, we could improve the training and test data as there may be some overfitting or underfitting issues.

* Conclusion
  * As of now, our trading strategy only contains the strategy itself and a machine learning algorithm to determine entries and exits. A major factor in determining the success of a trading strategy is to also include risk management, as in calculate position sizing, stop-losses, take-profits, diversification of trades, along with numerous other factors.

[![ADA-Chart.png](https://i.postimg.cc/FzXvcTmk/ADA-Chart.png)](https://postimg.cc/wy2nYc19)

---

## Contributors

Brought to you by [Angel Reyes](https://github.com/AngelR0), [Elgin Braggs Jr.](https://github.com/nustalgic), [Kevin Scott](https://github.com/Kevintscott01), and [Victor Dang](https://github.com/victorxdang/)

---
## License

MIT
