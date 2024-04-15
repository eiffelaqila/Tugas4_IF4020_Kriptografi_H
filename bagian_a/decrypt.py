from Crypto.Util.number import long_to_bytes, isPrime, inverse 
from sympy import factorint

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

    def iroot(self, k: int, num: int) -> int:
        # Kth root of num
        u, s = num, num+1
        while u < s:
            s = u
            t = (k-1) * s + num // pow(s, k-1)
            u = t // k
        return s

    def decrypt(self, version: str, n: int, e: int, c: int) -> str:
        try:
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
                p = self.iroot(2, n)
                if (p**2 != n):
                    raise ValueError('N bukan merupakan perkalian 2 bilangan prima yang sama (kuadratik)')

                totient = (p-1) * p
                d = pow(e, -1, totient)
                # raise NotImplementedError('Not implemented yet')
            elif version == 'C':
                # Notes:
                # Kelemahan C:  ...
                raise NotImplementedError('Not implemented yet')
            elif version == 'D':
                # Notes:
                # Kelemahan D:  Menggunakan e yang nilainya kecil (e = 3)
                # Serangan:     m = Akar pangkat e dari c
                s = self.iroot(e, c)
                p = long_to_bytes(s)
                return p.decode('utf-8')
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
        except Exception as e:
            print('Error: %s' % e)
            return None

def main():
    # TEST VERSI A
    test_cases = [
        {
            'version': 'A',
            'n': 24608047198635995402759555417135638116230885914219090661026244438702695517393286387957541330779356729850709750466261456173818729749148700607497275726292202843476572083673389289028156823871869689946749065547150226453459484460801072840900626613804320365733372832688732246279878345203351816401637413716762319499973701362633513934474506594752644782352272074904805776741593321278222940683116488444340494024906080820105173091040797368423296704444971612685527211975911010585462701412008573071193544476052611683007620306678206046675415035783035686357832960175636631929627140497120774123420665962084667389835638989909966275351,
            'e': 65537,
            'enc': 1143208513127837758508260764604580434204728783121339879418160563473323646733244964322963357963398465955648055122197126412837478469761710950184179474471189847478299601285906759007294140676389688051550722193440135277675103243435782745002902656784795319956338105123160147161397799736731473295969277865449745556893625469050570244844087051642117139703846396901612459801677311575957648275088850747292204233685127451294499256611871344543891512985779789102997520362369446326498322969288352064604893243262500072552028670465878900156366352763097811721554205036469268359088139563205658285870180946645018516123072512715231070902,
            'ans': 'KRIPTOGRAFIITB{4251}'
        },
        {
            'version': 'B',
            'n': 18637281413015647501381093492900003202098150082583794551127705031312360200408254257451916500912601455270007335601427933996128115742919020392176891664869492424621612695881340798328819532494741759411775635438368641003438825070415072364308124545646113226330572796185757691090590555849376093061752164459448286799802847065932625226087892401897683460929373251001716106480392464431858996999328921723422601450801029606616920112189259410863954752566442934456491335050285053441739357021856395314878246234188602434757138677052320562781759635049383352909983464758964771040842652057523933696180048863757902983460234542457175716569,
            'e': 65537,
            'enc': 13075159036221907268106856478084217506564059765052774327039057963375436360540285700969847386669553304557314701759932452718200664145343648023006305156171506240896366675246772236519544382341553630917415045968660919194604042301114331739083340256850609257222056970435505623262151042439799909403703113664594123774711600859293049580905325481003844497764897986365577282620555511244841620639729007621690749758021336862142865793258790428746792595375860989532486286073438873574586580200059486529724918230447543308887799975748882752419552840213150356433294240369545931642458448477495954816515315275945030129002969967383305584275,
            'ans': 'KRIPTOGRAFIITB{8085}'
        },  
        {
            'version': 'D',
            'n': 19266294211839939317335625510104357579950717913155791428253813195465293777014487781132683007351986350263613173625422836997382417002849619541732609447005917159724847804572052294476138094759133593884004292323918278821874109644070056064585142366217434975044276533141012272522165948604023072543411023952940878836304095612434566717791607382941015146709147260563002774341444911189920289582995178161337548104270154116402901219064857145901962891493283690478446446171336018876632050952546171260371088791560822948151435495295002851467997432006724272587601125153446205172160288212679105392439528761698598378411445262985140229611,
            'e': 3,
            'enc': 79512189580798597445445851463057563991520739833012546069299054508870983956457615097428068741707352278393796298083619535441194332595336312460133,
            'ans': 'KRIPTOGRAFIITB{1022}'
        },  
        {
            'version': 'E',
            'n': 139568680348872402220544658003474337295401810096538027361331040352684677610127534679897459737571691497374574967696924081173319105030371525129033835885476677479028774764647867295242000518272583662692299575167263745432490951268105787600020111251924898082349479640604952030633363423805194817315223857745674602909,
            'e': 65537,
            'enc': 60555035649064190342536420078279026237689182897165210196021253869537920421059953337208808823242535585672025074387210066173359790828011611262336222093404631335297120627996953193513813775305329924161315332776502848814732657976012460179706436365493472955962771859902389952705397336456213969048414680147896824265,
            'ans': 'KRIPTOGRAFIITB{380}'
        }    
    ]

    rsa_attack = RSA_Attack()
    for tc in test_cases:
        print('----------------------------------------')
        print(f"paket_soal = {tc['version']}")
        print(f"n = {tc['n']}")
        print(f"e = {tc['e']}")
        print(f"c = {tc['enc']}")
        plainteks = rsa_attack.decrypt(tc['version'], tc['n'], tc['e'], tc['enc'])
        print(f'Plainteks: {plainteks}\n')
        print('Hasil: ' + 'Benar' if plainteks == tc['ans'] else 'Salah' + '\n')

if __name__ == '__main__':
    main()