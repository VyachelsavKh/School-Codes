#ifndef LONG_DOUBLE_NUM_H
#define LONG_DOUBLE_NUM_H

#include "long_int_num.h"
#include <string>

class long_double_num
{
private:
	long_int_num order;
	long_int_num mantissa;

public:
	long_double_num(std::string str = "0");
	long_double_num(double n);
};

#endif