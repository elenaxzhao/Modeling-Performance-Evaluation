import numpy as np
from collections import deque
import heapq

class Event:
    """
    Represents an event in the queue simulation.
    """
    def __init__(self, time, event_type, arrival_time, server):
        self.time = time
        self.event_type = event_type  # 'arrival' or 'departure'
        self.arrival_time = arrival_time # None if arrival, og time if departure
        self.server = server

    def __lt__(self, other):
        return self.time < other.time

class MM2Simulator:
    """
    Simulates an M/M/2 queue
    """
    def __init__(self, arrival_rate, service_rate):
        self.arrival_rate = arrival_rate  # λ
        self.service_rate = service_rate  # μ
        self.current_time = 0  # Current time
        self.event_queue = []  # Priority queue of events
        self.queue_length = 0  # Queue length
        self.queue_length_over_time = []  # List to store queue lengths over time
        self.response_times = []  # List to track response times over time
        self.s1_busy = False  # Indicates if server 1 is busy
        self.s2_busy = False  # Indicates if server 1 is busy

        # To keep track of server utilization
        self.total_busy_time = [0,0]  # Total time 1 server is busy, both servers are busy
        self.last_event_time = 0  # Time of the last event for tracking

        self.warm_up_time = 100 * self.arrival_rate

    def exponential(self, r):
        return np.random.exponential(1 / r)

    def schedule_event(self, event_time, event_type, arrival_time, server):
        heapq.heappush(self.event_queue, Event(event_time, event_type, arrival_time, server))

    def run_simulation(self, n):
        # Schedule the first arrival event
        self.schedule_event(self.current_time + self.exponential(self.arrival_rate), 'arrival', None, None)

        # Run the simulation until the specified number of customers are processed
        customers_served = 0

        arrival_times_tracker = deque([])

        warm = False
        
        while customers_served < n:
            if self.current_time > self.warm_up_time and not warm:
                warm = True
            
            # Fetch next event
            event = heapq.heappop(self.event_queue)
            self.current_time = event.time

            # Track server busy time
            if self.s1_busy and self.s2_busy and warm:
                self.total_busy_time[1] += self.current_time - self.last_event_time
            elif (self.s1_busy or self.s2_busy) and warm:
                self.total_busy_time[0] += self.current_time - self.last_event_time

            if event.event_type == 'arrival':
                self.queue_length += 1
                if warm and self.queue_length >= 2:
                    self.queue_length_over_time.append((self.current_time, self.queue_length - 2))
                elif warm:
                    self.queue_length_over_time.append((self.current_time, 0))
                
                # Schedule next arrival
                self.schedule_event(self.current_time + self.exponential(self.arrival_rate), 'arrival', None, None)

                # If the server not busy, this current arrival can be processed immediately, so it's departure is scheduled too
                if not self.s1_busy:
                    self.s1_busy = True
                    service_time = self.exponential(self.service_rate)
                    self.schedule_event(self.current_time + service_time, 'departure', event.time, 1)
                elif not self.s2_busy:
                    self.s2_busy = True
                    service_time = self.exponential(self.service_rate)
                    self.schedule_event(self.current_time + service_time, 'departure', event.time, 2)
                # Otherwise, it's gonna wait in the queue, but let's keep track of when it got there to track response time
                else: 
                    arrival_times_tracker.append(event.time)
            
            elif event.event_type == 'departure':
                self.queue_length -= 1
                if warm:
                    self.response_times.append(self.current_time - event.arrival_time)
                    customers_served += 1
                    if self.queue_length >= 2:
                        self.queue_length_over_time.append((self.current_time, self.queue_length - 2))
                    elif warm:
                        self.queue_length_over_time.append((self.current_time, 0))

                # If there are still customers in the queue, schedule the next departure
                if self.queue_length > 1:
                    service_time = self.exponential(self.service_rate)
                    self.schedule_event(self.current_time + service_time, 'departure', arrival_times_tracker.popleft(), event.server)
                else:
                    if event.server == 1:
                        self.s1_busy = False
                    elif event.server == 2:
                        self.s2_busy = False
            self.last_event_time = self.current_time

        server_utilization = (self.total_busy_time[0] + 2*self.total_busy_time[1]) / (2*(self.current_time - self.warm_up_time))

        return self.response_times, self.queue_length_over_time, server_utilization
