# Queueing System Simulator

This project provides a Python-based simulation for M/M/1 and M/M/2 queueing systems. The simulator models queue behaviors and computes key metrics like average response time, queue length, and server utilization. It is designed for both academic and practical insights into queueing theory.

---

## Table of Contents
1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Setup and Installation](#setup-and-installation)
4. [Usage Instructions](#usage-instructions)
5. [Output Metrics](#output-metrics)
6. [Simulation Details](#simulation-details)

---

## Overview

Queueing systems are an essential part of operational research and are widely used to model real-world systems like call centers, server networks, and traffic flows. This project simulates:
- **M/M/1 Queue:** A single-server queue with exponential inter-arrival and service times.
- **M/M/2 Queue:** A two-server queue with exponential inter-arrival and service times.

The results provide insights into how changes in arrival and service rates affect the queue's performance.

---

## Project Structure

### Files

1. **`MM1Simulator.py`**:
   - Simulates an M/M/1 queue with Poisson arrivals and exponential service times.
   - Uses a priority queue to manage events like arrivals and departures.

2. **`MM2Simulator.py`**:
   - Simulates an M/M/2 queue with two servers.
   - Extends the M/M/1 logic to allocate tasks between two servers.

3. **`main.py`**:
   - Acts as the entry point for running the simulations.
   - Accepts command-line inputs and displays simulation results.

---

## Setup and Installation

### Prerequisites
- Python 3.x
- `numpy` library


## Usage Instructions

Run the simulation using the `main.py` script from the command line:

`python main.py <queue_type> <arrival_rate> <service_rate>` 

### Parameters:

-   `<queue_type>`: The type of queueing system to simulate (`mm1` or `mm2`).
-   `<arrival_rate>`: Average number of arrivals per unit of time (λ).
-   `<service_rate>`: Average number of services completed per unit of time (μ).

### Examples:

1.  Simulate an M/M/1 queue with arrival rate 5 and service rate 10:
    
    `python main.py mm1 5 10` 
    
2.  Simulate an M/M/2 queue with arrival rate 8 and service rate 12:
    
    `python main.py mm2 8 12` 
    

----------

## Output Metrics

The simulation outputs the following:

1.  **Average Response Time**: Mean time a customer spends in the system (waiting + service).
2.  **Average Queue Length**: Mean number of customers in the queue.
3.  **Server Utilization (ρ)**: Fraction of time the server(s) are busy.

#### Example Output:


`Simulation results for 10000 customers:`
`Average Response Time: 1.25 units of time`
`Average Queue Length: 3.50 customers`
`Server Utilization (ρ): 0.75`

----------

## Simulation Details

### Warm-Up Period:

To ensure accuracy, the first 100 × λ units of time are discarded, minimizing bias from initial system conditions.

Markdown 2983 bytes 416 words 101 lines Ln 28, Col 9HTML 2170 characters 369 words 54 paragraphs
Import/export
No file chosen
No file chosen
