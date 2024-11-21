import numpy as np
from collections import deque
import heapq

class Event:
    """
    Represents an event in the queue simulation.
    """
    def __init__(self, time, event_type, arrival_time):
        self.time = time
        self.event_type = event_type  # 'arrival' or 'departure'
        self.arrival_time = arrival_time # None if arrival, og time if departure

    def __lt__(self, other):
        return self.time < other.time

class MM1Simulator:
    """
    Simulates an M/M/1 queue
    """
    def __init__(self, arrival_rate, service_rate):
        self.arrival_rate = arrival_rate  # λ
        self.service_rate = service_rate  # μ
        self.current_time = 0  # current time
        self.event_queue = []  # priority queue of events
        self.queue_length = 0  # queue length
        self.queue_length_over_time = []  # list to store queue lengths over time
        self.response_times = []  # list to track response times over time
        self.server_busy = False  # indicates if server busy

        # to keep track of server utilization
        self.total_busy_time = 0  # total time server is busy
        self.last_event_time = 0  # time of the last event for tracking

        self.warm_up_time = 100 * arrival_rate

    def exponential(self, r):
        return np.random.exponential(1 / r)

    def schedule_event(self, event_time, event_type, arrival_time):
        heapq.heappush(self.event_queue, Event(event_time, event_type, arrival_time))

    def run_simulation(self, n):
        
        # first arrival event
        self.schedule_event(self.current_time + self.exponential(self.arrival_rate), 'arrival', None)

        customers_served = 0
        arrival_times_tracker = deque([])
        warm = False
        
        while customers_served < n:
            
            # to make sure the system warms up
            if self.current_time > self.warm_up_time and not warm:
                warm = True
            
            # fetch next event
            event = heapq.heappop(self.event_queue)
            self.current_time = event.time

            # track server busy time
            if self.server_busy and warm:
                self.total_busy_time += self.current_time - self.last_event_time

            if event.event_type == 'arrival':
                self.queue_length += 1

                # queue is offset by 1 since in this code queue_length includes the number of jobs currently being run 
                if warm and self.queue_length > 0: 
                    self.queue_length_over_time.append((self.current_time, max(self.queue_length - 1, 0)))
                
                # schedule next arrival
                self.schedule_event(self.current_time + self.exponential(self.arrival_rate), 'arrival', None)

                # if the server not busy, this current arrival can be processed immediately, so it's departure is scheduled too
                if not self.server_busy:
                    self.server_busy = True
                    service_time = self.exponential(self.service_rate)
                    self.schedule_event(self.current_time + service_time, 'departure', event.time)
                
                # otherwise, it's gonna wait in the queue, but let's keep track of when it got there to track response time
                else: 
                    arrival_times_tracker.append(event.time)
            
            elif event.event_type == 'departure':
                self.queue_length -= 1
                if warm:
                    self.response_times.append(self.current_time - event.arrival_time)
                    customers_served += 1
                    if self.queue_length > 0:
                        self.queue_length_over_time.append((self.current_time, max(self.queue_length - 1, 0)))

                # if there are still customers in the queue, schedule the next departure
                if self.queue_length > 0:
                    service_time = self.exponential(self.service_rate)
                    self.schedule_event(self.current_time + service_time, 'departure', arrival_times_tracker.popleft())
                else:
                    self.server_busy = False
            self.last_event_time = self.current_time

        server_utilization = self.total_busy_time / (self.current_time - self.warm_up_time)

        return self.response_times, self.queue_length_over_time, server_utilization
