#include <iostream>
#include <vector>
#include <string>

void print_buckets(std::vector<std::string>& mass, std::vector<std::vector<std::string>>& buckets, int j, int k)
{
	for (int i = 0; i < mass.size(); ++i)
	{
		buckets[mass[i][k - j] - '0'].push_back(mass[i]);
	}
	mass.clear();
	for (int i = 0; i < 10; ++i)
	{
		std::cout << "Bucket " << i << ": ";
		if (buckets[i].empty()) { std::cout << "empty\n"; }
		else {
			std::cout << buckets[i][0];
			mass.push_back(buckets[i][0]);
			for (int j = 1; j < buckets[i].size(); ++j)
			{
				std::cout << ", " << buckets[i][j];
				mass.push_back(buckets[i][j]);
			}
			std::cout << "\n";
			buckets[i].clear();
		}
	}
	std::cout << "**********\n";
}

int main()
{
	int N = 0;
	std::cin >> N;
	std::vector<std::string> mass(N);
	std::vector<std::vector<std::string>> buckets(10, std::vector<std::string>());
	for (int i = 0; i < N; ++i)
	{
		std::cin >> mass[i];
	}
	std::cout << "Initial array:\n" << mass[0];
	for (int i = 1; i < N; ++i)
	{
		std::cout << ", " << mass[i];
	}
	std::cout << "\n" << "**********\n";
	int k = mass[0].size();
	for (int j = 1; j <= k; ++j)
	{
		std::cout << "Phase " << j << "\n";
		print_buckets(mass, buckets, j, k);
	}
	std::cout << "Sorted array:\n";
	std::cout << mass[0];
	for (int i = 1; i < N; ++i)
	{
		std::cout << ", " << mass[i];
	}
	return 0;
}