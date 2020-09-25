#include "long_int_num.h"
#include <iostream>
#include <algorithm>

long_int_num::long_int_num(int a)
{
	num = std::to_string(a);
}
long_int_num::long_int_num(std::string str)
{
	num = str;
}

std::string long_int_num::Num()
{
	return num;
}

bool long_int_num::operator==(long_int_num n)
{
	std::string n2 = n.Num();
	std::string n1 = num;

	return n1 == n2;
}
bool long_int_num::operator==(int n)
{
	long_int_num n1(n);

	return operator==(n1);
}
bool operator==(int n, long_int_num n1)
{
	return n1 == n;
}

bool long_int_num::operator!=(long_int_num n)
{
	std::string n2 = n.Num();
	std::string n1 = num;

	return !(n1 == n2);
}
bool long_int_num::operator!=(int n)
{
	long_int_num n1(n);

	return operator!=(n1);
}
bool operator!=(int n, long_int_num n1)
{
	return n1 != n;
}

bool long_int_num::operator>(long_int_num n)
{
	if ((*this - n).Num()[0] == '-' || (*this - n).Num()[0] == '0')
		return 0;

	return 1;
}
bool long_int_num::operator>(int n)
{
	long_int_num n1(n);

	return operator>(n1);
}
bool operator>(int n, long_int_num n1)
{
	return n1 > n;
}

bool long_int_num::operator<(long_int_num n)
{
	if ((*this - n).Num()[0] == '-')
		return 1;

	return 0;
}
bool long_int_num::operator<(int n)
{
	long_int_num n1(n);

	return operator<(n1);
}
bool operator<(int n, long_int_num n1)
{
	return n1 < n;
}

bool long_int_num::operator>=(long_int_num n)
{
	if ((*this - n).Num()[0] != '-')
		return 1;

	return 0;
}
bool long_int_num::operator>=(int n)
{
	long_int_num n1(n);

	return operator>=(n1);
}
bool operator>=(int n, long_int_num n1)
{
	return n1 >= n;
}

bool long_int_num::operator<=(long_int_num n)
{
	if ((*this - n).Num()[0] == '-' || (*this - n).Num()[0] == '0')
		return 1;

	return 0;
}
bool long_int_num::operator<=(int n)
{
	long_int_num n1(n);

	return operator<=(n1);
}
bool operator<=(int n, long_int_num n1)
{
	return n1 <= n;
}

bool long_int_num::operator!()
{
	return (*this) == 0;
}

long_int_num long_int_num::operator+(long_int_num n)
{
	std::string out = "";

	std::string n2 = n.Num();
	std::string n1 = num;

	bool less0 = 0;

	if (n1[0] == '-' && n2[0] == '-')
	{
		n1.erase(n1.begin());
		n2.erase(n2.begin());

		less0 = 1;
	}

	if (n1[0] == '-' && n2[0] != '-')
	{
		n1.erase(n1.begin());

		return long_int_num(n2) - long_int_num(n1);
	}

	if (n1[0] != '-' && n2[0] == '-')
	{
		n2.erase(n2.begin());

		return long_int_num(n1) - long_int_num(n2);
	}

	while (n1.size() < n2.size())
		n1 = "0" + n1;

	while (n2.size() < n1.size())
		n2 = "0" + n2;

	int numeral;

	int add1 = 0;

	for (int i = n1.size() - 1; i >= 0; i--)
	{
		numeral = (n1[i] - '0') + (n2[i] - '0') + add1;

		if (numeral >= 10)
		{
			numeral -= 10;

			add1 = 1;
		}
		else
			add1 = 0;

		out = std::to_string(numeral) + out;
	}

	if (add1)
		out = "1" + out;
	
	if (less0)
		out = '-' + out;

	return long_int_num(out);
}
long_int_num long_int_num::operator+(int n)
{
	long_int_num n1(n);

	return long_int_num(operator+(n1));
}
long_int_num operator+(int n, long_int_num n1)
{
	return n1 + n;
}

