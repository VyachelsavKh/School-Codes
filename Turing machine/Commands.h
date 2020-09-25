#include <map>
#include <vector>
#include <string>
#include <fstream>

class Commands
{
private:
	class Command
	{
	public:
		char write_symbol = '\0';
		char move_symbol = 'N';
		int movecommand_symbol = 0;
	};

	std::map<int, std::map<char, Command>> commandsTable;

	std::string alphabet;

	std::ifstream fin;

	std::string name;

public:
	Commands(std::string inputfile);

	void readAlphabet();

	void readCommands();

	std::string Name();

	std::string executeCommands(std::string input, bool print = false);
};