import sys

class Wiener_Attack(object):
  def __init__(self) -> None:
    sys.setrecursionlimit(100000)

  def rational_to_contfrac(self, x: int, y: int) -> list[int]:
    a = x//y
    if a * y == x:
      return [a]
    else:
      pquotients = self.rational_to_contfrac(y, x - (a * y))
      pquotients.insert(0, a)
      return pquotients

  def convergents_from_contfrac(self, frac: list[int]) -> list[tuple[int, int]]:    
    convs = []
    for i in range(len(frac)):
      convs.append(self.contfrac_to_rational(frac[0:i]))
    return convs

  def contfrac_to_rational(self, frac: list[int]) -> tuple[int, int]:
    if len(frac) == 0:
      return (0,1)
    elif len(frac) == 1:
      return (frac[0], 1)
    else:
      remainder = frac[1:len(frac)]
      (num, denom) = self.contfrac_to_rational(remainder)
      return (frac[0] * num + denom, num)

  def is_perfect_square(self, n: int) -> int:
    h = n & 0xF; 
    if h > 9:
      return -1 

    if ( h != 2 and h != 3 and h != 5 and h != 6 and h != 7 and h != 8 ):
      t = self.isqrt(n)
      if t*t == n:
        return t
      else:
        return -1

    return -1

  def isqrt(self, n: int) -> int:
    if n == 0:
      return 0
    a, b = divmod(n.bit_length(), 2)
    x = 2**(a+b)
    while True:
      y = (x + n//x)//2
      if y >= x:
        return x
      x = y

  def solve(self, N: int, e: int):
    frac = self.rational_to_contfrac(e, N)
    self.convergents = self.convergents_from_contfrac(frac)

    for (k,d) in self.convergents:
      if k!=0 and (e*d-1)%k == 0:
        phi = (e*d-1)//k
        s = N - phi + 1
        discr = s*s - 4*N
        if(discr>=0):
          t = self.is_perfect_square(discr)
          if t!=-1 and (s+t)%2==0:
            return d
    return None