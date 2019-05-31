import argparse

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

class Stock:
    def __init__(self,timestamp,price,amount):
        self.timestamp=timestamp #need to parse timestamp
        self.price=price
        self.amount=amount
    def __str__(self):
        return str(self.__class__)+": "+str(self.__dict__)

def make_stock(data_string):
    data_array=data_string.split()
    stock=Stock(data_array[0],float(data_array[1]),int(data_array[2]))
    return stock.__dict__

all_stocks=[]
for stats in info_array:
    stock=make_stock(stats)
    print stock
    all_stocks.append(stock)

print all_stocks



