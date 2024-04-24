#include <iostream>
#include <vector>
#include <queue>
#include <random>
#include <cmath>

// Define Process class
class Process {
public:
    double arrival_time;
    double service_time;
    double start_time;

    Process(double arrival, double service) : arrival_time(arrival), service_time(service), start_time(0) {}
};

// Define Event class
class Event {
public:
    std::string event_type;
    double event_time;
    Process* process;
    int cpu_index;

    Event(std::string type, double time, Process* p, int index) : event_type(type), event_time(time), process(p), cpu_index(index) {}
};

// Define CPU class
class CPU {
public:
    bool is_busy;
    Process* current_process;

    CPU() : is_busy(false), current_process(nullptr) {}

    double assign_process(Process* process, double current_time) {
        is_busy = true;
        current_process = process;
        current_process->start_time = current_time;
        return current_time + process->service_time;
    }

    void release() {
        is_busy = false;
        current_process = nullptr;
    }
};

// Define MultiCPUSimulator class
class MultiCPUSimulator {
private:
    double lambda_rate;
    double average_service_time;
    int num_cpus;
    int scenario;
    int processes_completed;
    double clock;
    std::priority_queue<Event*, std::vector<Event*>, std::function<bool(Event*, Event*)>> event_queue;
    double total_waiting_time;
    double total_turnaround_time;
    std::vector<CPU*> cpus;
    std::vector<std::queue<Process*>> ready_queues;
    std::queue<Process*> global_ready_queue;

public:
    MultiCPUSimulator(double lambda_rate, double average_service_time, int num_cpus, int scenario) 
        : lambda_rate(lambda_rate), average_service_time(average_service_time), num_cpus(num_cpus), scenario(scenario), processes_completed(0), clock(0), total_waiting_time(0), total_turnaround_time(0) {
        
        if (num_cpus <= 0) {
            throw std::invalid_argument("Number of CPUs must be greater than zero.");
        }
        if (scenario != 1 && scenario != 2) {
            throw std::invalid_argument("Scenario must be either 1 or 2.");
        }

        auto comparator = [](Event* lhs, Event* rhs) { return lhs->event_time > rhs->event_time; };
        event_queue = std::priority_queue<Event*, std::vector<Event*>, decltype(comparator)>(comparator);

        for (int i = 0; i < num_cpus; ++i) {
            cpus.push_back(new CPU());
            if (scenario == 1) {
                ready_queues.push_back(std::queue<Process*>());
            }
        }
    }

    ~MultiCPUSimulator() {
        for (auto cpu : cpus) {
            delete cpu;
        }
        for (auto queue : ready_queues) {
            while (!queue.empty()) {
                delete queue.front();
                queue.pop();
            }
        }
        while (!global_ready_queue.empty()) {
            delete global_ready_queue.front();
            global_ready_queue.pop();
        }
    }

    void run() {
        Process* initial_process = generate_process(0);
        schedule_event("ARRIVAL", initial_process->arrival_time, initial_process);

        try {
            while (!end_condition()) {
                if (!event_queue.empty()) {
                    Event* event = event_queue.top();
                    event_queue.pop();
                    clock = event->event_time;

                    if (event->event_type == "ARRIVAL") {
                        handle_arrival(event);
                    } else if (event->event_type == "DEPARTURE") {
                        handle_departure(event->cpu_index);
                    }
                    delete event;
                } else {
                    std::cout << "Warning: Event queue is empty before end condition is met." << std::endl;
                    break;
                }
            }
        } catch (const std::exception& e) {
            std::cerr << "An error occurred during simulation: " << e.what() << std::endl;
        }

        report_metrics();
    }

private:
    void handle_arrival(Event* event) {
        if (scenario == 1) {
            int cpu_index = 0;
            for (int i = 1; i < num_cpus; ++i) {
                if (ready_queues[i].size() < ready_queues[cpu_index].size()) {
                    cpu_index = i;
                }
            }
            CPU* selected_cpu = cpus[cpu_index];

            if (selected_cpu->is_busy) {
                ready_queues[cpu_index].push(event->process);
            } else {
                double departure_time = selected_cpu->assign_process(event->process, clock);
                schedule_event("DEPARTURE", departure_time, event->process, cpu_index);
            }
        } else if (scenario == 2) {
            bool idle_cpu_found = false;
            for (int i = 0; i < num_cpus; ++i) {
                CPU* cpu = cpus[i];
                if (!cpu->is_busy) {
                    double departure_time = cpu->assign_process(event->process, clock);
                    schedule_event("DEPARTURE", departure_time, event->process, i);
                    idle_cpu_found = true;
                    break;
                }
            }
            if (!idle_cpu_found) {
                global_ready_queue.push(event->process);
            }
        }

        Process* next_process = generate_process(clock);
        schedule_event("ARRIVAL", next_process->arrival_time, next_process);
    }

    void handle_departure(int cpu_index) {
        CPU* cpu = cpus[cpu_index];
        Process* process = cpu->current_process;
        double waiting_time = process->start_time - process->arrival_time;
        double turnaround_time = clock - process->arrival_time;

        total_waiting_time += waiting_time;
        total_turnaround_time += turnaround_time;
        ++processes_completed;

        cpu->release();

        if (scenario == 1) {
            if (!ready_queues[cpu_index].empty()) {
                Process* next_process = ready_queues[cpu_index].front();
                ready_queues[cpu_index].pop();
                double departure_time = cpu->assign_process(next_process, clock);
                schedule_event("DEPARTURE", departure_time, next_process, cpu_index);
            }
        } else if (scenario == 2 && !global_ready_queue.empty()) {
            Process* next_process = global_ready_queue.front();
            global_ready_queue.pop();
            double departure_time = cpu->assign_process(next_process, clock);
            schedule_event("DEPARTURE", departure_time, next_process, cpu_index);
        }
    }

    Process* generate_process(double last_arrival_time) {
        double inter_arrival_time = expovariate(lambda_rate);
        double arrival_time = last_arrival_time + inter_arrival_time;
        double service_time = expovariate(1.0 / average_service_time);
        return new Process(arrival_time, service_time);
    }

    bool end_condition() {
        return processes_completed >= 10000;
    }

    void schedule_event(std::string event_type, double event_time, Process* process, int cpu_index = -1
