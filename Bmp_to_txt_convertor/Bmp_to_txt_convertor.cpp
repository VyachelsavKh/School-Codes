#include <iostream>
#include <fstream>
#include <vector>
#include <set>
#include "Convert.h"
#include "fileReader.h"

int main()
{
    std::cout << "Input images folder: ";

    std::string path;
    std::cin >> path;

    std::cout << "Do you need to print files names: ";

    bool outputNames;
    std::cin >> outputNames;

    int height;
    int width;
    std::cout << "Input new images height: ";
    std::cin >> height;
    std::cout << "Input new images width: ";
    std::cin >> width;

    std::vector<std::string> files = readFiles(path);

    std::ofstream fout(path + "/Out.txt");

    std::set<char> names;

    for (int i = 0; i < files.size(); i++)
        names.insert(files[i][0]);

    if (outputNames)
        fout << names.size() << "\n";

    if(outputNames)
        for (auto name : names)
            fout << name << ' ';

    if (outputNames)
        fout << "\n\n";

    std::string name;
    std::string bmpPath;

    fout << files.size() << "\n";

    for (int i = 0; i < files.size(); i++)
    {
        name = files[i][0];
        bmpPath = path + "/" + files[i];

        convert_bmp_to_txt(bmpPath, fout, name, height, width, outputNames);
    }
    
    return 0;
}