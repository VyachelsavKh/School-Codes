#include "Commands.h"
#include <vector>
#include <map>
#include <iostream>
#include <algorithm>

Commands::Commands(std::string inputfile)
{
	fin.open(inputfile);

	fin >> name;
}

std::string Commands::Name()
{
	return name;
}

void Commands::readCommands()
{
	std::string str;

	Command command;

	while (getline(fin, str))
	{
		while ((str.find("->") == std::string::npos ? str.find("|>") : str.find("->")) == std::string::npos)
		{
			if(!getline(fin, str))
				return;
		}

		command.clear();

		if ((str.find("->") == std::string::npos ? str.find("|>") : str.find("->")) > 0)
		{
			for (int i = 0; str[i] != ' '; i++)
				command.a += str[i];
		}

		str.erase(str.begin(), str.begin() + (str.find("->") == std::string::npos ? str.find("|>") : str.find("->")));

		if (str[0] == '|')
			command.finish = true;

		if (str[str.size() - 1] != '>' || str[str.size() - 2] != '|' && str[str.size() - 2] != '-')
		{
			str.erase(str.begin(), str.begin() + str.find('>') + 2);
			for (int i = 0; str[i] != '\0' && str[i] != ' '; i++)
				command.b += str[i];
		}

		commands.push_back(command);
	}
}

std::string Commands::executeCommands(std::string input, bool print)
{
	bool finish = false;
	bool applied_op = true;

	std::string a, b, newstr;
	int insertpos;

	std::map<std::string, int> prev_words;

	Command prev_operation = commands[0];
	int prev_input_len = input.length();
	int prev_operation_count = 0;

	while (applied_op)
	{
		applied_op = false;

		if (prev_words[input] != 0)
			return input + " Error: The input word repeated";

		prev_words[input]++;

		for (auto command : commands)
		{
			a = command.a;
			b = command.b;
			finish = command.finish;

			insertpos = input.find(a);

			if (insertpos != std::string::npos)
			{
				if (prev_operation_count > prev_input_len + 10)
					return input + " Error: Substitution repeated too often";

				if (prev_operation != command)
				{
					prev_operation = command;
					prev_input_len = input.length();
					prev_operation_count = 0;
				}
				else
					prev_operation_count++;

				newstr = "";

				for (int i = 0; i < insertpos; i++)
					newstr += input[i];

				newstr += b;

				for (int i = insertpos + a.size(); input[i] != '\0'; i++)
					newstr += input[i];

				input = newstr;

				if (print)
					std::cout << input << " - " << a << (finish ? " |> " : " -> ") << b << std::endl;

				if(finish)
					return input;

				applied_op = true;

				break;
			}
		}

		if(!applied_op)
			return input;
	}

	return "";
}