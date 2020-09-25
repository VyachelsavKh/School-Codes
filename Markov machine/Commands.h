#include <fstream>
#include <string>
#include <vector>

class Commands
{
private:
	class Command
	{
	public:
		std::string a = "";
		std::string b = "";
		bool finish = 0;

		void clear()
		{
			a = "";
			b = "";
			finish = 0;
		}

		friend bool operator!=(Command first, Command second)
		{
			if (first.a == second.a)
				if (first.b == second.b)
					if (first.finish == second.finish)
						return false;
			return true;
		}
	};

	std::vector<Command> commands;

	std::ifstream fin;

	std::string name;

public:
	Commands(std::string inputfile);

	std::string Name();

	void readCommands();

	std::string executeCommands(std::string input, bool print = false);
};