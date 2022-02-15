import tabulate
import re
import argparse

######################################
# Script to generate simple travellers
# for a few duplicateseatings
#
# Prints to stdout
# 
######################################

class TravsBase:
    def generate(self):
        self.boardsPerRound = self.numBoards// self.numRounds;
        self.genHtmlIntro();
        self.genTravellersTables();
        self.genHtmlClose();
        
    def genHtmlIntro(self):
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

    def genHtmlClose(self):
        print('''
        </body></html>
        ''')

    def getPairNumAry(self, bd):
        rnd = (bd-1) // self.boardsPerRound
        return self.getPairDict()[rnd % self.numRounds]
    

    def getVulString(self,bd):
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
        return vuldict[((bd-1)%16)+1]

    def genBoardInfoOneBoard(self, bd):
        return [f'<b/>Board {bd}  &nbsp;&nbsp;&nbsp; {self.getVulString(bd)} Vul', '', '', '', '', 'XX']
    
    def genBoardInfoLine(self, bd):
        return self.genBoardInfoOneBoard(bd) + self.genBoardInfoOneBoard(bd+1)

    def genBoardColHdrOneBoard(self):
        resultHead='<span style="font-size:12px">Contract/Result</span>'
        return ['NS', 'EW', resultHead, f'&nbsp;&nbsp;&nbsp;N-S&nbsp;&nbsp;&nbsp;', f'&nbsp;&nbsp;E-W&nbsp;', '&nbsp;']

    def genBoardColHdrLine(self):
        return self.genBoardColHdrOneBoard() + self.genBoardColHdrOneBoard()

    def genTableLineOneBoard(self, bd, tabnum):
        pairNumAry = self.getPairNumAry(bd)
        return [pairNumAry[tabnum*2], pairNumAry[tabnum*2 + 1], '', '', '', '']

    def genTableLine(self, bd, tabnum):
        return self.genTableLineOneBoard(bd, tabnum) + self.genTableLineOneBoard(bd+1, tabnum)
        
    def genTravellersTables(self):
        # we always print two boards horizontally per iteration
        rangeLimit = self.numBoards if self.numBoards % 2 == 0 else self.numBoards+1
        for bd in range(1, rangeLimit, 2):
            ary = []
            ary.append(self.genBoardInfoLine(bd))
            ary.append(self.genBoardColHdrLine())
            # now the traveller lines (one for each table)
            for tabnum in range(self.numTables):
                ary.append(self.genTableLine(bd, tabnum))

            # now use tabulate to create the html table
            tabtxt = tabulate.tabulate(ary, tablefmt='unsafehtml', colalign=(
                'center', 'center','None','None','None', 'None',
                'center', 'center','None','None','None', 'None',))
            tabtxt = re.sub('<td.*?>(<b/>Board.*?</td>).*?XX *?</td>', r'<td colspan="5" style="text-align:center">\1<td></td>', tabtxt);
            print(tabtxt)
            print('<p/>')
            # add page break at end of first page
            if (bd+1) % self.pageBreakBoardCount == 0:
                print('<p style="page-break-after: always;">&nbsp;</p>')
        # end of for bd in range loop
                

class TwoTablesTravs(TravsBase):
    def __init__(self, args):
        self.numTables = 2
        self.numRounds = 3
        self.numBoards = args.boards 
        # eventually this could be generated from numTables since each table takes a "line"
        self.pageBreakBoardCount = 12
       
    def getPairDict(self):
        return {0: [2,3,4,1],
                1: [3,1,4,2],
                2: [1,2,4,3]
                }

class ThreeTablesTravs(TravsBase):
    def __init__(self, args):
        self.numTables = 3
        self.numRounds = 10
        self.numBoards = 20
        # eventually this could be generated from numTables since each table takes a "line"
        self.pageBreakBoardCount = 10

       
    def getPairDict(self):
        return {0: [3,2,5,4,6,1],
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

    
parser = argparse.ArgumentParser('Duplicate Travellers HTML File Creator')
parser.add_argument('--tables', type=int, default=2, help='number of tables')
parser.add_argument('--boards', type=int, default=18, help='total number of boards for 2-table game')
args = parser.parse_args()
if args.tables == 2:
    travGen = TwoTablesTravs(args)
else:
    travGen = ThreeTablesTravs(args)
    
travGen.generate()
