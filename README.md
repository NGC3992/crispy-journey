# crispy-journey
This repo contains all the programs for our physics project for the PH1101 course at IISER Kolkata.

## g_value.py
This is a script that uses a slow motion video of a falling object to calculate the value of the acceleration due to gravity (g).

We have chosen two reference points 80cm away, with the object being dropped from the 0 cm mark. The script uses the opencv computer vision algorithm to identify the position of the object.

## integration.py
This script verifies the fact that line and surfaces integrals are actually just adding infinitesimal units multiple times.

It checks the fact that as we decrease the size of the small unit length, dx, or unit area, dA, the deviation from the ideal value keeps decreasing.

## pendulum.py
This program measures the time period of a simple pendulum numerically and analytically and compares the obtained vales to the standard value obtained by using the small angle approximation.

We notice a slight deviation in the time period as the angle at which the pendulum is released is made larger.
