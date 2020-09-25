#ifndef LONG_INT_NUM_H
#define LONG_INT_NUM_H

#include <string>

class long_int_num
{
private:
	std::string num;

public:
	long_int_num(int a = 0);
	long_int_num(std::string str);

	std::string Num();

	bool operator==(long_int_num n);
	bool operator==(int n);

	bool operator!=(long_int_num n);
	bool operator!=(int n);

	bool operator>(long_int_num n);
	bool operator>(int n);

	bool operator<(long_int_num n);
	bool operator<(int n);

	bool operator>=(long_int_num n);
	bool operator>=(int n);

	bool operator<=(long_int_num n);
	bool operator<=(int n);

	bool operator!();

	long_int_num operator+(long_int_num n);
	long_int_num operator+(int n);

	long_int_num operator+=(long_int_num n);
	long_int_num operator+=(int n);

	long_int_num operator-(long_int_num n);
	long_int_num operator-(int n);

	long_int_num operator-=(long_int_num n);
	long_int_num operator-=(int n);

	long_int_num operator++();
	long_int_num operator++(int);

	long_int_num operator--();
	long_int_num operator--(int);

	long_int_num operator*(long_int_num n);
	long_int_num operator*(int n);

	long_int_num operator*=(long_int_num n);
	long_int_num operator*=(int n);

	long_int_num operator<<(long_int_num n);
	long_int_num operator<<(int n);

	long_int_num operator/(long_int_num n);
	long_int_num operator/(int n);

	long_int_num operator/=(long_int_num n);
	long_int_num operator/=(int n);

	long_int_num operator>>(long_int_num n);
	long_int_num operator>>(int n);

	long_int_num operator%(long_int_num n);
	long_int_num operator%(int n);

	long_int_num operator%=(long_int_num n);
	long_int_num operator%=(int n);

	long_int_num pow(long_int_num n);
	long_int_num pow(int n);

	friend std::ostream& operator<< (std::ostream& out, long_int_num& lin);
	friend std::istream& operator>> (std::istream& in, long_int_num& lin);
};

bool operator==(int n, long_int_num n1);
bool operator!=(int n, long_int_num n1);
bool operator>(int n, long_int_num n1);
bool operator<(int n, long_int_num n1);
bool operator>=(int n, long_int_num n1);
bool operator<=(int n, long_int_num n1);

long_int_num operator+(int n, long_int_num n1);
long_int_num operator-(int n, long_int_num n1);
long_int_num operator*(int n, long_int_num n1);
long_int_num operator<<(int n, long_int_num n1);
long_int_num operator/(int n, long_int_num n1);
long_int_num operator>>(int n, long_int_num n1);
long_int_num operator%(int n, long_int_num n1);

#endif