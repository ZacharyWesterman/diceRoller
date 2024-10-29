import re
from random import randint

# 2x3d4+5

def roll(sides, number=1):
  total = 0
  for _ in range(number):
    total += randint(1, sides)
  return total

def replaceWithRoll(match):
  num, sides = match.group().split("d")

  num = 1 if num == '' else int(num)
  
  return str(roll(int(sides), num))

def rollDiceString(diceString):
  kDn = r'\d*d\d+'
  result = re.sub(kDn, replaceWithRoll, diceString)
  return eval(result)

# diceString = "2d6+1d4"
diceString = "d100"
print(diceString)
print(rollDiceString(diceString))

print("Ao100: ", end='', flush=True)
total = 0
for _ in range(100):
  total += int(rollDiceString(diceString))
print(total/100)
