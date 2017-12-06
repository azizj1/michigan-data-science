# Assignment 1

In this assignment, you'll be working with messy medical data and using regex to extract relevant infromation from the data. 

Each line of the `dates.txt` file corresponds to a medical note. Each note has a date that needs to be extracted, but each date is encoded in one of many formats.

The goal of this assignment is to correctly identify all of the different date variants encoded in this dataset and to properly normalize and sort the dates. 

Here is a list of some of the variants you might encounter in this dataset:
* 04/20/2009; 04/20/09; 4/20/09; 4/3/09
* Mar-20-2009; Mar 20, 2009; March 20, 2009;  Mar. 20, 2009; Mar 20 2009;
* 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009
* Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009
* Feb 2009; Sep 2009; Oct 2010
* 6/2008; 12/2009
* 2009; 2010

Once you have extracted these date patterns from the text, the next step is to sort them in ascending chronological order accoring to the following rules:
* Assume all dates in xx/xx/xx format are mm/dd/yy
* Assume all dates where year is encoded in only two digits are years from the 1900's (e.g. 1/5/89 is January 5th, 1989)
* If the day is missing (e.g. 9/2009), assume it is the first day of the month (e.g. September 1, 2009).
* If the month is missing (e.g. 2010), assume it is the first of January of that year (e.g. January 1, 2010).
* Watch out for potential typos as this is a raw, real-life derived dataset.

With these rules in mind, find the correct date in each note and return a pandas Series in chronological order of the original Series' indices.

For example if the original series was this:

    0    1999
    1    2010
    2    1978
    3    2015
    4    1985

Your function should return this:

    0    2
    1    4
    2    0
    3    1
    4    3

Your score will be calculated using [Kendall's tau](https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient), a correlation measure for ordinal data.

*This function should return a Series of length 500 and dtype int.*


```python
import pandas as pd
import re
doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)
print(type(df))
df.head(10)
```

    0         03/25/93 Total time of visit (in minutes):\n
    1                       6/18/85 Primary Care Doctor:\n
    2    sshe plans to move as of 7/8/71 In-Home Servic...
    3                7 on 9/27/75 Audit C Score Current:\n
    4    2/6/96 sleep studyPain Treatment Pain Level (N...
    5                    .Per 7/06/79 Movement D/O note:\n
    6    4, 5/18/78 Patient's thoughts about current su...
    7    10/24/89 CPT Code: 90801 - Psychiatric Diagnos...
    8                         3/7/86 SOS-10 Total Score:\n
    9             (4/10/71)Score-1Audit C Score Current:\n
    dtype: object


```python
def date_sorter():
    return # code here
```

                  0    1    2    3     4
    0      03/25/93  03/  NaN  25/    93
    1       6/18/85   6/  NaN  18/    85
    2        7/8/71   7/  NaN   8/    71
    3       9/27/75   9/  NaN  27/    75
    4        2/6/96   2/  NaN   6/    96
    5       7/06/79   7/  NaN  06/    79
    6       5/18/78   5/  NaN  18/    78
    7      10/24/89  10/  NaN  24/    89
    8        3/7/86   3/  NaN   7/    86
    9       4/10/71   4/  NaN  10/    71
    10      5/11/85   5/  NaN  11/    85
    11      4/09/75   4/  NaN  09/    75
    12      8/01/98   8/  NaN  01/    98
    13      1/26/72   1/  NaN  26/    72
    14    5/24/1990   5/  NaN  24/  1990
    15    1/25/2011   1/  NaN  25/  2011
    16      4/12/82   4/  NaN  12/    82
    17   10/13/1976  10/  NaN  13/  1976
    18      4/24/98   4/  NaN  24/    98
    19           59  NaN  NaN  NaN    59
    20      7/21/98   7/  NaN  21/    98
    21     10/21/79  10/  NaN  21/    79
    22      3/03/90   3/  NaN  03/    90
    23      2/11/76   2/  NaN  11/    76
    24   07/25/1984  07/  NaN  25/  1984
    25      4-13-82   4-  NaN  13-    82
    26      9/22/89   9/  NaN  22/    89
    27      9/02/76   9/  NaN  02/    76
    28      9/12/71   9/  NaN  12/    71
    29     10/24/86  10/  NaN  24/    86
    ..          ...  ...  ...  ...   ...
    470        1983  NaN  NaN  NaN  1983
    471        1999  NaN  NaN  NaN  1999
    472        2010  NaN  NaN  NaN  2010
    473        1975  NaN  NaN  NaN  1975
    474        1972  NaN  NaN  NaN  1972
    475        2015  NaN  NaN  NaN  2015
    476        1989  NaN  NaN  NaN  1989
    477          14  NaN  NaN  NaN    14
    478        1993  NaN  NaN  NaN  1993
    479        1996  NaN  NaN  NaN  1996
    480        2013  NaN  NaN  NaN  2013
    481        1974  NaN  NaN  NaN  1974
    482        1990  NaN  NaN  NaN  1990
    483        1995  NaN  NaN  NaN  1995
    484        2004  NaN  NaN  NaN  2004
    485        1987  NaN  NaN  NaN  1987
    486        1973  NaN  NaN  NaN  1973
    487        1992  NaN  NaN  NaN  1992
    488        1977  NaN  NaN  NaN  1977
    489          35  NaN  NaN  NaN    35
    490       12 96  12   NaN  NaN    96
    491        2009  NaN  NaN  NaN  2009
    492        1986  NaN  NaN  NaN  1986
    493        1978  NaN  NaN  NaN  1978
    494        2002  NaN  NaN  NaN  2002
    495        1979  NaN  NaN  NaN  1979
    496        2006  NaN  NaN  NaN  2006
    497        2008  NaN  NaN  NaN  2008
    498        2005  NaN  NaN  NaN  2005
    499        1980  NaN  NaN  NaN  1980
    
    [500 rows x 5 columns]
    0
