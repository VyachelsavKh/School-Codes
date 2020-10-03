#ifndef _NEURAL_NETWORK_H_
#define _NEURAL_NETWORK_H_
#include <vector>
#include <cstdlib>
#include <ctime>
#include <fstream>

class NeuralNetwork
{
private:
	class Neuron
	{
	public:
		double input_value;
		double output_value;
		double error;
		std::vector<double> weigth;

		void act()
		{
			output_value = 1 / (1 + pow(2.71828, -input_value));
		}
	};

	std::vector<std::vector<Neuron>> Neurons;

	double speed;
	std::string path;

	double sygmDerivation(double inputValue)
	{
		if (fabs(inputValue) + 1e-9 > 0 && fabs(inputValue) - 1e-9 < 0)
			return 0.0;

		if (fabs(inputValue) + 1e-9 > 1 && fabs(inputValue) - 1e-9 < 1)
			return 0.0;

		return inputValue * (1.0 - inputValue);
	}

	void transmitSignal(std::vector<Neuron>& firstLayer, std::vector<Neuron>& secondLayer)
	{
		firstLayer[0].output_value = firstLayer[0].input_value;

		for (int i = 1; i < firstLayer.size(); i++)
			firstLayer[i].act();

		for (int i = 1; i < secondLayer.size(); i++)
		{
			secondLayer[i].input_value = 0;

			for (int j = 0; j < firstLayer.size(); j++)
			{
				secondLayer[i].input_value += firstLayer[j].output_value * secondLayer[i].weigth[j];
			}
		}
	}

public:
	NeuralNetwork(const std::vector<int> NeuronsCount, double speed1, std::string path1)
	{
		speed = speed1;
		path = path1;

		Neurons.resize(NeuronsCount.size());

		for (int i = 0; i < Neurons.size(); i++)
			Neurons[i].resize(NeuronsCount[i] + 1);
	}

	~NeuralNetwork()
	{
		printWeights();
	}

	void printWeights()
	{
		std::ofstream weightsOut(path + "/Weights.txt");

		std::cout << "Print weights" << "\n";

		for (int i = 1; i < Neurons.size(); i++)
		{
			for (int j = 1; j < Neurons[i].size(); j++)
			{
				for (int k = 0; k < Neurons[i - 1].size(); k++)
				{
					weightsOut << Neurons[i][j].weigth[k] << ' ';
				}

				weightsOut << '\n';
			}

			weightsOut << '\n';
		}
	}

	void setRandomWeights()
	{
		std::ofstream weightsOut(path + "/Weights.txt");

		srand(static_cast<unsigned int>(time(0)));
		
		for (int i = 1; i < Neurons.size(); i++)
		{
			for (int j = 1; j < Neurons[i].size(); j++)
			{
				Neurons[i][j].weigth.resize(Neurons[i - 1].size());

				for (int k = 0; k < Neurons[i - 1].size(); k++) 
				{
					Neurons[i][j].weigth[k] = (0.5 - (double)(rand()) / RAND_MAX) * Neurons[i].size() / Neurons[i - 1].size();
				}
			}
		}
	}

	bool setWeights()
	{
		std::ifstream weightsOut(path + "/Weights.txt");

		if (!weightsOut.is_open())
			return 0;

		std::cout << "Reading weights" << "\n";

		srand(static_cast<unsigned int>(time(0)));

		double weight;

		for (int i = 1; i < Neurons.size(); i++)
		{
			for (int j = 1; j < Neurons[i].size(); j++)
			{
				Neurons[i][j].weigth.resize(Neurons[i - 1].size());

				for (int k = 0; k < Neurons[i - 1].size(); k++)
				{
					weightsOut >> weight;

					Neurons[i][j].weigth[k] = weight;
				}
			}
		}

		return 1;
	}
	
	std::vector<double> forwarFeed(std::vector<double> inputValues)
	{
		std::vector<double> out;
		
		for (int i = 0; i < Neurons.size(); i++)
			Neurons[i][0].input_value = 1;

		for (int i = 1; i < Neurons[0].size(); i++)
			Neurons[0][i].input_value = inputValues[i - 1];
		
		for (int i = 1; i < Neurons.size(); i++)
			transmitSignal(Neurons[i - 1], Neurons[i]);

		for (int i = 1; i < Neurons[Neurons.size() - 1].size(); i++)
		{
			Neurons[Neurons.size() - 1][i].act();
			out.push_back(Neurons[Neurons.size() - 1][i].output_value);
		}
		
		return out;
	}

	void backPropogation(std::vector<int> rightAnswer)
	{
		double dWeight;

		for (int k = 1; k < Neurons[Neurons.size() - 1].size(); k++)
		{
			if(rightAnswer[k - 1])
				Neurons[Neurons.size() - 1][k].error = pow(1 - Neurons[Neurons.size() - 1][k].output_value, 2);
			else
				Neurons[Neurons.size() - 1][k].error = -pow(Neurons[Neurons.size() - 1][k].output_value, 2);

			Neurons[Neurons.size() - 1][k].error *= sygmDerivation(Neurons[Neurons.size() - 1][k].output_value); //

			for (int j = 0; j < Neurons[Neurons.size() - 2].size(); j++)
			{
				dWeight = speed * Neurons[Neurons.size() - 1][k].error * Neurons[Neurons.size() - 2][j].output_value;

				Neurons[Neurons.size() - 1][k].weigth[j] += dWeight;
			}
		}

		double eError;

		for (int i = Neurons.size() - 2; i <= 1; i--)
		{
			eError = 0;

			for (int j = 1; j < Neurons[i].size(); j++)
			{
				for (int k = 1; k < Neurons[i + 1].size(); k++)
				{
					eError += Neurons[i + 1][k].error * Neurons[i + 1][k].weigth[j];
				}

				Neurons[i][j].error = eError * sygmDerivation(Neurons[i][j].output_value); //

				for (int k = 0; k < Neurons[i - 1].size(); k++)
				{
					dWeight = speed * Neurons[i][j].error * Neurons[i-1][k].output_value;

					Neurons[i][j].weigth[k] += dWeight;
				}
			}
		}
	}
};
#endif // !_NEURAL_NETWORK_H_