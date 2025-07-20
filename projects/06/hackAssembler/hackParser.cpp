#include <string>
#include <iostream>
#include <fstream>
#include <algorithm>
#include "hackParser.h"
#include "hackSymbolTable.h"
#include <regex>

hackParser::hackParser(std::string line, int run) {
    // Erases all white-space from the current line
    line.erase(std::remove(line.begin(), line.end(), ' '), line.end());
    // Checks if current line is an instruction
    isInstruction = checkIsInstruction(line);
    if (isInstruction == true) {
        // Gets the instruction type of the current line
        instructionType = getInstructionType(line);
        // Removes all comments from the current line
        std::string lineWoComments = line.substr(0, line.find("//"));
        if (run == 2){
            // If it is the second run of the .asm file, then it does the parsing logic depending on the instruction type
            if (instructionType == 'A') {
                aInstruction = getAInstruction(lineWoComments);
                aInstructionLabel = getAInstructionLabel(lineWoComments);
            }
            else if (instructionType == 'C') {
                destInstruction = getDestInstruction(lineWoComments);
                jumpInstruction = getJumpInstruction(lineWoComments);
                compInstruction = getCompInstruction(lineWoComments);
         
            }
        }
        else if (run == 1) {
            // If it is the first run of the .asm file, then it does the parsing logic only on the loop "instructions"
            if (instructionType == 'L') {
                loopInstruction = getLoopInstruction(lineWoComments);
            }
        }
    }
}

bool hackParser::checkIsInstruction(std::string line){
    // Checks if line is empty or is a comment and only returns true if the line is an instruction
    if (line == "") {
        return false;
      }
    else if (line.find('/') == 0) {
        return false;
      }
    else {
        return true;
    }
};

char hackParser::getInstructionType(std::string line) {
    // If @ is found at pos 0 of the line, then that means parsedLine is an A-instruction
    if (line.find('@') == 0){
        return 'A';
    }
    // If ( is found at pos 0 of the line, then that means parsedLine is an L-instruction (A loop)
    else if (line.find('(') == 0){
        return 'L';
    }
    // Anything else is a C-Instruction
    else {
        return 'C';
    }
};

std::string hackParser::getAInstructionLabel(std::string lineWoComments) {
    // If true then the line contains an A-instruction with text (a variable) and gets the label
    if (std::regex_search(lineWoComments, std::regex("[a-zA-Z]+")) == true) {
        std::string aInstructionLabel = lineWoComments.erase(0, 1);
        return aInstructionLabel;
    }
    else {
        return "";
    }
}

int hackParser::getAInstruction(std::string lineWoComments) {
    // If false then the line contains an A-instruction without text (not a variable) and gets the number
    if (std::regex_search(lineWoComments, std::regex( "[a-zA-Z]+" )) == false){
        int extractedNumber = stoi(lineWoComments.erase(0,1));
        return extractedNumber;
    }
}

std::string hackParser::getDestInstruction(std::string lineWoComments) {
    // Checks if the C-Instruction has an equals sign, if it does then it must have a destination component and extracts that part
    if (std::regex_search(lineWoComments, std::regex("=")) == false) {
        return "";
    }
    else {
        std::string destInstruction = lineWoComments.substr(0, lineWoComments.find('='));
        return destInstruction;
    }
}

std::string hackParser::getCompInstruction(std::string lineWoComments) {
    // C-Instructions always have a computation component, so it extracts it from between the equals sign and the semicolon
    int posEqualSign = lineWoComments.find('=');
    int posSemicolon = lineWoComments.find(';');
    std::string compInstruction = lineWoComments.substr(posEqualSign + 1, posSemicolon);
    return compInstruction;
}

std::string hackParser::getJumpInstruction(std::string lineWoComments) {
    // Checks if the C-Instruction has a semicolon, if it does then it must have a jump component and extracts that part
    if (std::regex_search(lineWoComments, std::regex(";")) == false) {
        return "";
    }
    else {
        std::string jumpInstruction = lineWoComments.substr(lineWoComments.find(';') + 1);
        return jumpInstruction;
    }
}

std::string hackParser::getLoopInstruction(std::string lineWoComments) {
    // Checks if the instruction has parenthesis, if it does then it must be a loop "instruction" and extracts the label from between the parenthesis
    int posOpenParenthesis = lineWoComments.find('(');
    int posCloseParenthesis = lineWoComments.find(')');
    std::string loopInstruction = lineWoComments.substr(posOpenParenthesis + 1, posCloseParenthesis - 1);
    return loopInstruction;
}