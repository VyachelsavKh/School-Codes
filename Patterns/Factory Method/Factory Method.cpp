#include <iostream>
#include "Factory.hpp"

int main()
{
    Shelter* dogShelter = new DogShelter();
    Animal* dog = dogShelter->Sold("Volt");

    Shelter* catShelter = new CatShelter("CatZoo");
    Animal* cat = catShelter->Sold("Barsik");
    
    return 0;
}