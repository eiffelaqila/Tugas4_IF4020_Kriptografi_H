from Crypto.Util.number import long_to_bytes, isPrime, inverse 
from sympy import factorint, sqrt

class RSA_Attack(object):
    def __init__(self):
        pass

    def factorize(self, n: int) -> tuple[int, int]:
        # Factorize the modulus n
        factors = factorint(n)
        prime_factors = [p for p in factors if isPrime(p)]
        if (len(prime_factors) == 1 and n == pow(prime_factors[0], 2)):
            # Meaning: n = p^2 (p is prime)
            return prime_factors[0], prime_factors[0]
        elif (len(prime_factors) == 1 and n == (prime_factors[0] * 1)):
            # Meaning: n = 1*p (p is prime)
            return 1, prime_factors[0]
        elif (len(prime_factors) == 2 and n == (prime_factors[0] * prime_factors[1])):
            # Meaning: n = p*q (p and q are prime)
            return prime_factors[0], prime_factors[1]
        return None, None

    def decrypt(self, version: str, n: int, e: int, c: int) -> str:
        p = None
        if version == 'A':
            # Notes:
            # Kelemahan A:  Menggunakan modulus n yang dihasilkan dari
            #               perkalian dua buah prima yang berdekatan.
            # Serangan:     Factorization attack.
            p, q = self.factorize(n)
            if (p == None):
                raise ValueError('N bukan merupakan perkalian 2 bilangan prima')

            totient = (p-1) * (q-1)
            d = pow(e, -1, totient)
        elif version == 'B':
            # Notes:
            # Kelemahan B:  Menggunakan modulus n yang dihasilkan dari
            #               perkalian dua prima yang sama (kuadratik).
            raise NotImplementedError('Not implemented yet')
        elif version == 'C':
            # Notes:
            # Kelemahan C:  ...
            raise NotImplementedError('Not implemented yet')
        elif version == 'D':
            # Notes:
            # Kelemahan D:  ...
            raise NotImplementedError('Not implemented yet')
        elif version == 'E':
            # Notes:
            # Kelemahan E:  Menggunakan modulus n yang dihasilkan dari
            #               satu buah prima.
            totient = (n-1)
            d = pow(e, -1, totient)
        else:
            raise ValueError('Versi paket soal tidak tersedia')

        p = pow(c, d, n)
        p = long_to_bytes(p)
        return p.decode('utf-8')

def main():
    v = 'A'
    n = 24608047198635995402759555417135638116230885914219090661026244438702695517393286387957541330779356729850709750466261456173818729749148700607497275726292202843476572083673389289028156823871869689946749065547150226453459484460801072840900626613804320365733372832688732246279878345203351816401637413716762319499973701362633513934474506594752644782352272074904805776741593321278222940683116488444340494024906080820105173091040797368423296704444971612685527211975911010585462701412008573071193544476052611683007620306678206046675415035783035686357832960175636631929627140497120774123420665962084667389835638989909966275351
    e = 65537
    c = 1143208513127837758508260764604580434204728783121339879418160563473323646733244964322963357963398465955648055122197126412837478469761710950184179474471189847478299601285906759007294140676389688051550722193440135277675103243435782745002902656784795319956338105123160147161397799736731473295969277865449745556893625469050570244844087051642117139703846396901612459801677311575957648275088850747292204233685127451294499256611871344543891512985779789102997520362369446326498322969288352064604893243262500072552028670465878900156366352763097811721554205036469268359088139563205658285870180946645018516123072512715231070902

    rsa_attack = RSA_Attack()

    plainteks = rsa_attack.decrypt(v, n, e, c)

    print(f'Plainteks: {plainteks}')

if __name__ == '__main__':
    main()