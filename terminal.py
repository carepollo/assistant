import subprocess
import pexpect

class Terminal:

    def __init__(self):
        self.process = None

    def start(self, executable_file):
        # self.process = subprocess.Popen(
        #     executable_file,
        #     stdin=subprocess.PIPE,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE
        # )
        self.process = pexpect.spawn(executable_file)

    def read(self):
        # self.process.stdout.readline().decode("utf-8")
        
        return self.process.logfile

    def write(self, message):
        # self.process.stdin.write(f"{message.strip()}\n".encode("utf-8"))
        # self.process.stdin.flush()
        self.process.write(message)

    def terminate(self):
        # self.process.stdin.close()
        # self.process.terminate()
        # self.process.wait(timeout=0.2)
        self.process.kill()
        self.process.wait()
        self.process = None
