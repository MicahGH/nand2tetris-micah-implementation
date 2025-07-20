# Micah's Nand2Tetris Implementations
<p align="center"><img width=300 src="images/nand2tetris_logo.png"></p>

## What this repo is about and why I did this course
Nand2Tetris is a course created by Noam Nisan and Shimon Schocken; two highly-experienced computer science professors at the University of Jerusalem. The course is all about teaching the fundamentals of how a computer works under the hood and starting up from basic logic gates to programming Tetris. 

The first part of the course includes learning binary, learning to use the Hack HDL (Hardware Description Language) and implementing chips with it (for example, from a simple AND chip all the way up to a fully working COMPUTER chip with ROM, RAM and a CPU), learning assembly and seeing how assembly instructions translate to binary and finally, creating an assembler using a higher-level language that takes Hack assembly files, parsers them and translates them into binary which are then saved in .hack files.

The second part of the course includes: (STILL STUDYING IT AT THIS TIME)

The main reason I did this course was to give myself a better understanding of how exactly a computer functions; something which was previously unknown to me (and to a lot of developers). Doing the course has definitely helped me improve my skills as a developer and has changed my mindset for the better about how to program more effectively and efficiently. I thoroughly enjoyed the course and would recommend it to anyone who wishes to understand computers better.

## Projects
In each week of the course, there is a project that you need to do. Below I will explain what the projects involved. I did these projects without hardly searching for help as I wanted to make sure that I really understood the concepts. 

Please excuse my terrible diagram drawings which I did in Paint :)
### Project 01
Project 01 includes the .hdl files for the basic chips (AND, OR, XOR, MUX, DMUX, etc.) and a .png file with a diagram for each chip.
### Project 02
Project 02 includes the .hdl files for more advanced chips used for computation (Inc16, HalfAdder, FullAdder, ALU, etc.) which were made from the basic chips I made in the previous project. The project folder also contains .png diagrams for each chip.
### Project 03
Project 03 includes the .hdl files for chips based on memory (Register, PC, RAM, etc.) and their .png diagrams.
### Project 04
Project 04 was mostly about learning how the Hack Assembly language works; there are two folders called fill and mult. Inside these folders are .asm files which I wrote myself to: 
For fill: Change a screen completely to black pixels on a keypress and back to white after the key is let go.
For mult: Implement multiplication functionality as the ALU doesn't support it hardware-wise.
### Project 05
Project 05 was about combining all of the previously created chips to create the Memory and CPU chips and then combine them with a built-in ROM chip and a previously created PC (Program Counter) chip to make the Computer chip.
### Project 06
Project 06 is the last project of the first part of the course and involved creating an assembler with a high-level language. In my case, I was going to program it in Python, but in the end I used C++ as I have a lot of experience with Python and wanted more of a challenge. Learning a new language to program something that is not too simple was very difficult, but highly rewarding.

There are many things I could improve about the assembler (mainly the error-handling), but for my first project in C++, I am content with it.

#### Assembler Description
An example of a Hack Assembly file is this:
```
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/06/add/Add.asm

// Computes R0 = 2 + 3  (R0 refers to RAM[0])

@2
D=A
@3
D=D+A
@0
M=D
```

An example of a .hack file (the output from the assembler for the .asm file above) is this:
```
0000000000000010
1110110000010000
0000000000000011
1110000010010000
0000000000000000
1110001100001000
```
#### Assembler Usage
```
path_to_hackAssembler.exe <path_to_asm_file> <optional: output_path_of_hack_file>
```

The assembler takes two arguments: the path to the .asm file and an optional path to the .hack file. If a path is no provided by the user for the .hack file, the assembler automatically creates one in the same directory as the .asm file. It performs some operations to see if the files provided are valid and if so, starts the first run through. In the first run through, it stores (LOOP) variables in a symbol table and once done, starts the second run through in which it parses each line and translates it to binary depending on a number of different parameters.
