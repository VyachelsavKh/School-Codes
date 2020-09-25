#include <iostream>
#include <string>
#include "Commands.h"

using namespace std;

int main()
{
	string input;
	//cin >> input;
	
	input = "|1999-20000|";

	Commands TuringCommands("algorithms/smerd.txt");
	TuringCommands.readAlphabet();
	TuringCommands.readCommands();

	cout << input << ' ' << TuringCommands.Name() << ' ' << TuringCommands.executeCommands(input) << endl;

	return 0;
}