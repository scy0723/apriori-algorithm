# collections 모듈에서 Counter 클래스를 가져옵니다
from collections import Counter

def apriori(transactions, min_support):
    """
    Apriori 알고리즘을 사용하여 빈발 항목 집합을 생성합니다.
    
    매개변수:
    transactions (list): 각 거래를 항목의 리스트로 나타내는 리스트입니다.
    min_support (float): 항목 집합이 빈발으로 간주되기 위한 최소 지지도 임계값입니다.
    
    반환값:
    list: 빈발 항목 집합의 리스트입니다.
    """
    
    # 거래 수를 결정합니다
    num_transactions = len(transactions)
    
    # 최소 지지도 카운트를 결정합니다
    min_support_count = int(min_support * num_transactions)
    
    # 후보 1-항목 집합의 리스트를 생성합니다
    candidate_itemsets = list(set(item) for transaction in transactions for item in transaction)
    
    # 빈발 1-항목 집합의 리스트를 생성합니다
    frequent_itemsets = []
    for itemset in candidate_itemsets:
        itemset_count = sum(1 for transaction in transactions if set(itemset).issubset(set(transaction)))
        if itemset_count >= min_support_count:
            frequent_itemsets.append((tuple(itemset), itemset_count))
    
    # 이전 단계에서 생성된 빈발 항목 집합의 리스트를 사용하여 k-항목 집합을 생성합니다
    k = 2
    while len(frequent_itemsets) > 0:
        # 이전 단계에서 생성된 빈발 항목 집합의 리스트를 사용하여 k-항목 집합의 후보를 생성합니다
        candidate_itemsets = [set(itemset1).union(itemset2) for itemset1 in frequent_itemsets for itemset2 in frequent_itemsets if len(itemset1.union(itemset2)) == k]
        
        # k-항목 집합의 후보를 사용하여 빈발 k-항목 집합의 리스트를 생성합니다
        frequent_itemsets = []
        for itemset in candidate_itemsets:
            itemset_count = sum(1 for transaction in transactions if set(itemset).issubset(set(transaction)))
            if itemset_count >= min_support_count:
                frequent_itemsets.append((tuple(itemset), itemset_count))
        
        # k를 증가시켜 다음 반복을 수행합니다
        k += 1
    
    # 빈발 항목 집합의 리스트를 반환합니다
    return [itemset for itemset, _ in frequent_itemsets]
