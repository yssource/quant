import numpy as np
import pandas as pd
from xgboost import XGBClassifier
import sys

columns = ['time','ticker', 'bids1', 'asks1', 'bsize1', 'asize1', 'last_price', 'last_size', 'volume', 'turnover', 'open_interest']
df = pd.read_csv("data.csv", names=columns)
df['mid'] = (df['bids1'] + df['asks1'])/2
df['delta'] = df['mid'].diff(periods=1).fillna(0)
df['labels'] = df['delta'] >0  #1-up 0-down
d = df['labels']
d[df['delta'] < 0] = -1
print df.head()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df.drop(['labels', 'time', 'ticker'], axis=1).values, df['labels'], test_size=0.1, random_state=0)


model = XGBClassifier(
    max_depth=10,
    n_estimators=20)

model.fit(
    X_train,
    y_train,
    eval_metric="error",
    eval_set=[(X_train, y_train), (X_test, y_test)],
    verbose=True)

a=model.predict(X_test)
