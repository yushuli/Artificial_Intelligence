1. TIC-TAC-TOE test:
	python tictactoe.py seed tictactoe.txt
	
	(seed could be any number, and the outputfile will be "tictactoe.txt") 

THE OUTPUT SHOWS: (eg. seed = 5)
seed== 5
GAME START!!!
---
--x
---

---
--x
--o

-x-
--x
--o

-x-
--x
o-o

xx-
--x
o-o

xx-
--x
ooo

GAME OVER AND THE WINNER IS: o (o means AI wins, x means RandomPlayer wins)

2. SUDOKU test:
	python sudoku.py suinput.csv suoutput.csv

THE OUTPUT SHOWS: (eg. hard sudoku problem 20 in Google)
row: ['1', '2', '3', '4', '5', '6', '7', '8', '9']
column: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
LOADED SUCCESSFULLY!!!!
ORIGINAL SUDOKU IS:
100070030
830600000
002900608
600004907
090000050
307500004
203009100
000002043
040080009

SOLUTION IS:
169875432
834621795
572943618
625134987
498267351
317598264
283459176
956712843
741386529

THE SOLUTION WILL BE SAVED IN supoutput.csv