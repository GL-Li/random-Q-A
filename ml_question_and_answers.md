## Scikit-Learn

### Feature extraction

**Q**: How to vectorize dictionaries?

**A**: Using `DictVectorizer()` to convert a list of dictionaries into a numeric array.

```python
from sklearn.feature_extraction import DictVectorizer

dic1 = {'x':4, 'y':"a", 'z':True, 'u':"a"}
dic2 = {'x':2, 'y':"b", 'z':False, 'u':"a"}
dic3 = {'x':9, 'y':"a", 'z':True, 'u':"c"}
dic = [dic1, dic2, dic3]
dict_vect = DictVectorizer(sparse=False)
dict_vect.fit_transform(dic)

# array([[1., 0., 4., 1., 0., 1.],
#        [1., 0., 2., 0., 1., 0.],
#        [0., 1., 9., 1., 0., 1.]])

"""
The result is an array, each individual dic corresponding to one row.

The dictionaries have 4 keys, 'x', 'y', 'z', 'u'. In the output, they
are reordered alphabetically.

The first key 'u' has two unique values so it takes the first two columns in the array.
The second key 'x' is numeric, taking only one column.
The third key 'y' also has two unique values, taking next two columns.
The fourth key 'z' is logical, taking the last one column.

The dict_vect is trained with dic and can be used to transform new dictionaries. If a key value does not appear in training sets, such as "aaa" below, the column for 'y':'a' and 'y':'b' simply assigned 0
"""
dic4 = {'x':99, 'y':"aaa", 'z':True, 'u':"a"}
dict_vect.transform([dic4])
# array([[ 1.,  0., 99.,  0.,  0.,  1.]])
```

