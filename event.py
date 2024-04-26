class Event:
    def __init__(self, event_type, event_time, process, cpu_index=None):
        """
        Initialize an Event object.

        Args:
            event_type (str): Type of event (e.g., arrival, departure).
            event_time (float): Time at which the event occurs.
            process (object): The process associated with the event.
            cpu_index (int, optional): CPU index relevant to the event.
        """
        self.event_type = event_type  # Type of event
        self.event_time = event_time  # Time at which the event occurs
        self.process = process  # Process associated with the event
        self.cpu_index = cpu_index  # CPU index relevant to the event (optional)

    def __lt__(self, other):
        """
        Compare two events based on their occurrence time.

        Args:
            other (Event): Another Event object to compare with.

        Returns:
            bool: True if this event occurs before the other event, False otherwise.
        """
        return self.event_time < other.event_time
