import csv

def writeTokens(tokens):
    c = csv.writer(open("./tokens.csv","w+"),delimiter="#")
    c.writerow(tokens)

def readTokens():
    c = csv.reader(open("./tokens.csv","r"),delimiter="#")
    for row in c:
        if len(row) > 0:
            return row

