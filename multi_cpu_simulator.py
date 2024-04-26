import random
import queue
from process import Process
from event import Event
from cpu import CPU

class MultiCPUSimulator:
    def __init__(self, lambda_rate, average_service_time, num_cpus, scenario):
        # Initialize simulator parameters
        if num_cpus <= 0:
            raise ValueError("Number of CPUs must be greater than zero.")
        if scenario not in [1, 2]:
            raise ValueError("Scenario must be either 1 or 2.")

        self.lambda_rate = lambda_rate  # Arrival rate of processes
        self.average_service_time = average_service_time  # Average service time of processes
        self.num_cpus = num_cpus  # Number of CPUs in the simulation
        self.scenario = scenario  # Scenario for process allocation
        self.processes_completed = 0  # Number of completed processes
        self.clock = 0  # Current simulation time
        self.event_queue = queue.PriorityQueue()  # Event queue for scheduling arrivals and departures
        self.total_waiting_time = 0  # Total waiting time of all completed processes
        self.total_turnaround_time = 0  # Total turnaround time of all completed processes
        self.total_processes_arrived = 0  # Total number of arrived processes
        
        # Initialize CPUs and queues
        self.cpus = [CPU() for _ in range(num_cpus)]  # List of CPUs
        self.ready_queues = [queue.Queue() for _ in range(num_cpus)]  # List of per-CPU ready queues
        self.global_ready_queue = queue.Queue() if scenario == 2 else None  # Global ready queue for scenario 2

        # Initialize CPU utilization logs
        self.cpu_utilization_logs = [[] for _ in range(num_cpus)]

    def run(self):
        # Generate initial process and schedule its arrival event
        initial_process = self.generate_process(0)
        self.schedule_event("ARRIVAL", initial_process.arrival_time, initial_process)

        try:
            # Simulation loop
            while not self.end_condition():
                # Process events in the event queue
                if not self.event_queue.empty():
                    event = self.event_queue.get()
                    self.clock = event.event_time

                    # Handle different event types
                    if event.event_type == "ARRIVAL":
                        self.handle_arrival(event)
                    elif event.event_type == "DEPARTURE":
                        self.handle_departure(event.cpu_index if hasattr(event, 'cpu_index') else None)

                else:
                    print("Warning: Event queue is empty before end condition is met.")
                    break
        except Exception as e:
            print(f"An error occurred during simulation: {e}")

        # Report simulation metrics
        self.report_metrics()

    def handle_arrival(self, event):
        # Scenario 1: Randomly assign process to a CPU
        if self.scenario == 1:
            cpu_index = random.randint(0, self.num_cpus - 1)
            selected_cpu = self.cpus[cpu_index]

            # If selected CPU is busy, enqueue process in its ready queue
            if selected_cpu.is_busy:
                self.ready_queues[cpu_index].put(event.process)
            # If selected CPU is idle, assign process to it and schedule departure event
            else:
                departure_time = selected_cpu.assign_process(event.process, self.clock)
                self.schedule_event("DEPARTURE", departure_time, event.process, cpu_index)

        # Scenario 2: Assign process to the first available CPU or global queue
        elif self.scenario == 2:
            idle_cpu_found = False
            for cpu_index, cpu in enumerate(self.cpus):
                if not cpu.is_busy:
                    departure_time = cpu.assign_process(event.process, self.clock)
                    self.schedule_event("DEPARTURE", departure_time, event.process, cpu_index)
                    idle_cpu_found = True
                    break

            # If no idle CPU found, enqueue process in global ready queue
            if not idle_cpu_found:
                self.global_ready_queue.put(event.process)

        # Schedule arrival of next process
        next_process = self.generate_process(self.clock)
        self.schedule_event("ARRIVAL", next_process.arrival_time, next_process)

    def handle_departure(self, cpu_index):
        if cpu_index is None:
            raise ValueError("CPU index must be provided for departure handling.")
        
        # Get CPU and process information
        cpu = self.cpus[cpu_index]
        process = cpu.current_process
        waiting_time = process.start_time - process.arrival_time
        turnaround_time = self.clock - process.arrival_time
        
        # Update simulation statistics
        self.total_waiting_time += waiting_time
        self.total_turnaround_time += turnaround_time
        self.processes_completed += 1

        # Release CPU
        cpu.release(self.clock)

        # Scenario 1: Check for next process in ready queue of the same CPU
        if self.scenario == 1:
            if not self.ready_queues[cpu_index].empty():
                next_process = self.ready_queues[cpu_index].get()
                departure_time = cpu.assign_process(next_process, self.clock)
                self.schedule_event("DEPARTURE", departure_time, next_process, cpu_index)
        
        # Scenario 2: Check global queue for next process
        elif self.scenario == 2 and not self.global_ready_queue.empty():
            next_process = self.global_ready_queue.get()
            departure_time = cpu.assign_process(next_process, self.clock)
            self.schedule_event("DEPARTURE", departure_time, next_process, cpu_index)

    def generate_process(self, last_arrival_time):
        # Generate inter-arrival time and service time for new process
        inter_arrival_time = random.expovariate(self.lambda_rate)
        arrival_time = last_arrival_time + inter_arrival_time
        service_time = random.expovariate(1.0 / self.average_service_time)
        
        # Create and return new process
        new_process = Process(arrival_time, service_time)
        return new_process

    def end_condition(self):
        # Check if the simulation should end based on the number of processes completed
        return self.processes_completed >= 10000

    def schedule_event(self, event_type, event_time, process, cpu_index=None):
        # Create new event and add it to the event queue
        new_event = Event(event_type, event_time, process, cpu_index)
        self.event_queue.put(new_event)

    def report_metrics(self):
        if self.processes_completed == 0:
            print("No processes completed. Metrics cannot be calculated.")
            return

        # Calculate and print simulation metrics
        average_waiting_time = self.total_waiting_time / self.processes_completed
        average_turnaround_time = self.total_turnaround_time / self.processes_completed
        total_throughput = self.processes_completed / self.clock

        if self.scenario == 1:
            total_queue_lengths = [sum(lengths) / len(lengths) if lengths else 0 for lengths in self.queue_length_logs]
            print("Dynamic Average Queue Lengths for Each CPU Queue:")
            for idx, length in enumerate(total_queue_lengths):
                print(f"CPU {idx + 1}: {length:.2f}")
        elif self.scenario == 2:
            average_queue_length = self.global_ready_queue.qsize() if self.global_ready_queue else 0
            print(f"Average Queue Length for Global Queue: {average_queue_length}")

        print("CPU Utilizations:")
        for idx, cpu in enumerate(self.cpus):
            cpu_utilization = cpu.get_utilization(self.clock)
            print(f"CPU {idx + 1}: {cpu_utilization:.2f}%")

        print(f"Average Waiting Time: {average_waiting_time:.2f} seconds.")
        print(f"Average Turnaround Time: {average_turnaround_time:.2f} seconds.")
        print(f"Total Throughput: {total_throughput:.2f} processes per second.")
