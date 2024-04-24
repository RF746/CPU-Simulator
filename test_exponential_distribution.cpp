#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <algorithm>
#include <numeric>
#include <iomanip>
#include <fstream>
#include <cstdlib>
#include <ctime>

// Function to generate exponentially distributed values
double generate_exponential(double mean_service_time) {
    static std::random_device rd;
    static std::mt19937 gen(rd());
    std::exponential_distribution<> dist(1.0 / mean_service_time);
    return dist(gen);
}

int main() {
    // Set mean service time
    double mean_service_time = 0.04;

    // Generate 10,000 exponentially distributed values
    std::vector<double> values(10000);
    for (int i = 0; i < 10000; ++i) {
        values[i] = generate_exponential(mean_service_time);
    }

    // Output the first 100 generated numbers
    std::cout << "First 100 generated numbers:" << std::endl;
    for (int i = 0; i < 100; ++i) {
        std::cout << i + 1 << ": " << values[i] << std::endl;
    }

    // Calculate the empirical mean of the generated values
    double empirical_mean = std::accumulate(values.begin(), values.end(), 0.0) / values.size();
    std::cout << "Empirical Mean: " << empirical_mean << std::endl;
    std::cout << "Expected Mean: " << mean_service_time << std::endl;

    // Plotting the histogram of the generated values (not implemented)

    return 0;
}
