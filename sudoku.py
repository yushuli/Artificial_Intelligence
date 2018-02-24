#!/usr/bin/env/ python2.7
import csv
import sys
import copy

class CSP:
    def __init__(self):
        self.variable = []
        self.domain = {}
        self.constraint = {}
        self.column = ['A','B','C','D','E','F','G','H','I']
        self.row = ['1','2','3','4','5','6','7','8','9']
        self.value = []
        self.conflict = []

    #initialize the fields
    def loadSudoku(self, filename):
        print "row:", self.row
        print "column:", self.column
        lineID = 0
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',', quotechar='|')
            #read value of variables
            for line in reader:
                for j in range(9):
                    #vb is the variable represented by location
                    vb = self.row[lineID] + self.column[j]
                    self.variable.append(vb)
                    if int(line[j]) != 0:
                        self.domain[vb] = [int(line[j])]
                    else:
                        self.domain[vb] = [1,2,3,4,5,6,7,8,9]
                lineID += 1
        if lineID == 9:
            print "LOADED SUCCESSFULLY!!!!"
        #initialize the constraints
        for v in self.variable:
            if v not in self.constraint:
                self.constraint[v] = []
            neighbor = self.getNeighbor(v)
            for nei in neighbor:
                self.constraint[v].append(nei)
        self.setUpConflictRegion()

    #get neighbors of the current variable
    def getNeighbor(self, v):
        r = self.row.index(v[0])
        c = self.column.index(v[1])
        neighbor = []
        #find neighbors in same row or column
        for i in range(0, 9):
            rowNeighbor = v[0] + self.column[i]
            columnNeighbor = self.row[i] + v[1]
            if i != c:
                neighbor.append(rowNeighbor)
            if i != r:
                neighbor.append(columnNeighbor)
        #find neighbors in same 3*3 block
        a = (r / 3) * 3
        b = (c / 3) * 3
        for i in range(0, 3):
            for j in range(0, 3):
                vTmp = self.row[a + i] + self.column[b + j]
                if vTmp != v and vTmp not in neighbor:
                    neighbor.append(vTmp)
        return neighbor

    #print the result
    def printCSP(self):
        #print original sudoku
        for i in range(0,9):
            line = ""
            row = self.row[i]
            for j in range(0, 9):
                col = self.column[j]
                if len(self.domain[row + col]) > 1:
                    line += str(0)
                else:
                    line += str(self.domain[row + col][0])
            print line

    #set up conflict region
    def setUpConflictRegion(self):
        #add each of the 9 rows in the conflict region
        for row in self.row:
            rowConflict = []
            for col in self.column:
                rowConflict.append(row + col)
            self.conflict.append(rowConflict)
        #add each of the 9 columns in the conflict region
        for col in self.column:
            colConflict = []
            for row in self.row:
                colConflict.append(row + col)
            self.conflict.append(colConflict)
        #add each of the 9 blocks in the conflict region
        for row in [0, 3, 6]:
            for col in [0, 3, 6]:
                blockConflict = []
                for i in range(0, 3):
                    for j in range(0, 3):
                        blockConflict.append(self.row[row + i] + self.column[col + j])
                self.conflict.append(blockConflict)

    #this is for writing solution into csv file
    def writeSolution(self, filename):
        self.value = []
        for i in range(0,9):
            line = []
            row = self.row[i]
            for j in range(0, 9):
                col = self.column[j]
                if len(self.domain[row + col]) > 1:
                    line.append(str(0))
                else:
                    line.append(str(self.domain[row + col][0]))
            self.value.append(line)
        with open(filename, "wb") as f:
            writer = csv.writer(f)
            writer.writerows(self.value)

#remove inconsistent values
def removeInconsistent(csp, v1, v2):
    remove = False
    for i in csp.domain[v1]:
        if len(csp.domain[v2]) == 1 and i == csp.domain[v2][0]:
            csp.domain[v1].remove(i)
            remove = True
    return remove

#this is the AC3 algorithm
def AC3(csp):
    queue = []
    for i in csp.variable:
        for j in csp.constraint[i]:
            queue.append((i, j))
    while queue:
        i, j = queue.pop(0)
        if removeInconsistent(csp, i, j):
            for k in csp.constraint[i]:
                queue.append((k, i))

#forward searching
def forward(csp):
    mark = True
    while mark:
        AC3(csp)
        mark = False
        #csp.column = ['A','B','C','D','E','F','G','H','I']
        #csp.row = ['1','2','3','4','5','6','7','8','9']
        for row in csp.conflict:
            domain = [1,2,3,4,5,6,7,8,9]
            for ele in row:
                if len(csp.domain[ele]) == 1:
                    if csp.domain[ele][0] in domain:
                        domain.remove(csp.domain[ele][0])
            for d in domain:
                if sum(csp.domain[ele].count(d) for ele in row) == 1:
                    csp.domain[[ele for ele in row if csp.domain[ele].count(d) > 0][0]] = [d]
                    mark = True

#DFS search
def DFS(csp):
    stk = []
    stk.append(copy.deepcopy(csp))
    while stk:
        node = stk.pop()
        forward(node)
        flag = True
        for d in node.domain:
            if len(node.domain[d]) != 1:
                flag = False
        if flag:
            return node
        flag2 = True
        for d in node.domain:
            if len(node.domain[d]) == 0:
                flag2 = False
        if flag2:
            Key = [k for k in node.domain if len(node.domain[k]) > 1][0] 
            for guess in node.domain[Key]: 
                successor = copy.deepcopy(node)
                successor.domain[Key] = [guess]
                stk.append(successor)

def main(input, output):
    csp = CSP()
    csp.loadSudoku(input)
    print "ORIGINAL SUDOKU IS:"
    csp.printCSP()
    ans = DFS(csp)
    print ""
    print "SOLUTION IS:"
    ans.printCSP()
    ans.writeSolution(output)

main(sys.argv[1], sys.argv[2])
