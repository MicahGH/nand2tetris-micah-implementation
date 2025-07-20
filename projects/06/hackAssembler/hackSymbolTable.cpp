#include "hackSymbolTable.h"
#include <map>

hackSymbolTable::hackSymbolTable() {
    // Pre-defined symbols used in the hack assembly language.
    symbolTable["SP"] = 0;
    symbolTable["LCL"] = 1;
    symbolTable["ARG"] = 2;
    symbolTable["THIS"] = 3;
    symbolTable["THAT"] = 4;
    symbolTable["R0"] = 0;
    symbolTable["R1"] = 1;
    symbolTable["R2"] = 2;
    symbolTable["R3"] = 3;
    symbolTable["R4"] = 4;
    symbolTable["R5"] = 5;
    symbolTable["R6"] = 6;
    symbolTable["R7"] = 7;
    symbolTable["R8"] = 8;
    symbolTable["R9"] = 9;
    symbolTable["R10"] = 10;
    symbolTable["R11"] = 11;
    symbolTable["R12"] = 12;
    symbolTable["R13"] = 13;
    symbolTable["R14"] = 14;
    symbolTable["R15"] = 15;
    symbolTable["SCREEN"] = 16384;
    symbolTable["KBD"] = 24576;
}

void hackSymbolTable::addLoopSymbol(std::string symbol, int nextLineNumber) {
        if (symbolTable.count(symbol) > 0) {
            // Don't insert as the loop symbol has already been found in the table
            ;
        }
        else {
            // Insert loop symbol into table with current line number
            symbolTable.insert({ symbol, nextLineNumber });
        }
    }

bool hackSymbolTable::addASymbol(std::string symbol, int nextAddress) {
    // Don't insert as the A-instruction symbol has already been found in the table
    if (symbolTable.count(symbol) > 0) {
        return false;
    }
    else {
        // Insert symbol into table with next free address
        symbolTable.insert({ symbol, nextAddress });
        return true;
    }
}

int hackSymbolTable::getSymbolValue(std::string symbol) {
    // Gets the value of the provided symbol in the symbolTable map
    int symbolValue = symbolTable.find(symbol)->second;
    return symbolValue;
}