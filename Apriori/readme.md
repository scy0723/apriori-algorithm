# Assignment #1
## Apriori algorithm
컴퓨터소프트웨어학부 2019055078 신채영
***
## Environment
- Language: `Python 3.9.13`
- OS: `macOS Vertura 13.2.1`

***

## Apriori Algorithm
Apriori 알고리즘은 데이터 마이닝 분야에서 사용되는 알고리즘으로 빈번하게 발생하는 항목 집합을 찾아내는 데 사용된다.
### Support(지지도)
- 전체 거래 중 항목 집합이 포함된 거래의 비율
- Minimum Support(최소 지지도)데이터 집합에서 빈발 항목 집합으로 판단하기 위한 최소한의 지지도를 나타내는 임계값
### Confidence(신뢰도)
- 항목 A가 포함된 거래 중에서 항목 B가 포함된 거래의 비율
- Minimum Confidence(최소 신뢰도): 항목 A가 포함된 거래 중에서 항목 B가 포함된 거래의 비율이 최소한의 값 이상이어야 해당 항목 집합이 신뢰도를 갖는 것으로 판단한다.

***

## Run
- `python apriori.py min_sup input.txt output.txt` 의 형태로 실행한다.
- ex. `python apriori.py 5 input.txt output.txt`
### - input.txt

### - output.txt
    printed 1066 lines of transactions
## Code Description

## main
argv에서 input file, output file 그리고 minimum support를 입력받는다.

    min_sup = float(sys.argv[1])
    input = sys.argv[2]
    output = sys.argv[3]

    read(input)

frequent items를 담을 배열을 선언하고 k=1인 Ck, Lk를 구한다.

    frequent = []
    frequent_sup = defaultdict(int)
    C1_sup = C1(datasets)

    L1, L1_sup = generate_frequent(C1_sup)

    Lk = L1
    Lk_sup = L1_sup
    k = 1

k = k인 Ck, Lk를 구한다. k를 증가해가며 실행하다가 더 이상 빈발 그룹을 만들 수 없을 때 종료한다.

    while True:
        frequent.append(Lk)
        frequent_sup.update(Lk_sup)

        Ck, Ck_sup = ck(Lk, Lk_sup, k)

        Lk, Lk_sup = generate_frequent(Ck_sup)

        k += 1
        
        if not Lk or not Ck:
            break

구한 모든 frequent items를 파일에 출력한다.
    write(output, frequent)