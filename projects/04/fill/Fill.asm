// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(LOOPKBD) // Keyboard Input Loop
@KBD
D = M // Sets D to KBD input
@BLKSCRNCHANGE
D;JNE // If D > 0 then goto BLKSCRNCHANGE
@WHTSCRNCHANGE
D;JEQ // If D == 0 then goto WHTSCRNCHANGE



(BLKSCRNCHANGE) // Change screen to black - functionality

@i
M = 0 // Sets i to 0
@8192
D=A // Gets the address 8192
@n
M = D // Stores the value in n as 8192 (The number of pixels on a screen divided by an address of 16 bits (256 x 512 / 16))

(BLKPIXELLOOP)

@n
D = M // Gets the new value of n
@LOOPKBD
D;JEQ // If the value of n is 0, goto Keyboard Input Loop
@SCREEN
D = A // Gets the starting address of the screen (16384)
@i
A = D+M // Gets the address of RAM[16384 + i]
M = -1 // Sets the value of the above address of RAM[16384 + i] to -1 (16 black pixels)
@i
M = M+1 // Increments i by 1
@n
D = M // Gets the value of n
M = M-1 // Subtracts n by 1

@BLKPIXELLOOP
D;JNE // If the value of n is not equal to 0, keep looping



(WHTSCRNCHANGE) // Change screen to white - functionality

@i
M = 0 // Sets i to 0
@8192
D=A // Gets the address 8192
@n
M = D // Stores the value in n as 8192 (The number of pixels on a screen divided by an address of 16 bits (256 x 512 / 16))

(WHTPIXELLOOP)

@n
D = M // Gets the new value of n
@LOOPKBD
D;JEQ // If the value of n is 0, goto Keyboard Input Loop
@SCREEN
D = A // Gets the starting address of the screen (16384)
@i
A = D+M // Gets the address of RAM[16384 + i]
M = 0 // Sets the value of the above address of RAM[16384 + i] to 0 (16 white pixels)
@i
M = M+1 // Increments i by 1
@n
D = M // Gets the value of n
M = M-1 // Subtracts n by 1

@WHTPIXELLOOP
D;JNE // If the value of n is not equal to 0, keep looping