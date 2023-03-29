def load():
    f = open("input.txt", 'r')
    datasets=[]
    while True:
        line = f.readline()
        if not line:
            break
        datasets.append(line)
    f.close()
    print(datasets[i])
    
'''
def makeC1(dataset):

def apriori(dataset, ms=0.05)

'''

def main():
    load()


if __name__ == "__main__":
    main()
