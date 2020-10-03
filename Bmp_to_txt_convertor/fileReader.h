#ifndef _FILE_READER_H_
#define _FILE_READER_H_
#include "dirent.h"
#include <vector>

std::vector<std::string> readFiles(std::string path)
{
    DIR* dir;
    dirent* entry;
    
    std::vector<std::string> out;

    dir = opendir(path.c_str());
    if (!dir) {
        out.push_back("Error open dir");

        return out;
    };
    
    std::string fileBMP;

    while ((entry = readdir(dir)) != NULL)
    {
        fileBMP = entry->d_name;
        if(fileBMP.find(".bmp") != std::string::npos)
            out.push_back(fileBMP);
    };

    closedir(dir);

    return out;
}
#endif