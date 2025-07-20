#include <string>
#include <iostream>
#include <fstream>
#include <algorithm>
#include "hackTranslator.h"
#include "hackParser.h"
#include <regex>
#include <bitset>

hackTranslator::hackTranslator(hackParser object) {
    // Creates a destTable map which stores the destination part of the C-Instruction
    destTable[""] = "000";
    destTable["M"] = "001";
    destTable["D"] = "010";
    destTable["MD"] = "011";
    destTable["A"] = "100";
    destTable["AM"] = "101";
    destTable["AD"] = "110";
    destTable["AMD"] = "111";

    // Creates a compTable map that stores the computation part of the C-Instruction
    compTable["0"] = "0101010";
    compTable["1"] = "0111111";
    compTable["-1"] = "0111010";
    compTable["D"] = "0001100";
    compTable["A"] = "0110000";
    compTable["!D"] = "0001101";
    compTable["!A"] = "0110001";
    compTable["-D"] = "0001111";
    compTable["-A"] = "0110011";
    compTable["D+1"] = "0011111";
    compTable["A+1"] = "0110111";
    compTable["D-1"] = "0001110";
    compTable["A-1"] = "0110010";
    compTable["D+A"] = "0000010";
    compTable["D-A"] = "0010011";
    compTable["A-D"] = "0000111";
    compTable["D&A"] = "0000000";
    compTable["D|A"] = "0010101";
    compTable["M"] = "1110000";
    compTable["!M"] = "1110001";
    compTable["-M"] = "1110011";
    compTable["M+1"] = "1110111";
    compTable["M-1"] = "1110010";
    compTable["D+M"] = "1000010";
    compTable["D-M"] = "1010011";
    compTable["M-D"] = "1000111";
    compTable["D&M"] = "1000000";
    compTable["D|M"] = "1010101";

    // Creates a jumpTable map that stores the jump part of the C-Instruction
    jumpTable[""] = "000";
    jumpTable["JGT"] = "001";
    jumpTable["JEQ"] = "010";
    jumpTable["JGE"] = "011";
    jumpTable["JLT"] = "100";
    jumpTable["JNE"] = "101";
    jumpTable["JLE"] = "110";
    jumpTable["JMP"] = "111";

	if (object.instructionType == 'A') {
        // Translates the A-Instruction
		translatedLine = translateAInstruction(object.aInstruction);
	}
	else if (object.instructionType == 'C') {
        // Translates all parts of the C-Instruction and stores them in a variable called translatedLine
		translatedLine = "111";
        translatedLine = translatedLine + translateCompInstruction(object.compInstruction);
        translatedLine = translatedLine + translateDestInstruction(object.destInstruction);
        translatedLine = translatedLine + translateJumpInstruction(object.jumpInstruction);
	}
}

std::string hackTranslator::translateAInstruction(int aInstruction) {
    // Converts the A-Instruction's decimal number to binary
    std::string translatedALine = '0' + std::bitset< 15 >(aInstruction).to_string();
    return translatedALine;
}

std::string hackTranslator::translateDestInstruction(std::string destInstruction) {
    // Looks up the dest part of the C-Instruction in the destTable map
    std::string translatedDestLine = destTable.find(destInstruction)->second;
	return translatedDestLine;
}

std::string hackTranslator::translateCompInstruction(std::string compInstruction) {
    // Looks up the comp part of the C-Instruction in the compTable map
    std::string translatedCompLine = compTable.find(compInstruction)->second;
	return translatedCompLine;
}

std::string hackTranslator::translateJumpInstruction(std::string jumpInstruction) {
    // Looks up the jump part of the C-Instruction in the jumpTable map
	std::string translatedJumpLine = jumpTable.find(jumpInstruction)->second;
	return translatedJumpLine;
}