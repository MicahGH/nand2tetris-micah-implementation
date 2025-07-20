#ifndef HACK_SYMBOL_TABLE_H
#define HACK_SYMBOL_TABLE_H

#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <regex>
#include <map>

class hackSymbolTable {
public:
	hackSymbolTable();

	void addLoopSymbol(std::string, int nextLineNumber);
	bool addASymbol(std::string, int nextAddress);
	int getSymbolValue(std::string symbol);

	std::map<std::string, int> symbolTable;
};
#endif