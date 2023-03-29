# Data Science Assignment #1 
## Apriori algorithm
컴퓨터소프트웨어학부 2019055078 신채영

## Environment
- Language: `Python 3.9.13`
- OS: `macOS Vertura 13.2.1`

## Apriori Algorithm
Apriori 알고리즘은 데이터 마이닝 분야에서 사용되는 알고리즘으로 빈번하게 발생하는 항목 집합을 찾아내는 데 사용된다.
### Support
-   probability (or, frequency) that a transaction contains X.
    - Minimum support: a threshold that decides whether X is a frequent pattern or not, based on its support
### Confidence
-   conditional probability that a transaction having X also contains Y
    - Minimum confidence: it is also a threshold
## Run
- `python apriori.py min_sup input.txt output.txt` 의 형태로 실행한다.
- ex. `python apriori.py 5 input.txt output.txt`

## Code Description
