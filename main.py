import math

from src.gear_calculations import (
    select_gear_pair,
    calculate_gear_geometry
)


print("====================================")
print("        GEAROPT DESIGN TOOL")
print("====================================")


# USER INPUTS

power_kw = float(input("Enter motor power (kW): "))
input_rpm = float(input("Enter input speed (RPM): "))
output_rpm = float(input("Enter desired output speed (RPM): "))


# CURRENT DESIGN ASSUMPTION

module = 2.0


# POWER CONVERSION

power_w = power_kw * 1000


# TARGET GEAR RATIO

target_ratio = input_rpm / output_rpm


# INPUT TORQUE

angular_velocity = (2 * math.pi * input_rpm) / 60

input_torque = power_w / angular_velocity


# SELECT GEAR PAIR

gear_design = select_gear_pair(target_ratio)

pinion_teeth = gear_design["pinion_teeth"]
gear_teeth = gear_design["gear_teeth"]

actual_ratio = gear_design["actual_ratio"]

ratio_error = gear_design["ratio_error"]

ratio_error_percent = (
    ratio_error / target_ratio
) * 100

# CALCULATE ACTUAL OUTPUT SPEED

actual_output_rpm = input_rpm / actual_ratio

speed_error = actual_output_rpm - output_rpm

speed_error_percent = (
    abs(speed_error) / output_rpm
) * 100

# IDEAL OUTPUT TORQUE

output_torque = input_torque * actual_ratio


# CALCULATE GEAR GEOMETRY

geometry = calculate_gear_geometry(
    pinion_teeth,
    gear_teeth,
    module
)


# OUTPUT RESULTS

print("\n====================================")
print("          DESIGN RESULTS")
print("====================================")

print(f"Target Gear Ratio: {target_ratio:.3f}:1")
print(f"Actual Gear Ratio: {actual_ratio:.3f}:1")
print(f"Ratio Error: {ratio_error_percent:.3f}%")

print(f"\nPinion Teeth: {pinion_teeth}")
print(f"Gear Teeth: {gear_teeth}")

print(f"\nModule: {module:.2f} mm")

print(
    f"Pinion Pitch Diameter: "
    f"{geometry['pinion_pitch_diameter']:.2f} mm"
)

print(
    f"Gear Pitch Diameter: "
    f"{geometry['gear_pitch_diameter']:.2f} mm"
)

print(
    f"Center Distance: "
    f"{geometry['center_distance']:.2f} mm"
)

print(f"\nInput Torque: {input_torque:.2f} N·m")
print(f"Output Torque: {output_torque:.2f} N·m")

print(f"\nActual Output Speed: {actual_output_rpm:.2f} RPM")

print(
    f"Output Speed Error: "
    f"{speed_error_percent:.3f}%"
)

print("====================================")