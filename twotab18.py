import tabulate
import re



print('''
<!doctype html>
<style>
 table, th, td {
     border: 1px solid black;
     border-collapse: collapse;
     font-size: 25px;
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
   17: 'Neither',
   18: 'N-S',
}
for bd in range(1,18,2):
    rnd = (bd-1) // 6
    prs = pairdict[rnd]
    ary = [[f'<b/>Board {bd}  &nbsp;&nbsp;&nbsp; {vuldict[bd]} Vul', '', '', '', '', 'XX',
            f'<b/>Board {bd+1}  &nbsp;&nbsp;&nbsp; {vuldict[bd+1]} Vul', '', '', '', '', 'XX',],
           ['<b/>NS', '<b/>EW', '<b/>Contract & Result', '<b/>Score&nbsp;&nbsp;<br/>N-S', '<b/>Score&nbsp;&nbsp;<br/>E-W', '&nbsp;',
            '<b/>NS', '<b/>EW', '<b/>Contract & Result', '<b/>Score&nbsp;&nbsp;<br/>N-S', '<b/>Score&nbsp;&nbsp;<br/>E-W', '&nbsp;',
            ],
           [prs[0], prs[1], '', '', '', '',   prs[0], prs[1], '', '', '', ''],
           [prs[2], prs[3], '', '', '', '',   prs[2], prs[3], '', '', '', ''],
           ]
    tabtxt = tabulate.tabulate(ary, tablefmt='unsafehtml', colalign=(
        'center', 'center','None','None','None', 'None',
        'center', 'center','None','None','None', 'None',))
    tabtxt = re.sub('<td.*?>(<b/>Board.*?</td>).*?XX *?</td>', r'<td colspan="5" style="text-align:center">\1<td></td>', tabtxt);
    print(tabtxt)
    print('<p/>')
    if bd % 10 == 9:
        print('<p style="page-break-after: always;">&nbsp;</p>')
    
print('''
</body></html>
''')
