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
    print(size)
    min_sup = size * (min_sup/100)
    f.close

def C1(db):
    C1_sup = defaultdict(int)
    for items in db:
        for item in items:
            C1_sup[tuple([item])] += 1
    return C1_sup

def ck(Lk, Lk_sup, k):
    ## initialize k-candidate itemset
    Ck = []
    Ck_sup = defaultdict(int)

    for i in range(len(Lk)):
        for j in range(i+1, len(Lk)):
            L_sub1 = Lk[i][:-1]
            L_sub2 = Lk[j][:-1]

            if L_sub1 == L_sub2:

                ## self_joining in sorted
                if Lk[i][-1] < Lk[j][-1]:
                    candidate = Lk[i] + tuple([Lk[j][-1]])
                else:
                    candidate = Lk[j] + tuple([Lk[i][-1]])
                ## pruning
                Ck, Ck_sup = prune(Ck, Ck_sup, candidate, Lk_sup, k)

    return Ck, Ck_sup

def prune(Ck, Ck_sup, candidate, Lk_sup, k):
    for i in range(k+1):
        subset = candidate[:i] + candidate[i+1:]
        sup = Lk_sup[subset]
        
        ## delete if candidate's support doesn't satify minimum support
        if sup < min_sup:
            del(candidate)
            return Ck, Ck_sup

    ## add candidate if satisfy minimum support
    Ck.append(candidate)
    Ck_sup[candidate] = get_sup_cnt(candidate)

    return Ck, Ck_sup

def get_sup_cnt(candidate):
    cnt = 0
    candidate = set(candidate)

    for trx in datasets:
        if candidate.issubset(trx):
            cnt += 1

    return cnt

def generate_frequent(Ck_sup):
    ## initialize k-frequent itemset
    Lk = []
    Lk_sup = defaultdict(int)

    for itemset, sup in Ck_sup.items():
        if sup >= min_sup:
            Lk.append(itemset)
            Lk_sup[itemset] = sup

    return Lk, Lk_sup

def write(output_file, frequent):
    of = open(output_file, 'w')
    for k in range(len(frequent)):

        for itemset in frequent[k]:
            ## get subsets of itemset
            length = len(itemset)
            subsets = []

            for i in range(1 << length):
                subset = set(itemset[j] for j in range(i) if (i & (1 << j)))
                if subset != set() and subset != set(itemset):
                    subsets.append(subset)

            ## calculate support and confidence of subset_1 and subset_2
            ## and make data with in conditions
            for subset_1 in subsets:
                subset_2 = set(itemset) - subset_1

                ## make tuple and sort union(subset_1, subset_2) and subset_1
                sorted_union = tuple(sorted(subset_1.union(subset_2)))
                sorted_subset_1 = tuple(sorted(subset_1))
                
                ## get support from each itemset
                sup_union = frequent_sup[sorted_union]
                sup_subset_1 = frequent_sup[sorted_subset_1]

                ## calculate support and confidence of subset_1 and subset_2
                sup = format(sup_union / len(datasets)*100, ".2f")
                conf = format(sup_union / sup_subset_1*100, ".2f")

                ## convert itemset list to string
                str_subset_1 = ",".join(str(s) for s in sorted(subset_1))
                str_subset_2 = ",".join(str(s) for s in sorted(subset_2))

                ## make data with in conditions
                output = "{" + str_subset_1 + "}" + "\t" + "{" + str_subset_2 + "}"
                output += "\t" + str(sup) + "\t" + str(conf) + "\n"

                of.write(output)
    of.close()


if __name__ == "__main__":

    ## argv
    min_sup = float(sys.argv[1])
    input = sys.argv[2]
    output = sys.argv[3]

    read(input)

    ## frequent itemsets
    frequent = []
    frequent_sup = defaultdict(int)

    ## c1
    C1_sup = C1(datasets)

    ## generate 1-frequent itemset
    L1, L1_sup = generate_frequent(C1_sup)

    ## k-frequent itemset
    Lk = L1
    Lk_sup = L1_sup
    k = 1

    ## generate k-candidate and k-frequent itemset
    while True:
        ## add k-frequent to frequent itemset list
        frequent.append(Lk)
        frequent_sup.update(Lk_sup)

        ## generate k-candidate from (k-1)-frequent
        Ck, Ck_sup = ck(Lk, Lk_sup, k)

        ## generate k-frequent from k-candidate 
        Lk, Lk_sup = generate_frequent(Ck_sup)

        k += 1
        ## stop generating when no more k-candidate or k-frequent
        if not Lk or not Ck:
            break

    ## write file
    write(output, frequent)
