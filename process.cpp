#include <iostream>

class Process {
private:
    static int pid_counter; // Static variable to generate unique PIDs
    int arrival_time;
    int service_time;
    int pid;
    int wait_time;

public:
    // Constructor
    Process(int arrival, int service) : arrival_time(arrival), service_time(service) {
        pid = ++pid_counter;
        wait_time = 0;
    }

    // Method to update wait time
    void update_wait_time(int current_time) {
        wait_time += current_time - arrival_time;
    }

    // Getter methods
    int get_pid() const { return pid; }
    int get_arrival_time() const { return arrival_time; }
    int get_service_time() const { return service_time; }
    int get_wait_time() const { return wait_time; }
};

// Initialize static member
int Process::pid_counter = 0;

int main() {
    // Example usage
    Process p1(0, 5); // Create a process with arrival time 0 and service time 5
    p1.update_wait_time(10); // Update wait time at time 10
    std::cout << "Process ID: " << p1.get_pid() << std::endl;
    std::cout << "Arrival Time: " << p1.get_arrival_time() << std::endl;
    std::cout << "Service Time: " << p1.get_service_time() << std::endl;
    std::cout << "Wait Time: " << p1.get_wait_time() << std::endl;

    return 0;
}
