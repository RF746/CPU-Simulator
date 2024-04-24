#include <iostream>

class Process {
public:
    int start_time;
    int service_time;
};

class CPU {
private:
    bool is_busy;
    Process* current_process;
    int utilization_time;
    int last_start_time;

public:
    CPU() {
        is_busy = false;
        current_process = nullptr;
        utilization_time = 0;
        last_start_time = 0;
    }

    int assign_process(Process* process, int current_time) {
        process->start_time = current_time;
        current_process = process;
        is_busy = true;
        last_start_time = current_time;
        return current_time + process->service_time;
    }

    void release(int current_time) {
        if (current_process != nullptr) {
            utilization_time += current_time - last_start_time;
            current_process = nullptr;
        }
        is_busy = false;
        last_start_time = 0;
    }

    float get_utilization(int total_simulation_time) {
        return (float(utilization_time) / total_simulation_time) * 100;
    }
};

int main() {
    // Example usage
    CPU cpu;

    Process process1;
    process1.service_time = 10;

    Process process2;
    process2.service_time = 15;

    int total_simulation_time = 100;

    int end_time = cpu.assign_process(&process1, 0);
    cpu.release(end_time);

    end_time = cpu.assign_process(&process2, end_time);
    cpu.release(end_time);

    std::cout << "CPU Utilization: " << cpu.get_utilization(total_simulation_time) << "%" << std::endl;

    return 0;
}
