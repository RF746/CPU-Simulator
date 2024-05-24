# Initialize the end condition variable
endCondition = False

# Main loop to manage events
while not endCondition:
    # Get the next event and update the clock
    event = get_event()
    clock = event.time

    # Check the type of event and call appropriate handler
    switch event.type:
        case ARRIVAL:
            handle_arrival(event)  # Handle arrival event
        case DEPARTURE:
            handle_departure(event)  # Handle departure event

# Function to handle arrival events
def handle_arrival(event):
    # If CPU is not busy, immediately schedule departure
    if CPU_busy == 0:
        CPU_busy = 1
        schedule_event(DEPARTURE, clock + service_time, p)
    # If CPU is busy, add process to the ready queue and schedule next arrival
    else:
        add_p_to_ready_queue(p)
        schedule_event(ARRIVAL, clock + interarrival_time, next_process)

# Function to handle departure events
def handle_departure(event):
    # If ready queue is empty, CPU becomes idle
    if is_ready_queue_empty():
        CPU_busy = 0
    # If ready queue is not empty, schedule departure of next process
    else:
        p = get_next_from_ready_queue()
        schedule_event(DEPARTURE, clock + service_time, p)
