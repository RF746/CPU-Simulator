while not endCondition:
    event = get_event()
    clock = event.time

    if event.type == ARRIVAL:
        handle_arrival(event)
    elif event.type == DEPARTURE:
        handle_departure(event)

def handle_arrival(event):
    global CPU_busy
    if CPU_busy == 0:
        CPU_busy = 1
        schedule_event(DEPARTURE, clock + service_time, event.process)
    else:
        add_to_ready_queue(event.process)
        schedule_event(ARRIVAL, clock + interarrival_time, next_process)

def handle_departure(event):
    global CPU_busy
    if ready_queue_is_empty():
        CPU_busy = 0
    else:
        next_process = get_next_from_ready_queue()
        schedule_event(DEPARTURE, clock + service_time, next_proce
