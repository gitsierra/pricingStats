import argparse
import re

parser = argparse.ArgumentParser()

parser.add_argument('file', type=argparse.FileType('r'),
                    help='File with Data')

parser.add_argument('-t1', action='store_const', dest='timestamp1',
                    const='t1',
                    help='1st Timestamp')

parser.add_argument('-t2', action='store_const', dest='timestamp2',
                    const='t2',
                    help='2nd Timestamp')


results = parser.parse_args()

info_array=results.file.readlines()

print 'timestamp1   =', results.timestamp1
print 'timestamp2 =', results.timestamp2

class Timestamp:
    def __init__(self,year,month,day,hour,minute,second):
        self.year=year
        self.month=month
        self.day=day
        self.hour=hour
        self.minute=minute
        self.second=second

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


def make_timestamp(timestamp):
    print timestamp
    time_array=re.split('-|T|:|Z',timestamp)#should make sure values in file are valid
    ts=Timestamp(int(time_array[0]),
                 int(time_array[1]),
                 int(time_array[2]),
                 int(time_array[3]),
                 int(time_array[4]),
                 int(time_array[5])#assume all values are UTC time AKA end in Z, also are values over 60 valid?
                 )
    return ts.__dict__


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

print all_stocks



