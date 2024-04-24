#include <iostream>

class Event {
public:
    Event(int event_type, double event_time, int process, int cpu_index = -1) :
            event_type(event_type), event_time(event_time), process(process), cpu_index(cpu_index) {}

    bool operator<(const Event& other) const {
        return event_time < other.event_time;
    }

    int getEventType() const {
        return event_type;
    }

    double getEventTime() const {
        return event_time;
    }

    int getProcess() const {
        return process;
    }

    int getCpuIndex() const {
        return cpu_index;
    }

private:
    int event_type;
    double event_time;
    int process;
    int cpu_index;
};

int main() {
    Event event(1, 10.5, 100); // Example instantiation of Event
    std::cout << "Event type: " << event.getEventType() << std::endl;
    std::cout << "Event time: " << event.getEventTime() << std::endl;
    std::cout << "Process: " << event.getProcess() << std::endl;
    std::cout << "CPU index: " << event.getCpuIndex() << std::endl;

    return 0;
}
