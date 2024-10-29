from re import sub
from random import randint
from functools import reduce

###### Util ######

regex = {
  "dice_roll": r'\d*d\d+'
}

def roll(sides, number=1):
  def sumRolls(total, _): return total + randint(1, sides)

  return reduce(sumRolls, range(number), 0)

def regexToRollResult(match):
  num, sides = match.group().split("d")

  return str(roll(int(sides), 1 if num == '' else int(num)))

def rollDiceString(diceString):
  subbedString = sub(regex["dice_roll"], regexToRollResult, diceString)
  
  return eval(subbedString)

###### Testing ######

def testDiceString(diceString):
  print()

  print(f"Input: {diceString}")
  print(f"Roll: {rollDiceString(diceString)}")

  total, quantity = 0, 100000
  for _ in range(quantity):
    total += int(rollDiceString(diceString))
  print(f"Ao{quantity}: {total/quantity}\n")

###### Main ######

testDiceString("d100")
