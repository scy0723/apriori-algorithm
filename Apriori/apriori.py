import sys
from collections import defaultdict

datasets = []
min_sup = int()

def read(input_file):
    global datasets, min_sup

    f = open(input_file, 'r')
    lines = f.readlines()
    for line in lines:
        items = line.split()
        items = set(items)
        datasets.append(items)

    size = len(datasets)
    min_sup = size * (min_sup/100)
    f.close()

def c1(db):
    supC1 = defaultdict(int)
    for items in db:
        for item in items:
            supC1[tuple([item])] += 1
    return supC1

def CktoLk(supCk):
    Lk = []
    supLk = defaultdict(int)

    for itemset, sup in supCk.items():
        if sup >= min_sup:
            Lk.append(itemset)
            supLk[itemset] = sup

    return Lk, supLk

def ck(Lk, supLk, k):
    Ck = []
    supCk = defaultdict(int)

    for i in range(len(Lk)):
        for j in range(i+1, len(Lk)):
            a = Lk[i][:-1]
            b = Lk[j][:-1]
            if a == b:
                if Lk[i][-1] < Lk[j][-1]:
                    candi_itemsets = Lk[i] + tuple([Lk[j][-1]])
                else:
                    candi_itemsets = Lk[j] + tuple([Lk[i][-1]])
                Ck, supCk = pruning(Ck, supCk, supLk, k, candi_itemsets,)
    return Ck, supCk

def pruning(Ck, supCk, supLk, k, candi_itemsets):
    for i in range(k+1):
        subset = candi_itemsets[:i] + candi_itemsets[i+1:]
        sup = supLk[subset]
        
        if sup < min_sup:
            del(candi_itemsets)
            return Ck, supCk
        
    Ck.append(candi_itemsets)
    supCk[candi_itemsets] = cal_sup(candi_itemsets)

    return Ck, supCk

def cal_sup(candidate):
    cnt = 0
    candidate = set(candidate)
    for i in datasets:
        if candidate.issubset(i):
            cnt += 1
    return cnt

def write(output_file, freq_sets):
    f = open(output_file, 'w')
    for k in range(len(freq_sets)):

        for itemset in freq_sets[k]:
            length = len(itemset)
            subsets = []

            for i in range(1 << length):
                s = set(itemset[j] for j in range(i) if (i & (1 << j)))
                if s != set() and s != set(itemset):
                    subsets.append(s)

            ##s1, s2의 confidence와 support를 구한다.
            for s1 in subsets:
                s2 = set(itemset) - s1

                ## S1 U S2 와 S1을 정렬하여 튜플을 만들고 support를 구한다.
                sorted_12 = tuple(sorted(s1.union(s2)))
                sorted_1 = tuple(sorted(s1))
                sup_12 = support[sorted_12]
                sup_1 = support[sorted_1]

                ##소수점 두 자리까지의 support, confidence 값을 계산한다.
                sup = format(sup_12 / len(datasets) * 100, ".2f")
                conf = format(sup_12 / sup_1 * 100, ".2f")

                ## 출력 문자열 만들기
                string1 = ",".join(str(s) for s in sorted(s1))
                string2 = ",".join(str(s) for s in sorted(s2))
                string = "{" + string1 + "}" 
                string += "\t{" + string2 + "}"
                string += "\t" + str(sup) + "\t" + str(conf) + "\n"

                f.write(string)
    f.close()


if __name__ == "__main__":
    min_sup = float(sys.argv[1])
    input = sys.argv[2]
    output = sys.argv[3]
    read(input)

    freq_itemsets = []
    support = defaultdict(int)

    k = 1
    supC1 = c1(datasets)
    Lk, supLk = CktoLk(supC1)

    while True:
        freq_itemsets.append(Lk)
        support.update(supLk)
        Ck, supCk = ck(Lk, supLk, k)
        Lk, supLk = CktoLk(supCk)
        
        k += 1
        if not Lk or not Ck:
            break

    write(output, freq_itemsets)