long_int_num long_int_num::operator+=(long_int_num n)
{
	*this = *this + n;
	return *this;
}
long_int_num long_int_num::operator+=(int n)
{
	long_int_num n1(n);

	return long_int_num(operator+=(n1));
}

long_int_num long_int_num::operator-(long_int_num n)
{
	std::string out = "";

	std::string n2 = n.Num();
	std::string n1 = num;
	
	if (n1[0] == '-' && n2[0] == '-')
	{
		n1.erase(n1.begin());
		n2.erase(n2.begin());

		return long_int_num(n2) - long_int_num(n1);
	}

	if (n1[0] == '-' && n2[0] != '-')
	{
		n1.erase(n1.begin());

		return long_int_num('-' + (long_int_num(n2) + long_int_num(n1)).Num());
	}

	if (n1[0] != '-' && n2[0] == '-')
	{
		n2.erase(n2.begin());

		return long_int_num(n1) + long_int_num(n2);
	}

	while (n1.size() < n2.size())
		n1 = "0" + n1;

	while (n2.size() < n1.size())
		n2 = "0" + n2;

	bool less0 = 0;

	if (n1 < n2)
	{
		less0 = 1;

		swap(n1, n2);
	}

	int numeral;

	int ded1 = 0;

	for (int i = n1.size() - 1; i >= 0; i--)
	{
		numeral = (n1[i] - '0') - (n2[i] - '0') - ded1;

		if (numeral < 0)
		{
			numeral += 10;

			ded1 = 1;
		}
		else
			ded1 = 0;

		out = std::to_string(numeral) + out;
	}

	while (out[0] == '0')
	{
		out.erase(out.begin());
	}

	if (out.size() == 0)
		return long_int_num(0);

	if (less0)
	{
		out = '-' + out;
	}
	
	return long_int_num(out);
}
long_int_num long_int_num::operator-(int n)
{
	long_int_num n1(n);

	return long_int_num(operator-(n1));
}
long_int_num operator-(int n, long_int_num n1)
{
	return n1 - n;
}

long_int_num long_int_num::operator-=(long_int_num n)
{
	*this = *this - n;
	return *this;
}
long_int_num long_int_num::operator-=(int n)
{
	long_int_num n1(n);

	return long_int_num(operator-=(n1));
}

long_int_num long_int_num::operator++()
{
	*this = *this + 1;
	return *this;
}
long_int_num long_int_num::operator++(int)
{
	long_int_num tmp = *this;
	++*this;
	return tmp;
}

long_int_num long_int_num::operator--()
{
	*this = *this - 1;
	return *this;
}
long_int_num long_int_num::operator--(int)
{
	long_int_num tmp = *this;
	--*this;
	return tmp;
}

long_int_num long_int_num::operator*(long_int_num n)
{
	long_int_num out;

	std::string n2 = n.Num();
	std::string n1 = num;
	
	if (n1[0] == '-' && n2[0] == '-')
	{
		n1.erase(n1.begin());
		n2.erase(n2.begin());
	}

	if (n1[0] == '-' && n2[0] != '-')
	{
		n1.erase(n1.begin());

		return long_int_num('-' + (long_int_num(n2) * long_int_num(n1)).Num());
	}

	if (n1[0] != '-' && n2[0] == '-')
	{
		n2.erase(n2.begin());

		return long_int_num('-' + (long_int_num(n2) * long_int_num(n1)).Num());
	}

	if (n1.size() < n2.size())
		swap(n1, n2);

	std::string out1;

	int numeral;
	int add;

	for (int i = n2.size() - 1; i >= 0; i--)
	{
		out1 = "";
		add = 0;

		for (int j = n1.size() - 1; j >= 0; j--)
		{
			numeral = (n2[i] - '0') * (n1[j] - '0') + add;

			add = numeral / 10;

			numeral %= 10;

			out1 = std::to_string(numeral) + out1;
		}

		if(add)
			out1 = std::to_string(add) + out1;

		for (int k = 0; k < n2.size() - 1 - i; k++)
			out1 += '0';

		out = out + long_int_num(out1);
	}

	return out;
}
long_int_num long_int_num::operator*(int n)
{
	long_int_num n1(n);

	return long_int_num(operator*(n1));
}
long_int_num operator*(int n, long_int_num n1)
{
	return n1 * n;
}

