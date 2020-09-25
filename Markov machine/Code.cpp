#include <iostream>
#include <string>
#include "Commands.h"

using namespace std;

string operator* (string str, int n)
{
	string newstr;

	for (int i = 0; i < n; i++)
		newstr += str;

	return newstr;
}

int main()
{
	string input;
	//cin >> input;

	input = "1111";

	Commands MarkovCommands("algorithms/2.57.txt");
	MarkovCommands.readCommands();

	cout << input << ' ' << MarkovCommands.Name() << ' ' << MarkovCommands.executeCommands(input, 1) << endl;

	return 0;
}