def load_dataset():
    """
    데이터 집합을 불러옵니다.
    """
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

def create_C1(dataset):
    """
    모든 항목의 단일 집합을 생성합니다.
    """
    C1 = []
    for transaction in dataset:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset, C1))

def scan_D(D, Ck, min_support):
    """
    Ck에서 최소 지지도를 충족하는 항목 집합을 생성합니다.
    """
    ss_cnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not can in ss_cnt:
                    ss_cnt[can] = 1
                else:
                    ss_cnt[can] += 1
    num_items = float(len(D))
    ret_list = []
    support_data = {}
    for key in ss_cnt:
        support = ss_cnt[key] / num_items
        if support >= min_support:
            ret_list.insert(0, key)
        support_data[key] = support
    return ret_list, support_data

def apriori_gen(Lk, k):
    """
    Lk에서 Ck+1 생
    """
    ret_list = []
    len_Lk = len(Lk)
    for i in range(len_Lk):
        for j in range(i + 1, len_Lk):
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                ret_list.append(Lk[i] | Lk[j])
    return ret_list

def apriori(dataset, min_support=0.5):
    """
    Apriori 알고리즘을 사용하여 항목 집합을 도출
    """
    C1 = create_C1(dataset)
    D = list(map(set, dataset))
    L1, support_data = scan_D(D, C1, min_support)
    L = [L1]
    k = 2
    while len(L[k - 2]) > 0:
        Ck = apriori_gen(L[k - 2], k)
        Lk, sup_k = scan_D(D, Ck, min_support)
        support_data.update(sup_k)
        L.append(Lk)
        k += 1
    return L, support_data
































































