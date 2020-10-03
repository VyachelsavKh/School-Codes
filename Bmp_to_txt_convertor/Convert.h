#ifndef _CONVERT_H_
#define _CONVERT_H
#include "bitmap-master/bitmap_image.hpp"
#include <iostream>
#include <vector>
#include <string>

struct Pixel
{
    int red = 0, green = 0, blue = 0, count = 0;
};

std::string conv(double gr)
{
    gr = 1 - gr;

    if (0 > gr - 0.01 && 0 < gr + 0.01)
        return "0     ";

    std::string out = std::to_string(gr).substr(0, 6);

    return out;
}

void convert_bmp_to_txt(std::string image_path, std::ofstream& fout, std::string name, int newHeight, int newWidth, int outputNames)
{
    bitmap_image image(image_path);
    
    const unsigned int height = image.height();
    const unsigned int width = image.width();

    if (!image)
    {
        std::cout << "Error - Failed to open: " << image_path << '\n';
        return;
    }

    double red, green, blue;
    rgb_t colours[9];

    std::vector<std::vector<Pixel>> newImage(newWidth, std::vector<Pixel>(newHeight));

    int newx;
    int newy;
    
    for (int y = 0; y < height; ++y)
    {
        for (int x = 0; x < width; ++x)
        {
            newx = round((double)x / (width - 1) * (newWidth - 1));
            newy = round((double)y / (height - 1) * (newHeight - 1));
            
            red = 0;
            green = 0;
            blue = 0;

            for (int j = -1; j <= 1; j++)
            {
                for (int i = -1; i <= 1; i++)
                {
                    if (x + i >= 0 && x + i < width && y + j >= 0 && y + j < height)
                    {
                        image.get_pixel(x + i, y + j, colours[(i + 1) + (j + 1) * 3]);
                    }
                    else
                    {
                        colours[(i + 1) + (j + 1) * 3].red = 255;
                        colours[(i + 1) + (j + 1) * 3].green = 255;
                        colours[(i + 1) + (j + 1) * 3].blue = 255;
                    }
                }
            }

            for (int j = -1; j <= 1; j++)
            {
                for (int i = -1; i <= 1; i++)
                {
                    if (abs(i) + abs(j) == 2)
                    {
                        red += colours[(i + 1) + (j + 1) * 3].red * 1.25;
                        green += colours[(i + 1) + (j + 1) * 3].green * 1.25;
                        blue += colours[(i + 1) + (j + 1) * 3].blue * 1.25;
                    }
                    if (abs(i) + abs(j) == 1)
                    {
                        red += colours[(i + 1) + (j + 1) * 3].red * 5;
                        green += colours[(i + 1) + (j + 1) * 3].green * 5;
                        blue += colours[(i + 1) + (j + 1) * 3].blue * 5;
                    }
                    if (abs(i) + abs(j) == 0)
                    {
                        red += colours[(i + 1) + (j + 1) * 3].red * 75;
                        green += colours[(i + 1) + (j + 1) * 3].green * 75;
                        blue += colours[(i + 1) + (j + 1) * 3].blue * 75;
                    }
                }
            }

            newImage[newx][newy].red += red;
            newImage[newx][newy].green += green;
            newImage[newx][newy].blue += blue;
            newImage[newx][newy].count++;
        }
    }            
    
    rgb_t colour;

    for (int y = 0; y < newHeight; ++y)
    {
        for (int x = 0; x < newWidth; ++x)
        {
            newImage[x][y].red = newImage[x][y].red / 100 / (newImage[x][y].count == 0 ? 1 : newImage[x][y].count);
            newImage[x][y].green = newImage[x][y].green / 100 / (newImage[x][y].count == 0 ? 1 : newImage[x][y].count);
            newImage[x][y].blue = newImage[x][y].blue / 100 / (newImage[x][y].count == 0 ? 1 : newImage[x][y].count);

        }
    }
    
    double grey;

    if(outputNames)
        fout << name << "\n";
    
    for (int y = 0; y < newHeight; ++y)
    {
        for (int x = 0; x < newWidth; ++x)
        {
            grey = newImage[x][y].red * 0.3 + newImage[x][y].green * 0.6 + newImage[x][y].blue * 0.1;

            fout << conv(grey / 255) << ' ';
        }
        fout << "\n";
    }

    fout << "\n";
}
#endif