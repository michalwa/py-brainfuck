import sys


class BrainfuckVM:
    """ Implements a virtual machine used to execute brainfuck code. """

    def __init__(self, memory_size: int = 32):
        """ Initializes a brainfuck VM with the given memory size (number of cells) """
        self.__memory = [0] * memory_size
        self.__pointer = 0

    def execute(self, program: str) -> None:
        """ Executes the given program. """
        ip = 0
        jumps = []

        while ip < len(program):
            i = program[ip]

            if i == '>':
                self.__pointer += 1
            elif i == '<':
                self.__pointer -= 1
            elif i == '+':
                self.__increment()
            elif i == '-':
                self.__decrement()
            elif i == '.':
                self.__print_char()
            elif i == ',':
                self.__read_char()
            elif i == '[':
                if self.__get() != 0:
                    jumps.append(ip)
                else:
                    loops = 1
                    initial_ip = ip
                    while loops > 0:
                        ip += 1
                        if ip >= len(program):
                            raise ValueError('Unclosed parenthesis at %i.' % initial_ip)
                        elif program[ip] == ']':
                            loops -= 1
                        elif program[ip] == '[':
                            loops += 1
            elif i == ']':
                if len(jumps) <= 0:
                    raise ValueError('Unexpected closing parenthesis at %i.' % ip)
                elif self.__get() > 0:
                    ip = jumps[len(jumps) - 1]
                else:
                    jumps.pop()

            ip += 1

    def __check_pointer(self) -> None:
        """ Checks whether the memory pointer is in the valid range. """
        if self.__pointer < 0 or self.__pointer >= len(self.__memory):
            raise ValueError('Memory pointer outside valid range: %i.' % self.__pointer)

    def __get(self) -> int:
        """ Returns the value of the current cell. """
        self.__check_pointer()
        return self.__memory[self.__pointer]

    def __set(self, value: int) -> None:
        """ Sets the current cell to the given value. """
        self.__check_pointer()
        self.__memory[self.__pointer] = value

    def __increment(self) -> None:
        """ Increments the current cell ensuring 8-bit int overflow. """
        self.__check_pointer()
        self.__memory[self.__pointer] += 1
        if self.__memory[self.__pointer] >= 256:
            self.__memory[self.__pointer] -= 256

    def __decrement(self) -> None:
        """ Decrements the current cell ensuring 8-bit int overflow. """
        self.__check_pointer()
        self.__memory[self.__pointer] -= 1
        if self.__memory[self.__pointer] < 0:
            self.__memory[self.__pointer] += 256

    def __print_char(self) -> None:
        """ Prints out the ASCII character corresponding to the value of the current cell. """
        print(chr(self.__get()), end='')

    def __read_char(self) -> None:
        """ Reads a character from the standard input and stores its ASCII code in the current cell. """
        self.__set(ord(input()[0]))

    def print(self) -> None:
        """ Prints out the current state of the VM. """
        print(' '.join(map(str, self.__memory)))
        print('pointer = %i' % self.__pointer)


vm = BrainfuckVM()

if __name__ == "__main__":
    argv = sys.argv[1:]
    if len(argv) >= 1:
        if argv[0] == '-f' and len(argv) >= 2:
            vm.execute(open(argv[1]).read())
        else:
            vm.execute(argv[0])
