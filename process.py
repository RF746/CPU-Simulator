import itertools

class Process:
    _pid_generator = itertools.count(1)  # Generator for unique process IDs

    def __init__(self, arrival_time, service_time):
        """
        Initializes a Process object with specified arrival time and service time.

        Args:
        - arrival_time: The time at which the process arrives in the system.
        - service_time: The time it takes for the process to be serviced.
        """
        self.arrival_time = arrival_time  # Store arrival time
        self.service_time = service_time  # Store service time
        self.pid = next(self._pid_generator)  # Assign a unique process ID
        self.wait_time = 0  # Initialize wait time to 0

    def update_wait_time(self, current_time):
        """
        Update the wait time of the process based on the current time.

        Args:
        - current_time: The current time in the simulation.
        """
        # Calculate the time the process has waited by subtracting arrival time from current time
        self.wait_time += current_time - self.arrival_time
