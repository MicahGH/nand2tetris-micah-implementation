#ifndef HACK_PARSER_H
#define HACK_PARSER_H

#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <regex>
#include "hackSymbolTable.h"

class hackParser {
public:
    hackParser(std::string line, int run);

    bool checkIsInstruction(std::string line);
    bool isInstruction;

    char getInstructionType(std::string line);
    char instructionType;

    std::string getAInstructionLabel(std::string line);
    std::string aInstructionLabel;

    int getAInstruction(std::string line);
    int aInstruction;

    std::string getDestInstruction(std::string line);
    std::string destInstruction;

    std::string getCompInstruction(std::string line);
    std::string compInstruction;

    std::string getJumpInstruction(std::string line);
    std::string jumpInstruction;

    std::string getLoopInstruction(std::string line);
    std::string loopInstruction;
};
#endif