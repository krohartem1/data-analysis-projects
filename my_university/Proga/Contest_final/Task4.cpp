/*
#include <iostream>
#include <vector>
#include <cstdint>
#include <algorithm>
bool exam(std::vector<int>& A, std::vector<int>& track, int j, std::vector<uint64_t>& sum, int N)
{
	if (sum[0] == N) { return 1; }
	else if (sum[0] > N) { return 0; }
	for (int i = j; i < A.size(); ++i)
	{
		track.push_back(A[i]);
		sum[0] += A[i];
		if (exam(A, track, i + 1, sum, N)) { return 1; }
		else
		{
			track.pop_back();
			sum[0] -= A[i];
		}
	}
	return 0;
}

int main()
{
	int N, M;
	std::cin >> N >> M;
	std::vector<int> A(2*M);
	std::vector<int> track;
	uint64_t Sum = 0;
	for (int i = 0; i < 2*M; i+=2)
	{
		std::cin >> A[i];
		A[i + 1] = A[i];
		Sum += A[i] + A[i+1];
	}
	std::sort(A.rbegin(), A.rend());
	std::vector<uint64_t> sum(1, 0);
	if (Sum < N)
	{
		std::cout << -1;
	}
	else {
		if (exam(A, track, 0, sum, N))
		{
			std::cout << track.size() << "\n";
			for (int i = 0; i < track.size(); ++i)
			{
				std::cout << track[i] << " ";
			}
		}
		else
		{
			std::cout << 0;
		}
	}
	return 0;
}
*/