long_int_num long_int_num::operator*=(long_int_num n)
{
	*this = *this * n;
	return *this;
}
long_int_num long_int_num::operator*=(int n)
{
	long_int_num n1(n);

	return long_int_num(operator*=(n1));
}

long_int_num long_int_num::operator<<(long_int_num n)
{
	long_int_num tmp = *this;

	for (long_int_num i = 0; i < n; i++)
		tmp *= 2;
	
	return tmp;
}
long_int_num long_int_num::operator<<(int n)
{
	long_int_num n1(n);

	return long_int_num(operator<<(n1));
}
long_int_num operator<<(int n, long_int_num n1)
{
	long_int_num n2(n);

	return n2 << n1;
}

long_int_num long_int_num::operator/(long_int_num n)
{
	long_int_num out;

	std::string n2 = n.Num();
	std::string n1 = num;

	if (n1[0] == '-' && n2[0] == '-')
	{
		n1.erase(n1.begin());
		n2.erase(n2.begin());

		return long_int_num(n1) / long_int_num(n2);
	}

	if (n1[0] == '-' && n2[0] != '-')
	{
		n1.erase(n1.begin());

		return long_int_num('-' + (long_int_num(n1) / long_int_num(n2)).Num());
	}

	if (n1[0] != '-' && n2[0] == '-')
	{
		n2.erase(n2.begin());

		return long_int_num('-' + (long_int_num(n1) / long_int_num(n2)).Num());
	}

	long_int_num tmp = *this;

	while(tmp >= n)
	{
		out++;
		tmp = tmp - n;
	}

	return out;
}
long_int_num long_int_num::operator/(int n)
{
	long_int_num n1(n);

	return long_int_num(operator/(n1));
}
long_int_num operator/(int n, long_int_num n1)
{
	long_int_num n2(n);

	return n2 / n1;
}

long_int_num long_int_num::operator/=(long_int_num n)
{
	*this = *this / n;
	return *this;
}
long_int_num long_int_num::operator/=(int n)
{
	long_int_num n1(n);

	return long_int_num(operator/=(n1));
}

long_int_num long_int_num::operator>>(long_int_num n)
{
	for (long_int_num i = 0; i < n; i++)
		*this /= 2;

	return *this;
}
long_int_num long_int_num::operator>>(int n)
{
	long_int_num n1(n);

	return long_int_num(operator>>(n1));
}
long_int_num operator>>(int n, long_int_num n1)
{
	long_int_num n2(n);

	return n2 >> n1;
}

long_int_num long_int_num::operator%(long_int_num n)
{
	return (*this - *this / n * n);
}
long_int_num long_int_num::operator%(int n)
{
	long_int_num n1(n);

	return long_int_num(operator%(n1));
}
long_int_num operator%(int n, long_int_num n1)
{
	long_int_num n2(n);

	return n2 % n1;
}

long_int_num long_int_num::operator%=(long_int_num n)
{
	*this = *this % n;
	return *this;
}
long_int_num long_int_num::operator%=(int n)
{
	long_int_num n1(n);

	return long_int_num(operator%=(n1));
}

long_int_num long_int_num::pow(long_int_num n)
{
	long_int_num out = *this;

	if (n == 0)
		return 1;

	long_int_num m = *this;

	for (long_int_num i = 1; i < n; i++)
		out *= m;

	return out;
}
long_int_num long_int_num::pow(int n)
{
	long_int_num n1(n);

	return long_int_num(pow(n1));
}

std::istream& operator>> (std::istream& in, long_int_num& lin)
{
	in >> lin.num;

	return in;
}
std::ostream& operator<< (std::ostream& out, long_int_num& lin)
{
	out << lin.num;

	return out;
}