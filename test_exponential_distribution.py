import random
import math
import matplotlib.pyplot as plt

def generate_exponential(mean_service_time):
    """
    Generate a random number from an exponential distribution
    with the specified mean service time.
    
    Args:
    - mean_service_time: Mean service time for the exponential distribution
    
    Returns:
    A randomly generated number from the exponential distribution
    """
    # Generate a random number between 0 and 1
    u = random.random()
    # Apply the inverse CDF of the exponential distribution
    return -mean_service_time * math.log(1 - u)

def main():
    # Generate 10,000 exponentially distributed values with a mean of 0.04
    mean_service_time = 0.04
    values = [generate_exponential(mean_service_time) for _ in range(10000)]

    # Output the first 100 generated numbers
    print("First 100 generated numbers:")
    for i in range(100):
        print(f"{i+1}: {values[i]}")

    # Calculate the empirical mean of the generated values
    empirical_mean = sum(values) / len(values)
    print(f"\nEmpirical Mean: {empirical_mean}")
    print(f"Expected Mean: {mean_service_time}")

    # Plotting the histogram of the generated values
    plt.hist(values, bins=50, density=True, alpha=0.6, color='g')

    # Plot title and labels
    plt.title('Histogram of Exponentially Distributed Values')
    plt.xlabel('Service Time')
    plt.ylabel('Density')

    plt.show()

if __name__ == "__main__":
    main()
