#include "long_double_num.h"

long_double_num::long_double_num(std::string str)
{
	int pos = str.find('.');

	if (pos == std::string::npos)
	{
		order = long_int_num(str);
		mantissa = 0;
	}
	else
	{
		mantissa = str.substr(pos + 1);
		str.erase(pos);
		order = str;
	}
}
long_double_num::long_double_num(double n)
{
	std::string str = std::to_string(n);

	*this = long_double_num(str);
}