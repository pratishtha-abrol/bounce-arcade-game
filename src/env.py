import sys, time, os

def animation(counter, length):
    os.system('tput reset')
    stage = counter % (length * 2)
    if stage < length + 1:
        left_spaces = stage
    else:
        left_spaces = length * 2 - 1 - stage
    return '[' + ' ' * left_spaces + '=' + ' ' * (length - left_spaces) + ']\n'

for i in range(100):
    sys.stdout.write('\b\b\b')
    sys.stdout.write(animation(i, 6))
    sys.stdout.flush()
    time.sleep(0.2)