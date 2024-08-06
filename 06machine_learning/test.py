import numpy as np

a = np.array([1,2,3,4,5])
a2 = [1,2,3,4,5]

print(a)
print(a2)

import pandas as pd

df = pd.DataFrame(
    {'이름': ['홍길동', '장마철', '소나기', '더워요'],
     'Age' : [23, 55, 24, 16],
     '성별': ['male', 'female', 'female', 'male']}
)

print(df)
# display(df)


df.drop('성별', axis=1, inplace=True)
print(df)