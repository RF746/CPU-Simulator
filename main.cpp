#include <iostream>
#include <cstdlib>

// Mock MultiCPUSimulator class
class MultiCPUSimulator {
public:
    MultiCPUSimulator(int lambda_rate, float average_service_time, int num_cpus, int scenario) {
        // Implementation of MultiCPUSimulator constructor
    }
    void run() {
        // Implementation of run method
    }
};

int main(int argc, char *argv[]) {
    if (argc != 5) {
        std::cout << "Usage: ./main <lambda_rate> <average_service_time> <scenario> <num_cpus>" << std::endl;
        return 1;
    }

    try {
        int lambda_rate = std::stoi(argv[1]);
        float average_service_time = std::stof(argv[2]);
        int scenario = std::stoi(argv[3]);
        int num_cpus = std::stoi(argv[4]);

        if (scenario != 1 && scenario != 2) {
            throw std::invalid_argument("Scenario must be 1 or 2.");
        }
        if (num_cpus != 4) {
            throw std::invalid_argument("Number of CPUs must be 4.");
        }
        if (lambda_rate != 50) {
            throw std::invalid_argument("Lambda rate must be 50 processes per second.");
        }
        if (average_service_time != 0.02) {
            throw std::invalid_argument("Average service time must be 0.02.");
        }

    } catch (const std::invalid_argument& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    for (int rate = 50; rate <= 150; rate += 10) {
        std::cout << "\nRunning simulation with Lambda Rate: " << rate << ", Scenario: " << argv[3] << ", CPUs: " << argv[4] << std::endl;
        MultiCPUSimulator simulator(rate, std::stof(argv[2]), std::stoi(argv[4]), std::stoi(argv[3]));
        simulator.run();
    }

    return 0;
}
