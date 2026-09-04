import math


def calculate_target_ratio(input_rpm, desired_output_rpm):
    return input_rpm / desired_output_rpm


def calculate_input_torque(power_kw, input_rpm):
    power_w = power_kw * 1000

    angular_velocity = (
        2 * math.pi * input_rpm
    ) / 60

    torque = power_w / angular_velocity

    return torque


def calculate_gear_pair(target_ratio, pinion_teeth):
    gear_teeth = round(
        target_ratio * pinion_teeth
    )

    actual_ratio = (
        gear_teeth / pinion_teeth
    )

    ratio_error_percent = (
        abs(actual_ratio - target_ratio)
        / target_ratio
    ) * 100

    return {
        "pinion_teeth": pinion_teeth,
        "gear_teeth": gear_teeth,
        "actual_ratio": actual_ratio,
        "ratio_error_percent": ratio_error_percent
    }


def select_gear_pair(
    target_ratio,
    min_pinion_teeth=18,
    max_pinion_teeth=40
):
    best_design = None
    smallest_error = float("inf")

    for pinion_teeth in range(
        min_pinion_teeth,
        max_pinion_teeth + 1
    ):
        design = calculate_gear_pair(
            target_ratio,
            pinion_teeth
        )

        error = design["ratio_error_percent"]

        if error < smallest_error:
            smallest_error = error
            best_design = design

    return best_design


def calculate_gear_geometry(
    pinion_teeth,
    gear_teeth,
    module
):
    pinion_pitch_diameter = (
        module * pinion_teeth
    )

    gear_pitch_diameter = (
        module * gear_teeth
    )

    center_distance = (
        pinion_pitch_diameter
        + gear_pitch_diameter
    ) / 2

    return {
        "pinion_pitch_diameter":
            pinion_pitch_diameter,

        "gear_pitch_diameter":
            gear_pitch_diameter,

        "center_distance":
            center_distance
    }


def calculate_gear_forces(
    torque_nm,
    pitch_diameter_mm,
    pressure_angle_deg=20.0
):
    pitch_diameter_m = (
        pitch_diameter_mm / 1000
    )

    tangential_force = (
        2 * torque_nm
    ) / pitch_diameter_m

    pressure_angle_rad = math.radians(
        pressure_angle_deg
    )

    radial_force = (
        tangential_force
        * math.tan(pressure_angle_rad)
    )

    normal_force = (
        tangential_force
        / math.cos(pressure_angle_rad)
    )

    return {
        "tangential_force":
            tangential_force,

        "radial_force":
            radial_force,

        "normal_force":
            normal_force
    }