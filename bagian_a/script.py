import subprocess
from bagian_a.decrypt import RSA_Attack

class Script(object):
  def __init__(self, ip, port, token):
    self.IP = ip
    self.PORT = port
    self.SECRET_TOKEN = token
    self.rsa_attack = RSA_Attack()

  def extract_values(self, input_str):
    paket_soal = input_str.split('paket_soal = ')[1].split('\n')[0]
    n = int(input_str.split('n = ')[1].split('\n')[0])
    e = int(input_str.split('e = ')[1].split('\n')[0])
    c = int(input_str.split('c = ')[1].split('\n')[0])

    return paket_soal, n, e, c

  def calculate_answer(self, paket_soal, n, e, c):
    return self.rsa_attack.decrypt(paket_soal, n, e, c)

  def is_stop_readline(self, lines):
    return 'n =' in lines and 'e =' in lines and 'c =' in lines

  def is_stop_loop(self, line):
    return ':((((((' in line or 'Error' in line or 'Uhuyyyy' in line or 'Tetap semangat dan jangan putus asa!' in line

  def run(self):
    result = ''
    end = False

    server_proc = subprocess.Popen(
      ['ncat', self.IP, self.PORT],
      # ['python', '-m', 'bagian_a.test'], 
      stdin=subprocess.PIPE, 
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      universal_newlines=True)

    response = server_proc.stdout.readline()
    print(response, end="")

    print(self.SECRET_TOKEN)
    server_proc.stdin.write(self.SECRET_TOKEN) # server_proc.stdin.write(self.SECRET_TOKEN + '\n')
    server_proc.stdin.flush()

    while not end:
      output = ''
      while not self.is_stop_readline(output):
        line = server_proc.stdout.readline()
        if ('Jawaban = ' in line):
          response = line.split('Jawaban = ')[1]
          print(response, end="")
          continue

        print(line, end="")

        if self.is_stop_loop(line):
          result = line.split('\n')[0]
          end = True
          break

        output += line

      if end:
        break

      paket_soal, n, e, c = self.extract_values(output)

      answer = self.calculate_answer(paket_soal, n, e, c)
      print("Jawaban = ")
      print(answer)

      server_proc.stdin.write(answer) # server_proc.stdin.write(answer + '\n')
      server_proc.stdin.flush()

    # Close the connection
    server_proc.stdin.close()
    server_proc.stdout.close()
    server_proc.stderr.close()

    print('\n==========================================')
    if 'Uhuyyyy' in result:
      flag = result.split('Uhuyyyy ')[1].split('\n')[0]
      print(f"Flag: {flag}")
    else:
      print(f"Terdapat kesalahan")
