#ifndef HACK_TRANSLATOR_H
#define HACK_TRANSLATOR_H

#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <regex>
#include "hackParser.h"
#include <bitset>
#include <map>

class hackTranslator {
public:
	hackTranslator(hackParser object);

	std::string translateAInstruction(int aInstruction);
	std::string translateDestInstruction(std::string destInstruction);
	std::string translateCompInstruction(std::string compInstruction);
	std::string translateJumpInstruction(std::string jumpInstruction);
	
	std::string translatedLine;

	std::map<std::string, std::string> destTable;
	std::map<std::string, std::string> compTable;
	std::map<std::string, std::string> jumpTable;
};
#endif