import subprocess

class Script(object):
  def __init__(self, ip, port, token):
    self.IP = ip
    self.PORT = port
    self.SECRET_TOKEN = token

  def extract_values(self, input_str):
    paket_soal = input_str.split('paket_soal =')[1].split('\n')[0]
    n = int(input_str.split('n = ')[1].split('\n')[0])
    e = int(input_str.split('e = ')[1].split('\n')[0])
    c = int(input_str.split('c = ')[1].split('\n')[0])
    p = input_str.split('p = ')[1].split('\n')[0]

    return paket_soal, n, e, c, p

  # TODO: Hapus "p"; Hanya untuk testing script
  def calculate_answer(self, paket_soal, n, e, c, p):
    return p

  def is_stop_readline(self, lines):
    return 'n =' in lines and 'e =' in lines and 'c =' in lines and 'p =' in lines and 'Jawaban =' in lines

  def is_stop_loop(self, line):
    return ':((((((' in line or 'Error' in line or 'Uhuyyyy' in line or 'Tetap semangat dan jangan putus asa!' in line

  def run(self):
    result = ''
    end = False

    server_proc = subprocess.Popen(
      # ['nc', self.IP, self.PORT],
      ['python', '-m', 'bagian_a.test'], 
      stdin=subprocess.PIPE, 
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      universal_newlines=True)

    response = server_proc.stdout.readline()
    print(response, end="") # Opsional

    print(self.SECRET_TOKEN)
    server_proc.stdin.write(self.SECRET_TOKEN + '\n')
    server_proc.stdin.flush()

    while not end:
      output = ''
      while not self.is_stop_readline(output):
        line = server_proc.stdout.readline()
        print(line, end="") # Opsional

        if self.is_stop_loop(line):
          result = line
          end = True
          break
        output += line

      if end:
        break

      # TODO: Hapus "p"; Hanya untuk testing script
      paket_soal, n, e, c, p = self.extract_values(output)

      answer = self.calculate_answer(paket_soal, n, e, c, p)
      print(answer) # Opsional

      server_proc.stdin.write(answer + '\n')
      server_proc.stdin.flush()

      response = server_proc.stdout.readline()
      print(response, end="") # Opsional

    # Close the connection
    server_proc.stdin.close()
    server_proc.stdout.close()
    server_proc.stderr.close()

    print(f"RESULT: {result}")
