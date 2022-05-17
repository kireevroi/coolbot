#Handling queries from txt file
#Copyright kireevroi

def readQuery(filename, query_list):
    try:
        f = open(filename, mode = "r", encoding="utf-8")
        for x in f:
            query_list.append(x)
        for i in range(len(query_list)):
            query_list[i] = query_list[i].strip('\n')
            query_list[i] = query_list[i].split(' ### ')
    except Exception as e:
        print(e)
