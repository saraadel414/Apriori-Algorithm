import collections
import itertools
import pandas as pd
from pandas import read_excel
from collections import Counter
from operator import itemgetter


def support_count_1(allitems, min_support_count):
    min_count1 = {}
    count1 = Counter(x for s in allitems for x in set(s))
    for i, x in count1.items():
        if x >= min_support_count:
            min_count1[i] = x

    return count1, min_count1


def support_count_2(min_count1, allitems, min_support_count):
    min_count1 = sorted(list(min_count1.keys()))  # sort the list
    min_count1 = list(itertools.combinations(min_count1, 2))  # combine each item with another item "set of 2 items"
    count2 = {}
    min_count2 = {}
    for l1 in min_count1:
        newcount = 0  # the count of each set
        for l2 in allitems:
            if set(l1) <= set(l2):  # check if the items exist at the same row
                newcount += 1
        count2[l1] = newcount
    for i, x in count2.items():
        if x >= min_support_count:
            min_count2[i] = x

    return count2, min_count2


def support_count_3(min_count2, allitems, min_support_count):
    min_count2 = list(min_count2.keys())
    min_count2 = sorted(list(set([item for t in min_count2 for item in t])))  # sort the list
    min_count2 = list(itertools.combinations(min_count2, 3))  # combine each item with another item "set of 3 items"
    count3 = {}
    min_count3 = {}

    for l1 in min_count2:
        newcount = 0  # the count of each set
        for l2 in allitems:
            if set(l1) <= set(l2):  # check if the items exist at the same row
                newcount += 1
        count3[l1] = newcount
    for i, x in count3.items():  # min support
        if x >= min_support_count:
            min_count3[i] = x

    return count3, min_count3


def confidence2(min_count2, min_count1, min_confidence):
    for y2, x2 in min_count2.items():
        l = list(y2)
        for y1 in y2:
            for y, x in min_count1.items():
                if y1 == y:
                    confidence = (x2 / x) * 100
                    if confidence >= min_confidence:
                        if y1 == l[0]:
                            print("{}->{} = ".format(l[0], l[1]), confidence)
                        if y1 == l[1]:
                            print("{}->{} = ".format(l[1], l[0]), confidence)


def confidence3(min_count3, min_count2, min_count1, min_confidence):
    sets = []  # list of 2 items from min_count3
    for iter1 in list(min_count3.keys()):
        subsets = list(itertools.combinations(iter1, 2))
        sets.append(subsets)

    list_l3 = list(min_count3.keys())  # all 3 items without count
    for i in range(len(list_l3)):
      for y3, x3 in min_count3.items():
        l = list(y3)
        for iter1 in sets[i]:
          for y2, x2 in min_count2.items():
            if iter1 == y2:
             sup2 = x2
             for y1 in y2:
                for y, x in min_count1.items():
                    if y1 == y:
                        confidence = (x3 / sup2) * 100
                        confidence2 = (x3 / x) * 100

                        if confidence >= min_confidence:
                           if y2 == l[0:1]:
                               print("{}->{} = ".format(l[0:1], l[2]), confidence)
                           if y2 == l[1:2]:
                               print("{}->{} = ".format(l[1:2], l[0]), confidence)
                           s = [0, 2]
                           if y2 == itemgetter(*s)(l):
                               print("{}->{} = ".format(itemgetter(*s)(l), l[1]), confidence)

                        if confidence2 >= min_confidence:
                           if y1 == l[0]:
                              print("{}->{} = ".format(l[0], l[1:2]), confidence2)
                           if y1 == l[2]:
                              print("{}->{} = ".format(l[2], l[0:1]), confidence2)
                           s = [0, 2]
                           if y1 == l[1]:
                              print("{}->{} = ".format(l[1], itemgetter(*s)(l)), confidence2)


if __name__ == '__main__':

    transactions = pd.read_excel('CoffeeShopTransactions.xlsx', header=None)
    allitems = []
    for i in range(len(transactions)):
        allitems.append([str(transactions.values[i, j]) for j in range(3, 6)])

    min_support = float(input("Enter minimum support in decimal:"))
    min_confidence = float(input("Enter minimum confidence in percent:"))
    min_support_count = int(min_support * len(transactions))

    count1, min_count1 = support_count_1(allitems, min_support_count)
    count2, min_count2 = support_count_2(min_count1, allitems, min_support_count)
    count3, min_count3 = support_count_3(min_count2, allitems, min_support_count)

    print("Strong association rules are:")
    confidence3(min_count3, min_count2, min_count1, min_confidence)

    if len(min_count3) == 0:
        print("****************************** There Are NO Frequent Triplets ************************")
        confidence2(min_count2, min_count1, min_confidence)
