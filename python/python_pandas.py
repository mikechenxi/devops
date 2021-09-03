import pandas as pd
from pandas import Series, DataFrame

# Series
[in]: obj = Series([10, 9, 8, 7, 6])
[out]: 
0    10
1     9
2     8
3     7
4     6
dtype: int64

[in]: obj.index
[out]: RangeIndex(start=0, stop=5, step=1)

[in]: obj.values
[out]: array([10,  9,  8,  7,  6], dtype=int64)

[in]: obj = Series([10, 9, 8, 7, 6])
[in]: obj.index = ['a', 'b', 'c', 'd', 'e']
[in]: obj
[out]:
a    10
b     9
c     8
d     7
e     6
dtype: int64

[in]: obj = Series([10, 9, 8, 7, 6], index = ['a', 'b', 'c', 'd', 'e'])
[out]: 
a    10
b     9
c     8
d     7
e     6
dtype: int64

[in]: obj[2]
[out]: 8

[in]: obj[[1, 2]]
[out]: 
b    9
c    8
dtype: int64

[in]: obj['b']
[out]: 9

[in]: obj[['b', 'c']]
[out]: 
b    9
c    8
dtype: int64

[in]: obj[1] = 11
[in]: obj
[out]: 
a    10
b    11
c     8
d     7
e     6
dtype: int64

[in]: obj[obj > 8]
[out]: 
a    10
b    11
dtype: int64

[in]: obj * 2
[out]: 
a    20
b    22
c    16
d    14
e    12
dtype: int64

[in]: 'a' in obj
[out]: True

[in]: dic = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
[in]: obj = Series(dic)
[in]: obj
[out]:
a    1
b    2
c    3
d    4
e    5
dtype: int64

[in]: index = ['A',  'a', 'b', 'c', 'd', 'e']
[in]: obj = Series(dic, index)
[in]: obj
[out]:
A    NaN
a    1.0
b    2.0
c    3.0
d    4.0
e    5.0
dtype: float64

[in]: pd.isnull(obj) / obj.isnull
[out]:
A     True
a    False
b    False
c    False
d    False
e    False
dtype: bool

[in]: pd.notnull(obj) / obj.notnull
[out]: 
A    False
a     True
b     True
c     True
d     True
e     True
dtype: bool

[in]: obj1 = Series([10, 9, 8, 7, 6, None], index = ['a', 'b', 'c', 'd', 'e', 'f'])
[in]: obj1
[out]:
a    10.0
b     9.0
c     8.0
d     7.0
e     6.0
f     NaN
dtype: float64

[in]: obj2 = Series([10, 9, 8, 7], index = ['a', 'b', 'c', 'd']
[in]: obj2
[out]:
a    10
b     9
c     8
d     7
dtype: int64

[in]: obj1 + obj2:
[out]: 
a    20.0
b    18.0
c    16.0
d    14.0
e     NaN
f     NaN
dtype: float64

# DataFrame
[in]: data = {
	'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
	'year': [2000, 2001, 2002, 2001, 2002],
	'pop': [1.5, 1.7, 3.6, 2.4, 2.9]
}
[in]: frame = DataFrame(data)
[out]:
    state  year  pop
0    Ohio  2000  1.5
1    Ohio  2001  1.7
2    Ohio  2002  3.6
3  Nevada  2001  2.4
4  Nevada  2002  2.9

[in]: frame = DataFrame(data, columns = ['pop', 'year', 'state'])
[out]:
   pop  year   state
0  1.5  2000    Ohio
1  1.7  2001    Ohio
2  3.6  2002    Ohio
3  2.4  2001  Nevada
4  2.9  2002  Nevada

[in]: frame = DataFrame(data, columns = ['pop', 'year', 'state', 'debt'], index = ['one', 'two', 'three', 'four', 'five'])
[out]:
       pop  year   state debt
one    1.5  2000    Ohio  NaN
two    1.7  2001    Ohio  NaN
three  3.6  2002    Ohio  NaN
four   2.4  2001  Nevada  NaN
five   2.9  2002  Nevada  NaN
