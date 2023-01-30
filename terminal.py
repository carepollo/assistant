import pexpect

class Terminal:
    '''
    a server-side terminal emulator to 
    interact with terminal programs from python scripts
    '''

    process: pexpect.spawn
    '''the terminal program to be executed'''

    def __init__(self):
        self.process = None

    def start(self, executable_file: str):
        '''
        run a command that returns an executable TUI program, returns the output, 
        (if present) of the initialization of program
        '''
        self.process = pexpect.spawn(executable_file, encoding="utf-8", maxread=1)
        return self.read()

    def read(self):
        '''return a string with all lines of output of last executed command'''
        return self.process.read_nonblocking(999999999)

    def write(self, message):
        '''send value to program through keyboard input'''
        self.process.sendline(message)

    def terminate(self):
        '''kill process/program and restart property value to None'''
        self.process.kill()
        self.process.wait()
        self.process = None

    def run_command(self, command: str):
        '''
        run an instruction for the executed program 
        and get the returned result as string
        '''
        self.write(command)
        return self.read()

# output closes prematurely when a pexpect subprocess returns variable outputs
