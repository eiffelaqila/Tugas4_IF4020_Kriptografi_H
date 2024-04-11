from .script import Script

def main():
  # Secret
  IP = ''
  PORT = ''
  SECRET_TOKEN = ''

  # Run Script
  script = Script(IP, PORT, SECRET_TOKEN)
  script.run()

if __name__ == '__main__':
  main()
