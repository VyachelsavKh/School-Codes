class Animal
{
protected:
	std::string nickName;

public:
	Animal(std::string str) : nickName(str) {}

	virtual std::string Type() = 0;

	std::string GetNickName()
	{
		return nickName;
	}
};

class Dog : public Animal
{
public:
	Dog(std::string str = "Dog") : Animal(str) {}

	std::string Type() override
	{
		return "Dog";
	}
};

class Cat : public Animal
{
public:
	Cat(std::string str = "Cat") : Animal(str) {}

	std::string Type() override
	{
		return "Cat";
	}
};

class Shelter
{
protected:
	std::string name;

	std::string printSold(Animal* animal)
	{
		std::string out;

		out = "Shelter " + name + " sold " + animal->Type() + " with nickname " + animal->GetNickName();

		return out;
	}

public:
	Shelter(std::string str) : name(str) {}

	virtual Animal* Sold(std::string name) = 0;

};

class DogShelter : public Shelter
{
public:
	DogShelter(std::string str = "DogShelter") : Shelter(str) {}

	Animal* Sold(std::string name) override //If you write name = "Dog", then the default will not be used, I could not find how to solve this problem
	{
		Animal* out = new Dog(name);

		std::cout << this->printSold(out) << "\n";

		return out;
	}
};

class CatShelter : public Shelter
{
public:
	CatShelter(std::string str = "CatShelter") : Shelter(str) {}

	Animal* Sold(std::string name) override
	{
		Animal* out = new Cat(name);

		std::cout << this->printSold(out) << "\n";

		return out;
	}
};