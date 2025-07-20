// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Psuedo Code
//  n = RAM[0]
//  sum = 0; 
//  for (n; n==0; n--){
//      sum = sum + n;
//      }

// Put your code here.

@R0
D = M // Set D to RAM[0]

@n
M = D // Set n to D (RAM[0])

@sum
M = 0 // Set sum to 0

(LOOP)
@n
D = M

@STOP
D;JEQ

@R1
D = M // Sets D to RAM[1]

@sum
M = D + M // Adds RAM[1] to sum

@n
D = M
M = D-1 // Sets M to n - 1

@LOOP
0;JMP // Unconditionally jumps to the start of the loop

(STOP)
@sum
D = M
@R2
M = D // Sets RAM[2] to sum

(END)
@END
0;JMP