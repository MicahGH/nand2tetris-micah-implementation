#include <fstream>
#include <iostream>
#include <string>
#include <filesystem>
#include "hackParser.h"
#include "hackTranslator.h"
#include "hackSymbolTable.h"
namespace fs = std::filesystem;

int main(int argc, char* argv[]) {
    // Checks the number of arguments provided by the user. If none or too many are provided, it exits the program and throws an error
    if (argc <= 1) {
        std::cout << "NO ARGUMENTS PROVIDED BY THE USER" << std::endl;
        std::cout << "Usage: " << argv[0] << " <path_to_asm_file> <optional: output_path_of_hack_file>" << std::endl;
        return 0;
    }
    else if (argc > 3) {
        std::cout << "TOO MANY ARGUMENTS PROVIDED BY THE USER" << std::endl;
        std::cout << "Usage: " << argv[0] << " <path_to_asm_file> <optional: output_path_of_hack_file>" << std::endl;
        return 0;
    }

    // Checks the validity and / or existence of the extensions of the arguments provided by the user
    if (fs::path(argv[1]).extension() != ".asm"){
        std::cout << "NO .asm FILE PROVIDED BY THE USER" << std::endl;
        std::cout << "Usage: " << argv[0] << " <path_to_asm_file> <optional: output_path_of_hack_file>" << std::endl;
        return 0;
    }
    std::ifstream asmFile(argv[1]);

    // If the .asm input file is not found, it throws an error
    if (!asmFile) {
        std::cout << ".asm INPUT FILE NOT FOUND" << std::endl;
        return 0;
    }
    
    // Gets the .asm file input as a string
    std::string inputFileName = argv[1];

    // Creates the .hack file
    std::ofstream hackFile;

    // Checks if the second specified argument has a .hack extension
    if (argv[2] != NULL) {
        if (fs::path(argv[1]).extension() != ".hack") {
            std::cout << "THE THIRD ARGUMENT REQUIRES A .hack EXTENSION" << std::endl;
            std::cout << "Usage: " << argv[0] << " <path_to_asm_file> <optional: output_path_of_hack_file>" << std::endl;
            return 0;
        }
        else {
            hackFile.open(argv[2]);
            // If the .hack file is not found, it throws an error
            if (!hackFile) {
                std::cout << ".hack INPUT FILE NOT FOUND" << std::endl;
                return 0;
            }
        }
    }
    else {
        // If no .hack file path is specified, it creates a .hack file in the same directory as the specified .asm file using .asm file name and path
        std::string outputFileName = inputFileName.substr(0, inputFileName.find_last_of('.')) + ".hack";
        hackFile.open(outputFileName);
    }
    
    // First run through
    std::string line;
    hackSymbolTable symbolTable;
    int run = 1;
    int lineNumber = 0;
    /// Does a first run through the .asm file to get L-Instructions and stores them in the symbol table
    while (std::getline(asmFile, line)) {
        hackParser parsedLine(line, run);

        if (parsedLine.isInstruction == true) {
            if (parsedLine.loopInstruction != "") {
                symbolTable.addLoopSymbol(parsedLine.loopInstruction, lineNumber); // Add Loop symbol to symbolTable with current line
            }
            else {
                lineNumber = lineNumber + 1;
            }
        }

    }

    // Second run through
    run = 2;
    asmFile.clear();
    asmFile.seekg(0);
    int aLabelAddress = 16;
    /// Does a second run through to do the parsing and translation of each assembly instruction
    while (std::getline(asmFile, line)) {
        hackParser parsedLine(line, run);
        
        if (parsedLine.isInstruction) {
            if (parsedLine.aInstructionLabel != "") {
                bool insertedAInstruction = symbolTable.addASymbol(parsedLine.aInstructionLabel, aLabelAddress);
                if (insertedAInstruction == true) {
                    parsedLine.aInstruction = aLabelAddress;
                    aLabelAddress = aLabelAddress + 1;
                }
                else {
                    parsedLine.aInstruction = symbolTable.getSymbolValue(parsedLine.aInstructionLabel);
                }
            }
            if (parsedLine.instructionType != 'L') {
                // Writes the translated instruction to the .hack file
                hackTranslator translatedLine(parsedLine);
                hackFile << translatedLine.translatedLine << std::endl;
            }
        }
    }
    // Outputs success message and closes .asm and .hack file
    std::cout << "File: " << inputFileName << " has been parsed successfully.";
    asmFile.close();
    hackFile.close();
}