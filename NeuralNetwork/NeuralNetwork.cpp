#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include "NeuralNetwork.h"

int main()
{
    std::cout << "Input NeuralNetwork Folder: ";

    std::string path;
    std::cin >> path;

    std::fstream paramsIn(path + "/Params.txt");

    if (!paramsIn.is_open())
    {
        std::cout << "Wrong Folder or there aren`t Params.txt";
        return 0;
    }

    int layers;
    paramsIn >> layers;

    std::vector<int> NeuronsCount;
    int count;

    for (int i = 0; i < layers; i++)
    {
        paramsIn >> count;
        NeuronsCount.push_back(count);
    }

    double speed;
    paramsIn >> speed;

    paramsIn.close();

    NeuralNetwork nn(NeuronsCount, speed, path);

    std::cout << "Do you need to study NeuralNetwork? 1 - Yes, 0 - No: ";

    bool study;
    std::cin >> study;

    std::ifstream studyLibIn(path + "/StudyLib.txt");

    if (!studyLibIn.is_open())
    {
        std::cout << "Cant open StudyLib.txt";
        return 0;
    }

    int alphabetCount;
    studyLibIn >> alphabetCount;

    std::string letters;

    std::map<char, int> outputNeuronNumber;

    char letter;
    for (int i = 0; i < alphabetCount; i++)
    {
        studyLibIn >> letter;
        letters += letter;
        outputNeuronNumber[letter] = i;
    }

    double percent;

    if (study)
    {
        std::cout << "Input rightAnswers %: ";
        std::cin >> percent;

        if (!nn.setWeights())
            nn.setRandomWeights();

        int exampleCount;
        studyLibIn >> exampleCount;

        std::string rigthAnswers = "";

        std::vector<std::vector<double>> inputData;
        std::vector<double> inputValues;
        std::vector<std::vector<int>> outputNeuronsRightAnswers(exampleCount, std::vector<int>(alphabetCount));

        for (int i = 0; i < exampleCount; i++)
        {
            char rresult;
            studyLibIn >> rresult;

            outputNeuronsRightAnswers[i][outputNeuronNumber[rresult]] = 1;

            double inputValue;
            inputValues.clear();

            for (int i = 0; i < NeuronsCount[0]; i++)
            {
                studyLibIn >> inputValue;

                inputValues.push_back(inputValue);
            }

            rigthAnswers += rresult;
            inputData.push_back(inputValues);
        }
        
        int rightAnswersCount = 0;
        std::vector<double> nnOut;

        int epoch = 0;
        int nnAnswer;

        while (rightAnswersCount < exampleCount * percent / 100.0)
        {
            rightAnswersCount = 0;

            if (epoch % 10 == 0)
                std::cerr << epoch << " epoch\n";

            for (int i = 0; i < exampleCount; i++)
            {

                nnOut = nn.forwarFeed(inputData[i]);

                nnAnswer = 0;

                for (int j = 1; j < nnOut.size(); j++)
                    if (nnOut[j] > nnOut[nnAnswer])
                        nnAnswer = j;

                if (nnAnswer == outputNeuronNumber[rigthAnswers[i]])
                    rightAnswersCount++;

                if (epoch % 10 == 0)
                    std::cerr << "Right answer " << outputNeuronNumber[rigthAnswers[i]] << " other answers: ";

                if (epoch % 10 == 0)
                    for (auto x : outputNeuronsRightAnswers[i])
                        std::cerr << x << ' ';

                if (epoch % 10 == 0)
                    std::cerr << "\n";

                if (epoch % 10 == 0)
                    std::cerr << "Neural network answers: " << nnAnswer << " other answers: ";

                if (epoch % 10 == 0)
                    for (int k = 0; k < nnOut.size(); k++)
                        std::cerr << nnOut[k] << ' ';
                if (epoch % 10 == 0)
                    std::cerr << "\n";

                nn.backPropogation(outputNeuronsRightAnswers[i]);
            }

            if (epoch % 10 == 0)
                std::cerr << int((double)rightAnswersCount / exampleCount * 100) << "% right answers\n";
            
            epoch++;
        }

        epoch--;

        if (epoch % 10 != 0)
            std::cerr << epoch << " epoch\n";

        if (epoch % 10 != 0)
            for (int i = 0; i < exampleCount; i++)
            {
                nnOut = nn.forwarFeed(inputData[i]);

                nnAnswer = 0;

                for (int j = 1; j < nnOut.size(); j++)
                    if (nnOut[j] > nnOut[nnAnswer])
                        nnAnswer = j;

                if (nnAnswer == outputNeuronNumber[rigthAnswers[i]])
                    rightAnswersCount++;


                std::cerr << "Right answer " << outputNeuronNumber[rigthAnswers[i]] << " other answers: ";

                for (auto x : outputNeuronsRightAnswers[i])
                        std::cerr << x << ' ';

                std::cerr << "\n";

                std::cerr << "Neural network answers: " << nnAnswer << " other answers: ";

                for (int k = 0; k < nnOut.size(); k++)
                        std::cerr << nnOut[k] << ' ';
                std::cerr << "\n";
            }

        nn.printWeights();
    }
    else
    {
        nn.setWeights();
    }

    studyLibIn.close();

    std::fstream testsLibIn(path + "/TestsLib.txt");

    if (!testsLibIn.is_open())
    {
        std::cout << "Cant open TestsLib.txt";
        return 0;
    }

    int testsCount;
    testsLibIn >> testsCount;

    std::vector<double> inputValues;
    double inputValue;

    std::vector<double> nnOut;
    double nnAnswer;

    bool nnAnswerRight;
    char rightAnswer;
    std::vector<int> rightAnswers(alphabetCount, 0);

    int epoch = 0;

    for (int i = 0; i < testsCount; i++)
    {
        inputValues.clear();

        for (int j = 0; j < NeuronsCount[0]; j++)
        {
            testsLibIn >> inputValue;

            inputValues.push_back(inputValue);
        }

        nnOut = nn.forwarFeed(inputValues);

        nnAnswer = 0;

        for (int j = 1; j < nnOut.size(); j++)
            if (nnOut[j] > nnOut[nnAnswer])
                nnAnswer = j;
        
        std::cout << "Neuron network thinks this is that symbol: " << letters[nnAnswer] << " Is it true? ";
        
        std::cin >> nnAnswerRight;

        if (!nnAnswerRight)
        {
            std::cout << "What symbol is it? ";
            std::cin >> rightAnswer;

            rightAnswers[outputNeuronNumber[rightAnswer]] = 1;

            epoch = 0;

            do
            {
                if (epoch % 10 == 0)
                    std::cerr << epoch << " epoch\n";

                if (epoch % 10 == 0)
                    std::cerr << "Right answer " << outputNeuronNumber[rightAnswer] << " other answers: ";

                if (epoch % 10 == 0)
                    for (auto x : rightAnswers)
                        std::cerr << x << ' ';

                if (epoch % 10 == 0)
                    std::cerr << "\n";

                if (epoch % 10 == 0)
                    std::cerr << "Neural network answers: " << nnAnswer << " other answers: ";

                if (epoch % 10 == 0)
                    for (int k = 0; k < nnOut.size(); k++)
                        std::cerr << nnOut[k] << ' ';

                if (epoch % 10 == 0)
                    std::cerr << "\n";

                epoch++;

                nn.backPropogation(rightAnswers);

                nnOut = nn.forwarFeed(inputValues);

                nnAnswer = 0;

                for (int j = 1; j < nnOut.size(); j++)
                    if (nnOut[j] > nnOut[nnAnswer])
                        nnAnswer = j;

            } while (nnAnswer != outputNeuronNumber[rightAnswer]);
            
            std::cerr << epoch << " epoch\n";

            std::cerr << "Right answer " << outputNeuronNumber[rightAnswer] << " other answers: ";

            for (auto x : rightAnswers)
                std::cerr << x << ' ';

             std::cerr << "\n";

            std::cerr << "Neural network answers: " << nnAnswer << " other answers: ";

            for (int k = 0; k < nnOut.size(); k++)
               std::cerr << nnOut[k] << ' ';

            std::cerr << "\n";

            rightAnswers[outputNeuronNumber[rightAnswer]] = 0;
        }
    }

    return 0;
}