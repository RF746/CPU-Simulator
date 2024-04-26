# MM4 Queue Simulation
# To run use command python main.py <lambda_rate> <average_service_time> <scenario> <num_cpus>
# Where <lambda_rate> is 50, <average_service_time> is 0.02, <scenario> is 1 or 2 <num_cpus> is 4.
# Command to simulate scenario 1: python main.py 50 0.02 1 4
# Command to simulate scenario 2: python main.py 50 0.02 2 4
import sys
from multi_cpu_simulator import MultiCPUSimulator

def main():
    # Check if correct number of command-line arguments is provided
    if len(sys.argv) != 5:
        print("Usage: python main.py <lambda_rate> <average_service_time> <scenario> <num_cpus>")
        sys.exit(1)

    try:
        # Parse command-line arguments
        lambda_rate = int(sys.argv[1])  # Lambda rate (processes per second)
        average_service_time = float(sys.argv[2])  # Average service time per CPU (seconds)
        scenario = int(sys.argv[3])  # Scenario number (1 or 2)
        num_cpus = int(sys.argv[4])  # Number of CPUs

        # Validate input parameters
        if scenario not in [1, 2]:
            raise ValueError("Scenario must be 1 or 2.")
        if num_cpus != 4:
            raise ValueError("Number of CPUs must be 4.")
        if lambda_rate != 50:
            raise ValueError("Lambda rate must be 50 processes per second.")
        if average_service_time != 0.02:
            raise ValueError("Average service time must be 0.02 seconds.")

    except ValueError as e:
        # Handle invalid input
        print(f"Error: {e}")
        sys.exit(1)

    # Run simulation for lambda rates from 50 to 150 with step size 10
    for rate in range(50, 151, 10):
        # Print current simulation configuration
        print(f"\nRunning simulation with Lambda Rate: {rate}, Scenario: {scenario}, CPUs: {num_cpus}")
        
        # Create a simulator instance and run the simulation
        simulator = MultiCPUSimulator(rate, average_service_time, num_cpus, scenario)
        simulator.run()

if __name__ == "__main__":
    main()
