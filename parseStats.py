import argparse
import re
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('file', type=argparse.FileType('r'),
                    help='File with Data')

parser.add_argument('-t1', action='store', dest='timestamp1',
                    help='1st Timestamp')

parser.add_argument('-t2', action='store', dest='timestamp2',
                    help='2nd Timestamp')


results = parser.parse_args()

info_array=results.file.readlines()

class Timestamp:
    def __init__(self,year,month,day,hour,minute,second):
        self.year=year

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


def make_timestamp(timestamp):
    time_array=re.split('-|T|:|Z',timestamp)#should make sure values in file are valid
    ts=time_array[0]+time_array[1]+time_array[2]+time_array[3]+time_array[4]+time_array[5]#assume all values are UTC time AKA end in Z, also are values over 60 valid?
    instts=int(ts)
    return instts


class Stock:
    def __init__(self,timestamp,price,amount):
        self.timestamp=make_timestamp(timestamp)
        self.price=price
        self.amount=amount
    def __str__(self):
        return str(self.__class__)+": "+str(self.__dict__)

def make_stock(data_string):
    data_array=data_string.split()
    stock=Stock(
                data_array[0],
                float(data_array[1]),
                int(data_array[2])
                )
    return stock.__dict__

all_stocks=[]
for stats in info_array:
    stock=make_stock(stats)
    all_stocks.append(stock)
all_stocks.sort(key=lambda x:x['timestamp'])

def binary_search(arr, l, r, x):

    while l <= r:
        mid = l + (r - l) / 2;

        if arr[mid]['timestamp'] == x:
            return mid

        elif arr[mid]['timestamp'] < x:
            l = mid + 1

        else:
            r = mid - 1
    if arr[mid]['timestamp'] > x:
        return mid-1,mid
    elif arr[mid]['timestamp'] < x:
        return mid+1,mid

#print 'timestamp1 =', results.timestamp1
#print 'timestamp2 =', results.timestamp2

if results.timestamp1 is None and results.timestamp2 is None:
    print "No Timestamps were given"

elif results.timestamp1 is not None and results.timestamp2 is None:
    it1=make_timestamp(results.timestamp1)
    index_found=binary_search(all_stocks,0,len(all_stocks)-1,it1)
    if type(index_found)==int:
        print "Price is:",all_stocks[index_found]['price']
    elif index_found[0]==-1 or index_found[0]==len(all_stocks):
        print "Price is:",all_stocks[index_found[1]]['price']
    else:
        stock1price=all_stocks[index_found[0]]['price']
        stock1amount=all_stocks[index_found[0]]['amount']

        stock2price=all_stocks[index_found[1]]['price']
        stock2amount = all_stocks[index_found[1]]['amount']

        print "Price is:",(stock1price*stock1amount+stock2price*stock2amount)/(stock1amount+stock2amount)

elif results.timestamp2 is not None and results.timestamp1 is None: #flipped timestamps
    print"Only timestamp2 was given"

elif results.timestamp1 is not None and results.timestamp2 is not None:
    it1 = make_timestamp(results.timestamp1)
    it2 = make_timestamp(results.timestamp2)
    index_found1 = binary_search(all_stocks, 0, len(all_stocks) - 1, it1)
    index_found2 = binary_search(all_stocks, 0, len(all_stocks) - 1, it2)
    if type(index_found1)!=int:
        index_found1=index_found1[0]
        if index_found1==-1:
            index_found1=0
        elif index_found1==len(all_stocks):
            index_found1=index_found1-1
    if type(index_found2)!=int:
        index_found2=index_found2[0]
        if index_found2 == -1:
            index_found2 = 0
        elif index_found2==len(all_stocks):
            index_found2=index_found2-1

    median_search=[]
    flattened_list=[]
    all_prices=[]
    total_price=0
    total_units=0
    std=0

    for x in range(index_found1,index_found2+1):
        all_prices.append(all_stocks[x]['price'])
        total_price=total_price+(all_stocks[x]['price']*all_stocks[x]['amount'])
        total_units=total_units+all_stocks[x]['amount']
        median_search.append(np.ones(all_stocks[x]['amount'])*all_stocks[x]['price'])

    for x in median_search:
        for y in x:
            flattened_list.append(y)

    average_price=total_price/total_units

    for x in range(index_found1,index_found2+1):
        std=std+(all_stocks[x]['amount']*(all_stocks[x]['price']-average_price)**2)


    std_deviation=(std/total_units)**(0.5)

    all_prices.sort()
    print "Max price is:",all_prices[-1]
    print "Min price is:", all_prices[0]
    print "Average Price is:",average_price
    print "Standard Deviation is:",std_deviation
    print "Median is:",np.median(flattened_list)

