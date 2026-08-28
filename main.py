import math


print("====================================")
print("        GEAROPT DESIGN TOOL")
print("====================================")


# USER INPUTS

power_kw = float(input("Enter motor power (kW): "))
input_rpm = float(input("Enter input speed (RPM): "))
output_rpm = float(input("Enter desired output speed (RPM): "))


# CONVERSIONS

power_w = power_kw * 1000


# GEAR RATIO

gear_ratio = input_rpm / output_rpm


# INPUT TORQUE

angular_velocity = (2 * math.pi * input_rpm) / 60

input_torque = power_w / angular_velocity


# IDEAL OUTPUT TORQUE

output_torque = input_torque * gear_ratio


# OUTPUT

print("\n====================================")
print("          DESIGN RESULTS")
print("====================================")

print(f"Gear Ratio: {gear_ratio:.2f}:1")
print(f"Input Torque: {input_torque:.2f} N·m")
print(f"Output Torque: {output_torque:.2f} N·m")

print("====================================")