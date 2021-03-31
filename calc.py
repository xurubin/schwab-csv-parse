import sys

SALE = "Sale"
DEPOSIT = "Deposit"
GIFT = "Gift"
BUY = "Buy"

def splitLine(l):
    result = []
    acc = []
    inQuote = False
    for c in l:
        if c == ',' and not inQuote:
            result.append(''.join(acc))
            acc = []
        elif c == '"':
            inQuote = not inQuote
        else:
            acc.append(c)
    if acc:
        result.append(''.join(acc))
    return result


def toType(s):
    if s == "Deposit":
        return DEPOSIT
    if s == "Gift":
        return GIFT
    if s == "Sale" or s == "Sell":
        return SALE
    if s == "Buy":
        return BUY
    raise "Unknown type: " + s

def parseDollar(s):
    if s[0] == '-':
        return -float(s[1:].lstrip('$').replace(',', ''))
    else:
        return float(s.lstrip('$').replace(',', ''))

def parseDate(text):
    s = text.split('/')
    ## Sale date format is YYYY/MM/DD, Vest date format is MM/DD/YYYY
    ## Convert both to DD/MM/YYYY
    if len(s[0]) == 4:
        return '%s/%s/%s' % (s[2], s[1], s[0])
    else:
        return '%s/%s/%s' % (s[1], s[0], s[2])

def recordToLine(entry):
    return ','.join([entry[0], entry[1], '%.2f' % entry[2] if entry[2] != None else 'None', str(entry[3]), entry[4]])

def main():
    entries = []
    entry = None # [Date, Type, FMV, Amount]
    lc = 0
    for line in open(sys.argv[1]):
        line = splitLine(line.strip())
        if line[0] == "Date" or line[0].startswith("Transaction"):
            continue
        print line
        if line[0]:
            if entry:
                entries.append(entry)
            date = parseDate(line[0])
            etype = toType(line[1])
            tick = line[2]
            amount = float(line[4])
            if etype == SALE:
                fmv = parseDollar(line[7]) / amount
            elif etype == BUY:
                fmv = -parseDollar(line[7]) / amount
            else:
                fmv = None
            entry = [date, etype, fmv, amount, tick]
            lc = 1
            continue
        lc += 1
        if entry[1] == DEPOSIT:
            if lc == 3:
                entry[0] = parseDate(line[3])
                entry[2] = parseDollar(line[4])
            continue
    if entry:
        entries.append(entry)

    #print entries[0]
    print '\n'.join(map(recordToLine, entries[::-1]))
if __name__ == '__main__':
    main()