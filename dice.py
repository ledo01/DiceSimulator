import re
import random
from colorama import  Fore

PATTERN = re.compile(r'\s*(?P<nb>\d+)d(?P<sides>\d+)\s*(?:(?P<mod>[\+-])\s*(?P<val>\d+))?')
WELCOME_MSG = r"""
 ______     _                   ______    _                        __          _                   
|_   _ `.  (_)                .' ____ \  (_)                      [  |        / |_                 
  | | `. \ __   .---.  .---.  | (___ \_| __   _ .--..--.  __   _   | |  ,--. `| |-' .--.   _ .--.  
  | |  | |[  | / /'`\]/ /__\\  _.____`. [  | [ `.-. .-. |[  | | |  | | `'_\ : | | / .'`\ \[ `/'`\] 
 _| |_.' / | | | \__. | \__., | \____) | | |  | | | | | | | \_/ |, | | // | |,| |,| \__. | | |     
|______.' [___]'.___.' '.__.'  \______.'[___][___||__||__]'.__.'_/[___]\'-;__/\__/ '.__.' [___]    
                                                                                                   

(type help for instuctions)
"""

HELP_MSG = """
Usage: [nb]d[sides](+-)[mod]
  nb        number of dices
  sides     number of sides
  mod       result modifier (+ or -)
  
Example: 
> 1d6 + 1
( 3 ) + 1 = 4
> 3d4
( 1 + 3 + 2 ) = 6

Type q, quit or exit to quit
"""

def read_input(text):
  try:
    m = PATTERN.match(text).groupdict()
    dices = make_dices(int(m['nb']), int(m['sides']))
    mod = m['mod'] or '+'
    val = m['val'] or 0
    val = int(val)

    if mod == '-':
      val *= -1
  except Exception:
    raise ValueError("Can't process the input.")
  return Hand(dices, val)


def make_dices(nb, sides):
  return [Dice(sides) for _ in range(nb)]


class Dice(object):
  def __init__(self, sides):
    self.sides = sides
    self.res = None

  def roll(self):
    self.res = random.randint(1,self.sides)

  def __str__(self):
    p = str(self.res) or 'NA'
    if self.res == 1:
      p = Fore.RED + p
    elif self.res == self.sides:
      p = Fore.GREEN + p

    return p + Fore.RESET
        

class Hand(object):
  def __init__(self, dices, mod):
    self.dices = dices
    self.mod = mod
  
  def roll(self):
    for dice in self.dices:
      dice.roll()

  def __str__(self):
    rolls = [dice.res for dice in self.dices]
    p = f"( {' + '.join(map(str, self.dices))} )"
    if self.mod != 0:
      if self.mod > 0:
        p += f' + {self.mod}'
      else:
        p += f' - {-self.mod}'

    p += f' = {sum(rolls) + self.mod}'

    return p

if __name__ == "__main__":
  print(WELCOME_MSG)
  while True:
    user_input = input('> ')
    if user_input in ('q', 'quit', 'exit'):
      break
    elif user_input in ('h', 'help'):
      print(HELP_MSG)
      continue

    try:
      hand = read_input(user_input)
    except ValueError as e:
      print(e)
    else:
      hand.roll()
      print(hand)