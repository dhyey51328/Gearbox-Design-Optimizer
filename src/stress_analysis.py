def calculate_lewis_form_factor(
    number_of_teeth
):
    """
    Approximate Lewis form factor for
    standard 20-degree full-depth
    involute spur gears.
    """

    return (
        0.484
        - (2.87 / number_of_teeth)
    )


def calculate_gear_bending_stress(
    tangential_force,
    face_width_mm,
    module_mm,
    lewis_factor
):
    """
    Lewis bending stress.

    N / mm^2 = MPa
    """

    stress = (
        tangential_force
        / (
            face_width_mm
            * module_mm
            * lewis_factor
        )
    )

    return stress


def calculate_factor_of_safety(
    allowable_stress_mpa,
    actual_stress_mpa
):
    if actual_stress_mpa <= 0:
        return float("inf")

    return (
        allowable_stress_mpa
        / actual_stress_mpa
    )


def analyze_gear_bending(
    tangential_force,
    pinion_teeth,
    gear_teeth,
    face_width_mm,
    module_mm,
    allowable_stress_mpa
):
    pinion_factor = (
        calculate_lewis_form_factor(
            pinion_teeth
        )
    )

    gear_factor = (
        calculate_lewis_form_factor(
            gear_teeth
        )
    )

    pinion_stress = (
        calculate_gear_bending_stress(
            tangential_force,
            face_width_mm,
            module_mm,
            pinion_factor
        )
    )

    gear_stress = (
        calculate_gear_bending_stress(
            tangential_force,
            face_width_mm,
            module_mm,
            gear_factor
        )
    )

    pinion_fos = (
        calculate_factor_of_safety(
            allowable_stress_mpa,
            pinion_stress
        )
    )

    gear_fos = (
        calculate_factor_of_safety(
            allowable_stress_mpa,
            gear_stress
        )
    )

    return {
        "pinion_lewis_factor":
            pinion_factor,

        "gear_lewis_factor":
            gear_factor,

        "pinion_bending_stress":
            pinion_stress,

        "gear_bending_stress":
            gear_stress,

        "pinion_fos":
            pinion_fos,

        "gear_fos":
            gear_fos,

        "minimum_gear_fos":
            min(pinion_fos, gear_fos)
    }