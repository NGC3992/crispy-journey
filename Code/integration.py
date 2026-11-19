# Program to calculate the perimeter of a circle using the concept of line integral.
# Also verifies the fact that the deviation error between the calculated value and
# actual value decreases as the number of divisions increases.

# Imports.
import math
import matplotlib.pyplot as plt

# Inputs.
#
# @input r -- radius of circle

r = float(input("Enter the radius of the circle: "))

# Function to calculate the circumference by repeated summing.
#
# @param n -- the number of iterations to be done
def line_integral(n):
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
    abs_error = abs((actual_circ - calc_circ) / actual_circ * 100)

    # Display.
    print("For n =", n)
    print("Actual value of circumference is:", round(actual_circ, 5))
    print("Calculated value of circumference is:", round(calc_circ.real, 5))
    print("The deviation error is:", round(abs_error.real, 5), "%")

    # Return the error value for plotting.
    return abs_error

# Function to calculate the area of the circle by repeated summing.
# 
# @ param n -- the number of iterations to be done
def calc_area(n):
    # Define the variables.
    calc_ar = 0
    actual_ar = math.pi * (r ** 2)
    x = 0
    y = 0
    dx = dy = r / n

    # Looping through x and y.
    for i in range(n):
        x += dx
        for j in range(n):
            y += dy
            if (x ** 2) + (y ** 2) < (r ** 2):
                calc_ar += dx * dy
        y = 0

    # Calculations.
    calc_ar *= 4
    abs_error = abs((calc_ar - actual_ar) / (actual_ar) * 100)

    # Display.
    print("For n =", n)
    print("Actual value of area is:", round(actual_ar, 5))
    print("Calculated value of area is:", round(calc_ar.real, 5))
    print("The deviation error is:", round(error.real, 5), "%")

    return abs_error

# Empty lists to store the error values and the 'n' values.
circumference_errors = []
area_errors = []
n_values = []

# Get the error values for multiple 'n'.
for j in range(10, 101, 3):
    n_values.append(j)
    error = line_integral(j)
    circumference_errors.append(error)

for k in range(10, 101, 3):
    error = calc_area(k)
    area_errors.append(error)

# Plotting the circumference errors.
plt.figure(1)
plt.plot(n_values, circumference_errors)
plt.title("Deviation vs \'n\' graph for circumference of a circle")
plt.xlabel("Number of divisions (n)")
plt.ylabel("Deviation error (%)")

# Plotting the area errors.
plt.figure(2)
plt.plot(n_values, area_errors)
plt.title("Deviation vs \'n\' graph for area of a circle.")
plt.xlabel("Number of divisions (n)")
plt.ylabel("Deviation error (%)")

plt.show()
