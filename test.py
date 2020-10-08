
list1 = [250, 325,100,-75,0]
# arrange assending order.
# biggest
# 2nd largest

def arrange(list1):
    list2 = []
    minimum_value = min(*list1)
    for i in range(len(list1) - 1):
        minimum_value = min(*list1)
        list2.append(minimum_value)
        print(list1)
        print(len(list1))
        if len(list1) == 1:
            pass
        else:
            list1.remove(minimum_value)
    print(list2)



arrange(list1)
