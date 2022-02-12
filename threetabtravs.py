import tabulate
import re
import argparse


print('''
<!doctype html>
<style>
 table, th, td {
     border: 1px solid black;
     border-collapse: collapse;
     font-size: 16px;
     font-weight: bold;
 }
 body {
     
 }
</style>

<html><body>
''')

pairdict = {0: [3,2,5,4,6,1],
            1: [4,2,5,3,6,1],
            2: [1,5,4,3,6,2],
            3: [1,4,5,3,6,2],
            4: [2,1,5,4,6,3],
            5: [1,4,2,5,6,3],
            6: [1,5,3,2,6,4],
            7: [2,5,3,1,6,4],
            8: [2,1,4,3,6,5],
            9: [3,1,4,2,6,5],
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
parser.add_argument('--boards', type=int, default=20, help='total number of boards')
args = parser.parse_args()
boardsPerRound = args.boards// 10;

def getPairDict(bd):
    rnd = (bd-1) // boardsPerRound
    return pairdict[rnd % 10]
    

# two boards per iteration
rangeLimit = args.boards if args.boards % 2 == 0 else args.boards+1
for bd in range(1, rangeLimit, 2):
    prsa = getPairDict(bd)
    prsb = getPairDict(bd+1)
    resultHead='<span style="font-size:12px">Contract/Result</span>'
    smallSpan='<span style="font-size:12px">'
    ary = [[f'Board {bd}  &nbsp;&nbsp;&nbsp; {getVul(bd)} Vul', '', '', '', '', 'XX',
            f'Board {bd+1}  &nbsp;&nbsp;&nbsp; {getVul(bd+1)} Vul', '', '', '', '', 'XX',],
           ['NS', 'EW', resultHead, f'&nbsp;&nbsp;&nbsp;N-S&nbsp;&nbsp;&nbsp;', f'&nbsp;&nbsp;E-W&nbsp;', '&nbsp;',
            'NS', 'EW', resultHead, f'&nbsp;&nbsp;&nbsp;N-S&nbsp;&nbsp;&nbsp;', f'&nbsp;&nbsp;E-W&nbsp;', '&nbsp;',
            ],
           [prsa[0], prsa[1], '', '', '', '',   prsb[0], prsb[1], '', '', '', ''],
           [prsa[2], prsa[3], '', '', '', '',   prsb[2], prsb[3], '', '', '', ''],
           [prsa[4], prsa[5], '', '', '', '',   prsb[4], prsb[5], '', '', '', ''],
           ]
    tabtxt = tabulate.tabulate(ary, tablefmt='unsafehtml', colalign=(
        'center', 'center','None','None','None', 'None',
        'center', 'center','None','None','None', 'None',))
    tabtxt = re.sub('<td.*?>(Board.*?</td>).*?XX *?</td>', r'<td colspan="5" style="text-align:center">\1<td></td>', tabtxt);
    print(tabtxt)
    print('<p/>')
    # add page break at end of first page
    if bd % 10 == 9:
        print('<p style="page-break-after: always;">&nbsp;</p>')
    
print('''
</body></html>
''')
