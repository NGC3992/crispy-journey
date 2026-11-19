import cv2
import numpy as np
import matplotlib.pyplot as plt

# Constants.
VIDEO = "/Users/aaraviyer/Documents/Code/IISER-K/PH1101-Project/Data/vid_2_slow.mp4"

# The video was recorded in 1/8x slow motion.
SLOW_MOTION_FACTOR = 8

# Measure the ball every N video frames.
FRAME_STEP = 3

# Distance between the two calibration points in m.
CALIBRATION_DISTANCE = 0.80

# Distance at which we stop tracking.
STOP_DISTANCE = 0.80


# Load the video.
cap = cv2.VideoCapture(VIDEO)

if not cap.isOpened():
    raise RuntimeError("Could not open video.")

fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# The video file is ~30 FPS, but it is 1/8x slow motion.
real_fps = fps * SLOW_MOTION_FACTOR

print(f"Video FPS: {fps:.2f}")
print(f"Frames: {frame_count}")
print(f"Video duration: {frame_count / fps:.2f} s")
print(f"Estimated real FPS: {real_fps:.2f}")


# Calibration
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

ret, frame = cap.read()

if not ret:
    raise RuntimeError("Could not read video.")

calibration_points = []

def calibration_callback(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        calibration_points.append((x, y))
        print(
            f"Calibration point {len(calibration_points)}: "
            f"({x}, {y})"
        )

print("\nCALIBRATION")
print("Click the 0 cm point FIRST.")
print("Click the 80 cm point SECOND.")

cv2.namedWindow("Calibration")
cv2.setMouseCallback("Calibration", calibration_callback)

while len(calibration_points) < 2:
    display = frame.copy()
    for point in calibration_points:
        cv2.circle(
            display,
            point,
            6,
            (0, 0, 255),
            -1
        )

    cv2.imshow("Calibration", display)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        cap.release()
        cv2.destroyAllWindows()
        raise SystemExit

cv2.destroyWindow("Calibration")


# Calculate the distance between the calibration points (in pixels).
y_top = calibration_points[0][1]
y_bottom = calibration_points[1][1]

pixel_distance = abs(y_bottom - y_top)

if pixel_distance == 0:
    raise RuntimeError(
        "Calibration points have the same vertical position."
    )

metres_per_pixel = (
    CALIBRATION_DISTANCE / pixel_distance
)


# Find the 80cm position.
# 80 cm is 80/90 of the way from the 0 cm mark to the 90 cm mark.

eighty_cm_pixel = (
    y_top
    + (STOP_DISTANCE / CALIBRATION_DISTANCE)
    * (y_bottom - y_top)
)

print("\nCALIBRATION RESULTS")
print(f"80 cm = {pixel_distance:.2f} pixels")
print(f"Scale = {metres_per_pixel:.6f} m/pixel")
print(f"80 cm mark = y = {eighty_cm_pixel:.2f} pixels")


# Find the release frame.
print("\nFIND RELEASE FRAME")
print("A = previous frame")
print("D = next frame")
print("ENTER = select frame")
print("ESC = quit")

cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

frame_number = 0

while True:
    cap.set(
        cv2.CAP_PROP_POS_FRAMES,
        frame_number
    )

    ret, frame = cap.read()

    if not ret:
        break
    display = frame.copy()

    cv2.putText(
        display,
        f"Frame: {frame_number}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        display,
        "A: previous   D: next   ENTER: select",
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "Find Release Frame",
        display
    )

    key = cv2.waitKey(0) & 0xFF

    if key == 27:
        cap.release()
        cv2.destroyAllWindows()
        raise SystemExit

    elif key == 13:
        break

    elif key == ord("d"):
        frame_number += 1


    elif key == ord("a"):
        frame_number = max(
            0,
            frame_number - 1
        )

cv2.destroyWindow(
    "Find Release Frame"
)

release_frame = frame_number

print(
    f"Release frame selected: {release_frame}"
)


# Use computer vision to locate the ball.
def detect_ball(frame, frame_number):
    # Convert image from BGR to HSV.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Golden/brown colour range.
    lower = np.array([5, 60, 40])
    upper = np.array([35, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)

    # Restrict detection to the approximate ball path.
    roi = np.zeros_like(mask)
    roi[100:830, 190:290] = 255

    mask = cv2.bitwise_and(mask, roi)

    # Remove small noise.
    mask = cv2.medianBlur(mask, 5)

    # Find contours.
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    candidates = []

    for contour in contours:
        area = cv2.contourArea(contour)

        if area < 400:
            continue

        # Find enclosing circle.
        (x, y), radius = cv2.minEnclosingCircle(contour)

        if not (12 <= radius <= 30):
            continue

        # Check circularity.
        perimeter = cv2.arcLength(contour, True)

        if perimeter == 0:
            continue

        circularity = (
            4 * np.pi * area / (perimeter ** 2)
        )

        if circularity < 0.65:
            continue

        candidates.append((x, y, radius))

    if len(candidates) == 0:
        print(f"Ball not detected in frame {frame_number}")
        return None

    # Select the largest candidate.
    x, y, radius = max(
        candidates,
        key=lambda item: item[2]
    )

    # Bottommost point of the ball.
    ball_x = int(round(x))
    ball_y = int(round(y + radius))
    display = frame.copy()

    cv2.circle(
        display,
        (ball_x, ball_y),
        5,
        (0, 0, 255),
        -1
    )

    cv2.circle(
        display,
        (ball_x, int(round(y))),
        int(round(radius)),
        (0, 255, 0),
        2
    )

    cv2.imshow("Automatic Ball Tracking", display)
    cv2.waitKey(100)
    return ball_x, ball_y


# Collect ball position data.
frame_steps = range(3,4)

accepted_g = 9.81
errors = []
measured_g_values = []

for FRAME_STEP in frame_steps:
    print("\n" + "=" * 50)
    print(f"RUNNING EXPERIMENT: FRAME STEP = {FRAME_STEP}")
    print("=" * 50)

    times = []
    pixel_positions = []

    # Reset video to release frame.
    cap.set(cv2.CAP_PROP_POS_FRAMES, release_frame)

    frame_number = release_frame

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if (frame_number - release_frame) % FRAME_STEP == 0:
            detected = detect_ball(frame, frame_number)

            if detected is not None:
                ball_x, ball_y = detected

                time = (
                    frame_number - release_frame
                ) / real_fps

                times.append(time)
                pixel_positions.append(ball_y)

                print(
                    f"Frame {frame_number}: "
                    f"t = {time:.4f} s, "
                    f"x = {ball_x}, y = {ball_y}"
                )

                if ball_y >= eighty_cm_pixel:
                    print("\nBall reached the 80 cm mark.")
                    break

        frame_number += 1

    # Check if the data is usable.
    if len(times) < 3:
        print("Not enough measurements. Skipping this frame step.")
        continue

    times = np.array(times)
    pixel_positions = np.array(pixel_positions)

    # Convert pixels to distance.
    distance_pixels = pixel_positions - pixel_positions[0]

    distance_metres = distance_pixels * metres_per_pixel

    # Fit the free-fall equation
    coefficients = np.polyfit(
        times,
        distance_metres,
        2
    )

    A = coefficients[0]
    u = coefficients[1]
    C = coefficients[2]

    g = 2 * A

    # Percentage error calculation.
    percentage_error = (
        abs(g - accepted_g) / accepted_g
    ) * 100

    measured_g_values.append(g)
    errors.append(percentage_error)

    # Display results.
    print("\nRESULTS")
    print(f"Frame step          : {FRAME_STEP}")
    print(f"Measurements        : {len(times)}")
    print(f"Initial velocity    : {u:.4f} m/s")
    print(f"Measured g          : {g:.4f} m/s²")
    print(f"Percentage error    : {percentage_error:.2f}%")


# Release the video.
cap.release()
cv2.destroyAllWindows()


# Frame step vs percentage error graph.
completed_steps = [
    step for step, error in zip(frame_steps, errors)
]

plt.figure(figsize=(9, 6))

plt.plot(
    completed_steps,
    errors,
    marker="o",
    linestyle="-",
    label="Percentage error"
)

plt.xlabel("Frame step")
plt.ylabel("Percentage error (%)")

plt.title("Effect of Frame Step on Measurement of g")

plt.xticks(list(frame_steps))
plt.grid()
plt.legend()

plt.tight_layout()

plt.savefig("frame_step_vs_error.png", dpi=300)

# Plotting.
fitted_distance = np.polyval(coefficients, times)
plt.figure(
    figsize=(8, 6)
)

plt.scatter(
    times,
    distance_metres,
    label="Experimental data"
)

plt.plot(
    times,
    fitted_distance,
    label=f"Quadratic fit (g = {g:.2f} m/s²)"
)

plt.xlabel(
    "Time (s)"
)

plt.ylabel(
    "Distance fallen (m)"
)

plt.title(
    "Measurement of g Using Video Analysis"
)

plt.grid()
plt.legend()

plt.tight_layout()

plt.savefig("distance_time_1.png", dpi=300)

# v-t graph.
velocity = 2 * A * times + u

plt.figure(figsize=(8, 6))

plt.plot(
    times,
    velocity,
    label=f"Velocity (g = {g:.2f} m/s²)"
)

plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.title("Velocity-Time Graph")

plt.grid()
plt.legend()
plt.tight_layout()

plt.savefig("velocity_time_1.png", dpi=300)

plt.show()