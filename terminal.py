import pexpect

class Terminal:

    def __init__(self):
        self.process = None

    def start(self, executable_file):
        self.process = pexpect.spawn(executable_file, encoding="utf-8")

    def read(self):
        return self.process.readline()

    def write(self, message):
        self.process.write(message)

    def terminate(self):
        self.process.kill()
        self.process.wait()
        self.process = None
