#include "Commands.h"
#include <iostream>

Commands::Commands(std::string inputfile)
{
	fin.open(inputfile);

	fin >> name;
}

void Commands::readAlphabet()
{
	fin >> alphabet;

	if (alphabet[0] == '#')
		fin >> alphabet;

	if(alphabet[alphabet.size() - 1] != '@')
		alphabet += '@';
}

std::string Commands::Name()
{
	return name;
}

void Commands::readCommands()
{
	std::string str;

	int n = 1;
	int i = 1;

	for (int k = 0; k != n; i++)
	{
		for(int j = 0; j < alphabet.size(); j++)
		{
			fin >> str;

			if (str.find(",") == std::string::npos)
				fin >> str;
			
			if (str == "")
			{
				n = 0;
				break;
			}

			if (str[0] == '#')
				fin >> str;

			char write_symbol = str[0] == ',' ? '\0' : str[0];

			if (str[0] != ',')
			{
				str.erase(str.begin());
				str.erase(str.begin());
			}
			else
				str.erase(str.begin());

			char move_symbol = str[0] == ',' ? 'N' : str[0];

			if (str[0] != ',')
			{
				str.erase(str.begin());
				str.erase(str.begin());
			}
			else
				str.erase(str.begin());

			int movecommand_symbol;

			if (str.size() == 0)
				movecommand_symbol = 0;
			else
				movecommand_symbol = str[0] == '!' ? -1 : stoi(str);

			if(str == "!")
				str.erase(str.begin());
			
			commandsTable[i][alphabet[j]].write_symbol = write_symbol;
			commandsTable[i][alphabet[j ]].move_symbol = move_symbol;
			commandsTable[i][alphabet[j]].movecommand_symbol = movecommand_symbol;
		}
	}
}

std::string Commands::executeCommands(std::string input, bool print)
{
	std::string str = input;

	int q = 1;
	int pos = 0;

	while (true)
	{
		char write_symbol = commandsTable[q][str[pos]].write_symbol;
		char move_symbol = commandsTable[q][str[pos]].move_symbol;
		int movecommand_symbol = commandsTable[q][str[pos]].movecommand_symbol;

		if (write_symbol != '\0')
			str[pos] = write_symbol;

		pos = move_symbol == 'N' ? pos : move_symbol == 'R' || move_symbol == 'r' ? pos + 1 : pos - 1;

		if (pos == -1)
		{
			str = "@@" + str;
			pos += 2;
		}
		
		if (pos == str.size())
			str += "@@";

		if (print)
			std::cout << str << ' ' << q << ' ' << pos << ' ' << str[pos] << ' ' << write_symbol << ' ' << move_symbol << ' ' << movecommand_symbol << std::endl;

		if (movecommand_symbol == -1)
		{
			std::string out;

			for (auto x : str)
			{
				if (x != '@')
					out += x;
			}

			return out;
		}

		if(movecommand_symbol != 0)
				q = movecommand_symbol;
	}
}