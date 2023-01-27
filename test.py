from terminal import Terminal

term = Terminal()

def startCommand():
    term.start(["/home/halgorithmics/Projects/esolang/esolang"])
    print(term.read(), end="")
    print(term.read(), end="")
    print(term.read(), end="")

def runCommand(instruction):
    term.write(instruction)
    print(term.read(), end="")

def stopCommand():
    term.terminate()

startCommand()
runCommand("let a = fn(a) { a + 1 }")
runCommand("a(1)")
