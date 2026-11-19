# Program to calculate the perimeter of a circle using the concept of line integral.
# Also verifies the fact that the deviation error between the calculated value and
# actual value decreases as the number of divisions increases.

# Imports.
import math
import matplotlib.pyplot as plt

# Inputs.
# @input r -- radius of circle

r = float(input("Enter the radius of the circle: "))

# Function to calculate the integral by repeated summing.
#
# @param n -- the number of iterations to be done
def integrate(n):
    # Define the variables.
    calc_circ = 0
    actual_circ = 2 * math.pi * r
    x = 0
    y = r
    dx = r/n

    # The 'integral' for loop.
    for i in range(0, n):
        x += dx
        dy = y - (((r ** 2) - (x ** 2)) ** 0.5)

        dr = ((dx ** 2) + (dy ** 2)) ** (1/2)

        y -= dy

        calc_circ += dr

    # Multiply by 4 for each quadrant.
    calc_circ *= 4

    # Error calculation.
    error = (actual_circ - calc_circ) / actual_circ * 100

    # Display.
    print("For n =", j)
    print("Actual value of circumference is:", round(actual_circ, 5))
    print("Calculated value of circumference is:", round(calc_circ.real, 5))
    print("The deviation error is:", round(error.real, 5), "%")

    # Return the error value for plotting.
    return error

# Empty lists to store the error values and the 'n' values.
errors = []
n_values = []

# Get the error values for multiple 'n'.
for j in range(10, 101, 3):
    n_values.append(j)
    error = integrate(j)
    errors.append(error)

# Plotting.
plt.plot(n_values, errors)
plt.title("Deviation vs \'n\' graph")
plt.xlabel("Number of divisions (n)")
plt.ylabel("Deviation error (%)")
plt.show()
