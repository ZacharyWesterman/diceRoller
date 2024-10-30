from re import sub
from random import randint
from functools import reduce
from sys import argv

###### Util ######
diceRollRegex = r'\d*d\d+'

# Rolls [number]d[sides], like 2d6, 5d4, or even d100 
def roll(sides, number=1):
  sumRolls = lambda total, _: total + randint(1, sides)
  return reduce(sumRolls, range(number), 0)

# Converts the regex of kdn into the result of the roll
def regexToRollResult(match):
  num, sides = match.group().split("d")
  return str(roll(int(sides), int(num) if num else 1))

# Takes an input dice string and returns the result of the relevant dice and math
def rollDiceString(diceString):
  subbedString = sub(diceRollRegex, regexToRollResult, diceString)
  return eval(subbedString)

###### Testing ######
# Shows the input, result of a single roll, and a high AoX result
def testDiceString(diceString):
  print(f"\nInput: {diceString}")
  print(f"Roll: {rollDiceString(diceString)}")

  total, quantity = 0, 100000
  for _ in range(quantity):
    total += int(rollDiceString(diceString))
  
  print(f"Ao{quantity}: {total/quantity}\n")

###### Main ######
if __name__ == '__main__':
  testDiceString(argv[1])
