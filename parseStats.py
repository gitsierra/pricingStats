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
print info_array