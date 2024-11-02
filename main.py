from sys import argv
from parser import *

###### Testing ######
# Shows the input, result of a single roll, and a high AoX result
def testDiceString(diceString):
  dice = parse(diceString)

  print(f"\nInput: {diceString}")
  print(f"Roll: {dice.eval()}")

  total, quantity = 0, 100000
  for _ in range(quantity):
    total += dice.eval()
  
  print(f"Ao{quantity}: {total/quantity}\n")

###### Main ######
if __name__ == '__main__':
  testDiceString(argv[1])
