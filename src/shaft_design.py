import math


STANDARD_SHAFT_DIAMETERS_MM = [
    15,
    17,
    20,
    25,
    30,
    35,
    40
]


def calculate_max_bending_moment(
    transverse_force_n,
    bearing_span_mm
):
    """
    Simplified shaft model:

    Gear is centered between two
    bearings.

    For a centered point load:

    Mmax = F * L / 4
    """

    return (
        transverse_force_n
        * bearing_span_mm
        / 4
    )


def calculate_shaft_stress(
    diameter_mm,
    torque_nm,
    transverse_force_n,
    bearing_span_mm
):
    torque_nmm = torque_nm * 1000

    bending_moment_nmm = (
        calculate_max_bending_moment(
            transverse_force_n,
            bearing_span_mm
        )
    )

    bending_stress = (
        32
        * bending_moment_nmm
        / (
            math.pi
            * diameter_mm ** 3
        )
    )

    torsional_stress = (
        16
        * torque_nmm
        / (
            math.pi
            * diameter_mm ** 3
        )
    )

    von_mises_stress = math.sqrt(
        bending_stress ** 2
        + 3 * torsional_stress ** 2
    )

    return {
        "bending_moment_nmm":
            bending_moment_nmm,

        "bending_stress_mpa":
            bending_stress,

        "torsional_stress_mpa":
            torsional_stress,

        "von_mises_stress_mpa":
            von_mises_stress
    }


def select_shaft_diameter(
    torque_nm,
    transverse_force_n,
    bearing_span_mm,
    yield_strength_mpa,
    minimum_fos,
    candidate_diameters=None
):
    if candidate_diameters is None:
        candidate_diameters = (
            STANDARD_SHAFT_DIAMETERS_MM
        )

    for diameter in candidate_diameters:

        stress = calculate_shaft_stress(
            diameter,
            torque_nm,
            transverse_force_n,
            bearing_span_mm
        )

        von_mises = (
            stress[
                "von_mises_stress_mpa"
            ]
        )

        if von_mises <= 0:
            fos = float("inf")
        else:
            fos = (
                yield_strength_mpa
                / von_mises
            )

        if fos >= minimum_fos:
            return {
                "diameter_mm":
                    diameter,

                "factor_of_safety":
                    fos,

                **stress
            }

    return None