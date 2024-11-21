import sys
from MM1Simulator import MM1Simulator
from MM2Simulator import MM2Simulator
import numpy as np

class Runner:
    def __init__(self, sim_type, arrival_rate, service_rate):
        self.sim_type = sim_type
        self.arrival_rate = float(arrival_rate)
        self.service_rate = float(service_rate)
        self.n = 10000 # we choose to run 10,000 trials

    def calculate_average_queue_length(self, queue_length_over_time):
        total_time = 0
        total_queue_time = 0

        for i in range(1, len(queue_length_over_time)):
            time_interval = queue_length_over_time[i][0] - queue_length_over_time[i - 1][0]
            queue_length = queue_length_over_time[i - 1][1]
            total_time += time_interval
            total_queue_time += time_interval * queue_length

        return total_queue_time / total_time

    def run(self):
        
        if self.sim_type.lower() == "mm1":
            simulator = MM1Simulator(self.arrival_rate, self.service_rate)
        elif self.sim_type.lower() == "mm2":
            simulator = MM2Simulator(self.arrival_rate, self.service_rate)
        else:
            print(f"Invalid simulator type: {self.sim_type}. Please choose 'mm1' or 'mm2'.")
            return

        response_times, queue_length_over_time, server_utilization = simulator.run_simulation(self.n)

        average_response_time = np.mean(response_times)
        average_queue_length = self.calculate_average_queue_length(queue_length_over_time)

        
        print(f"Simulation results for {self.n} customers:")
        print(f"Average Response Time: {average_response_time:.2f} units of time")
        print(f"Average Queue Length: {average_queue_length:.2f} customers")
        print(f"Server Utilization (ρ): {server_utilization:.2f}")
        
        return


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <mm1/mm2> <arrival_rate> <service_rate>")
    else:
        sim_type = sys.argv[1]
        arrival_rate = sys.argv[2]
        service_rate = sys.argv[3]
        runner = Runner(sim_type, arrival_rate, service_rate)
        runner.run()
