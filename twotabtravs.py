import tabulate
import re
import argparse


print('''
<!doctype html>
<style>
 table, th, td {
     border: 1px solid black;
     border-collapse: collapse;
     font-size: 20px;
     font-weight: bold;
 }
 body {
     
 }
</style>

<html><body>
''')

pairdict = {0: [2,3,4,1],
            1: [3,1,4,2],
            2: [1,2,4,3]
            }

vuldict = {
    1: 'Neither',
    2: 'N-S',
    3: 'E-W',
    4: 'Both',
    5: 'N-S',
    6: 'E-W',
    7: 'Both',
    8: 'Neither',
    9: 'E-W',
   10: 'Both',
   11: 'Neither',
   12: 'N-S',
   13: 'Both',
   14: 'Neither',
   15: 'N-S',
   16: 'E-W',
}

def getVul(bd):
    return vuldict[((bd-1)%16)+1]

parser = argparse.ArgumentParser('2-table dup travellers file creator')
parser.add_argument('--boards', type=int, default=18, help='total number of boards')
args = parser.parse_args()
boardsPerRound = args.boards// 3;

def getPairDict(bd):
    rnd = (bd-1) // boardsPerRound
    return pairdict[rnd % 3]
    

# two boards per iteration
rangeLimit = args.boards if args.boards % 2 == 0 else args.boards+1
for bd in range(1, rangeLimit, 2):
    prsa = getPairDict(bd)
    prsb = getPairDict(bd+1)
    ary = [[f'<b/>Board {bd}  &nbsp;&nbsp;&nbsp; {getVul(bd)} Vul', '', '', '', '', 'XX',
            f'<b/>Board {bd+1}  &nbsp;&nbsp;&nbsp; {getVul(bd+1)} Vul', '', '', '', '', 'XX',],
           ['<b/>NS', '<b/>EW', '<b/>Contract & Result', '<b/>Score&nbsp;&nbsp;<br/>N-S', '<b/>Score&nbsp;&nbsp;<br/>E-W', '&nbsp;',
            '<b/>NS', '<b/>EW', '<b/>Contract & Result', '<b/>Score&nbsp;&nbsp;<br/>N-S', '<b/>Score&nbsp;&nbsp;<br/>E-W', '&nbsp;',
            ],
           [prsa[0], prsa[1], '', '', '', '',   prsb[0], prsb[1], '', '', '', ''],
           [prsa[2], prsa[3], '', '', '', '',   prsb[2], prsb[3], '', '', '', ''],
           ]
    tabtxt = tabulate.tabulate(ary, tablefmt='unsafehtml', colalign=(
        'center', 'center','None','None','None', 'None',
        'center', 'center','None','None','None', 'None',))
    tabtxt = re.sub('<td.*?>(<b/>Board.*?</td>).*?XX *?</td>', r'<td colspan="5" style="text-align:center">\1<td></td>', tabtxt);
    print(tabtxt)
    print('<p/>')
    # add page break at end of first page
    if bd % 12 == 11:
        print('<p style="page-break-after: always;">&nbsp;</p>')
    
print('''
</body></html>
''')
