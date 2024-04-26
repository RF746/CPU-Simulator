class CPU:
    def __init__(self):
        # Initialize CPU attributes
        self.is_busy = False           # Flag to indicate if CPU is currently busy processing a task
        self.current_process = None    # Reference to the currently running process
        self.utilization_time = 0      # Total time the CPU has been utilized
        self.last_start_time = None    # Time when the current process started

    def assign_process(self, process, current_time):
        # Assign a process to the CPU
        process.start_time = current_time      # Set the start time of the process
        self.current_process = process         # Set the current process
        self.is_busy = True                    # Set CPU to busy
        self.last_start_time = current_time    # Record the start time of the current process
        return current_time + process.service_time  # Return the time when the process will be completed

    def release(self, current_time):
        # Release the current process from the CPU
        if self.current_process:
            # If there is a current process running
            self.utilization_time += current_time - self.last_start_time  # Update the utilization time
            self.current_process = None         # Clear the current process
        self.is_busy = False                    # Set CPU to idle
        self.last_start_time = None            # Clear the last start time

    def calculate_utilization(self, total_simulation_time):
        # Calculate CPU utilization percentage
        if total_simulation_time == 0:
            # Avoid division by zero error
            return 0
        return (self.utilization_time / total_simulation_time) * 100  # Calculate utilization percentage
