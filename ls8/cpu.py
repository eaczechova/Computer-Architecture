"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101


SP = 7 # stack pointer

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[SP] = 0xF4
        self.pc = 0
        self.halted = False


    def ram_read(self, address): # address could be replaces with MAR
        return self.ram[address]

    def ram_write(self, address, val):
        self.ram[address] = val

    def load(self, filename):
        """Load a program into memory."""
        # returns array of arguments passed via commend line
        if len(sys.argv) != 2:
            print('incorrect number of arguments')
            sys.exit(1)

        address = 0
        try: 
            with open(filename) as f:
                
                for line in f:
                    line = line.split("#")
                    num = line[0].strip() # removes trailing whitespace
                    if num == "":
                        continue
                    else:
                        try:
                            val = int(num, 2)
                            self.ram_write( address, val )
                            print("works here", self.ram)
                        except:
                            print( 'Could not convert string to integer' )
                    address += 1 
        except:
            print("Error with file")
            sys.exit(1)
      
        # For now, we've just hardcoded a program:

#         program = [
#             # From print8.ls8
#             0b10000010, # LDI R0,8
#             0b00000000,
#             0b00001000,
#             0b01000111, # PRN R0
#             0b00000000,
#             0b00000001, # HLT
# 2        ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while not self.halted:
            instruction_to_execute = self.ram_read(self.pc)

            if instruction_to_execute == PRN:
                index = self.ram[self.pc + 1]
                self.pc += 2
            elif instruction_to_execute == LDI:
                index = self.ram[self.pc + 1]
                val = self.ram[self.pc + 2]
                self.reg[index] = val
                self.pc += 3
            elif instruction_to_execute == HLT:
                self.halted = True
                self.pc += 1
            elif instruction_to_execute == MUL:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.alu("MUL", reg_a, reg_b)
                self.pc += 3
            elif instruction_to_execute == PUSH: # decrease the stack pointer and write the element at the top of the stack
                self.reg[SP] -= 1 # stack starts at very high memory address and goes downwards
                address = self.reg[SP] # get address SP point to
                reg_num = self.ram_read(self.pc + 1)
                value = self.reg[reg_num]
                self.ram_write(address, value)
                self.pc += 2
            elif instruction_to_execute == POP: # pop element from the top of the stack
                value = self.ram_read(self.reg[SP])
                reg_num = self.ram_read(self.pc + 1)
                self.reg[reg_num] = value
                self.reg[SP] += 1
                self.pc += 2


          
