# Imports.
import numpy as np
import matplotlib.pyplot as plt

# Define the constants.
g = 9.81
l = 1.0
alpha = np.sqrt(g / l)
dt = 0.001           
t_max = 10.0        

angles = np.arange(1, 91, 5)
t = np.arange(0, t_max + dt, dt)  

# Function to get the numerical period along with other useful data.
def simulate(phi0_deg, dt=dt , t = t):
    phi0 = np.radians(phi0_deg)
    phi = np.zeros(len(t))
    omega = np.zeros(len(t))

    phi[0] = phi0
    omega[0] = 0.0

    for i in range(len(t) - 1):

        omega[i + 1] = omega[i] - alpha**2 * np.sin(phi[i]) * dt
        phi[i + 1] = phi[i] + omega[i + 1] * dt


    peak_index = np.where((phi[1:-1] > phi[:-2]) & (phi[1:-1] >= phi[2:]))[0] + 1
    time_periods = np.diff(t[peak_index])
    avg_time = np.mean(time_periods)

    return t,phi,omega,time_periods,avg_time

# Using small angle approximation.
T_small = 2 * np.pi * np.sqrt(l / g)

# Function to calculate the analytical period.
def analytical_period(phi0_deg):
    phi0 = np.radians(phi0_deg)
    T = T_small * (1 + 0.25 * (np.sin(phi0 / 2))**2)
    return T

# Empty lists to store the numerical and analytical periods.
numerical_periods = []
analytical_periods = []

# Calculate periods for all angles in the range.
for angle in angles:
    t,phi,omega,time_periods,avg_time = simulate(angle)
    numerical_periods.append(avg_time)
    analytical_periods.append(analytical_period(angle))

numerical_periods = np.array(numerical_periods)
analytical_periods = np.array(analytical_periods)

# Display.
print(f"\nPENDULUM SIMULATION RESULTS\nAngle (degrees) ; Numerical T ; Analytical T")
for i in range(len(angles)):
    print(f"{angle:.1f} ; {numerical_periods[i]:.5f} ; {analytical_periods[i]:.5f}")
print(f"Small-angle theoretical period: {T_small:.5f} s")

# Plotting the x-t graphs for certain angles.
angles_graphs = [10, 30, 50, 70]
for angle in angles_graphs:
    t,phi,omega,time_periods,avg_time = simulate(angle)  
    plt.figure(1)
    plt.plot(
        t,
        np.degrees(phi),
        label=f"{angle} degrees"
    )

plt.xlabel("Time (seconds)")
plt.ylabel("Angular displacement (degrees)")
plt.title("Time vs Nonlinear Simple Pendulum: Angular Displacement")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("disp_time_pendulum.png")

# Plotting the numerical T, analytical T and the small-angle-approximation T.
plt.figure(2)
plt.plot(
    angles,
    numerical_periods,
    color = "deeppink",
    label="Numerical simulation"
)

plt.plot(
    angles,
    analytical_periods,
    color = "blue",
    label="Analytical approximation"
)

plt.axhline(
    T_small,
    color="black",
    linestyle=":",
    label="Small-angle theoretical period"
)

plt.xlabel("Initial angular displacement (degrees)")
plt.ylabel("Time period (seconds)")
plt.title("Time Period vs Initial Angular Displacement")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("period-comparision.png")

# Plotting the percentage deviation error between the numerical and analytical T.
percentage_error = (
    np.abs(numerical_periods - analytical_periods)
    / analytical_periods
) * 100

plt.figure(3,figsize=(10, 6))

plt.plot(
    angles,
    percentage_error,
    'o-'
)

plt.xlabel("Initial angular displacement (degrees)")
plt.ylabel("Percentage difference (%)")
plt.title("Difference Between Numerical and Analytical Periods")
plt.grid()
plt.tight_layout()
plt.savefig("deviation-error.png")
plt.show()
