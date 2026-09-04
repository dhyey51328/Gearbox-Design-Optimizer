import math
import pandas as pd

from src.gear_calculations import (
    calculate_target_ratio,
    calculate_input_torque,
    calculate_gear_pair,
    calculate_gear_geometry,
    calculate_gear_forces
)

from src.stress_analysis import (
    analyze_gear_bending
)

from src.shaft_design import (
    select_shaft_diameter
)

from src.bearing_design import (
    select_bearing
)

from src.materials import (
    load_materials
)


STANDARD_MODULES_MM = [
    1.5,
    2.0,
    2.5,
    3.0,
    4.0
]


FACE_WIDTH_FACTORS = [
    8,
    10,
    12
]


def cylinder_mass(
    diameter_mm,
    length_mm,
    density_kg_m3
):
    diameter_m = (
        diameter_mm / 1000
    )

    length_m = (
        length_mm / 1000
    )

    volume = (
        math.pi
        * diameter_m ** 2
        / 4
        * length_m
    )

    return (
        volume
        * density_kg_m3
    )


def estimate_rotating_mass(
    geometry,
    face_width_mm,
    input_shaft,
    output_shaft,
    bearing_span_mm,
    density_kg_m3,
    input_bearing,
    output_bearing
):
    pinion_mass = cylinder_mass(
        geometry[
            "pinion_pitch_diameter"
        ],
        face_width_mm,
        density_kg_m3
    )

    gear_mass = cylinder_mass(
        geometry[
            "gear_pitch_diameter"
        ],
        face_width_mm,
        density_kg_m3
    )

    shaft_length_mm = (
        bearing_span_mm + 40
    )

    input_shaft_mass = cylinder_mass(
        input_shaft["diameter_mm"],
        shaft_length_mm,
        density_kg_m3
    )

    output_shaft_mass = cylinder_mass(
        output_shaft["diameter_mm"],
        shaft_length_mm,
        density_kg_m3
    )

    bearing_mass = (
        2 * input_bearing["mass_kg"]
        + 2 * output_bearing["mass_kg"]
    )

    total_mass = (
        pinion_mass
        + gear_mass
        + input_shaft_mass
        + output_shaft_mass
        + bearing_mass
    )

    return total_mass


def optimize_gearbox(
    power_kw,
    input_rpm,
    desired_output_rpm,
    materials_path,
    required_life_hours=10000,
    minimum_gear_fos=2.0,
    minimum_shaft_fos=2.0,
    max_ratio_error_percent=1.0,
    max_center_distance_mm=300,
    pressure_angle_deg=20.0,
    efficiency=0.97,
    service_factor=1.25
):
    target_ratio = calculate_target_ratio(
        input_rpm,
        desired_output_rpm
    )

    if target_ratio <= 1:
        raise ValueError(
            "This version of GearOpt "
            "is designed for speed-reduction "
            "gearboxes where input RPM is "
            "greater than output RPM."
        )

    input_torque = calculate_input_torque(
        power_kw,
        input_rpm
    )

    materials = load_materials(
        materials_path
    )

    valid_designs = []

    evaluated_designs = 0

    rejected_ratio = 0
    rejected_packaging = 0
    rejected_gear = 0
    rejected_shaft = 0
    rejected_bearing = 0

    for material in materials:

        yield_strength = (
            material[
                "yield_strength_mpa"
            ]
        )

        density = (
            material[
                "density_kg_m3"
            ]
        )

        for pinion_teeth in range(
            18,
            41
        ):

            gear_pair = (
                calculate_gear_pair(
                    target_ratio,
                    pinion_teeth
                )
            )

            gear_teeth = (
                gear_pair[
                    "gear_teeth"
                ]
            )

            if gear_teeth <= pinion_teeth:
                continue

            if gear_teeth > 220:
                continue

            for module in (
                STANDARD_MODULES_MM
            ):

                geometry = (
                    calculate_gear_geometry(
                        pinion_teeth,
                        gear_teeth,
                        module
                    )
                )

                for width_factor in (
                    FACE_WIDTH_FACTORS
                ):

                    evaluated_designs += 1

                    face_width = (
                        width_factor
                        * module
                    )

                    ratio_error = (
                        gear_pair[
                            "ratio_error_percent"
                        ]
                    )

                    if (
                        ratio_error
                        > max_ratio_error_percent
                    ):
                        rejected_ratio += 1
                        continue

                    if (
                        geometry[
                            "center_distance"
                        ]
                        > max_center_distance_mm
                    ):
                        rejected_packaging += 1
                        continue

                    basic_forces = (
                        calculate_gear_forces(
                            input_torque,
                            geometry[
                                "pinion_pitch_diameter"
                            ],
                            pressure_angle_deg
                        )
                    )

                    design_tangential_force = (
                        basic_forces[
                            "tangential_force"
                        ]
                        * service_factor
                    )

                    design_radial_force = (
                        basic_forces[
                            "radial_force"
                        ]
                        * service_factor
                    )

                    design_normal_force = (
                        basic_forces[
                            "normal_force"
                        ]
                        * service_factor
                    )

                    gear_analysis = (
                        analyze_gear_bending(
                            design_tangential_force,
                            pinion_teeth,
                            gear_teeth,
                            face_width,
                            module,
                            yield_strength
                        )
                    )

                    if (
                        gear_analysis[
                            "minimum_gear_fos"
                        ]
                        < minimum_gear_fos
                    ):
                        rejected_gear += 1
                        continue

                    actual_ratio = (
                        gear_pair[
                            "actual_ratio"
                        ]
                    )

                    actual_output_rpm = (
                        input_rpm
                        / actual_ratio
                    )

                    ideal_output_torque = (
                        input_torque
                        * actual_ratio
                    )

                    output_torque = (
                        ideal_output_torque
                        * efficiency
                    )

                    transverse_force = (
                        math.sqrt(
                            design_tangential_force
                            ** 2
                            +
                            design_radial_force
                            ** 2
                        )
                    )

                    bearing_span = max(
                        80.0,
                        4.0 * face_width
                    )

                    input_design_torque = (
                        input_torque
                        * service_factor
                    )

                    output_design_torque = (
                        output_torque
                        * service_factor
                    )

                    input_shaft = (
                        select_shaft_diameter(
                            input_design_torque,
                            transverse_force,
                            bearing_span,
                            yield_strength,
                            minimum_shaft_fos
                        )
                    )

                    output_shaft = (
                        select_shaft_diameter(
                            output_design_torque,
                            transverse_force,
                            bearing_span,
                            yield_strength,
                            minimum_shaft_fos
                        )
                    )

                    if (
                        input_shaft is None
                        or output_shaft is None
                    ):
                        rejected_shaft += 1
                        continue

                    load_per_bearing = (
                        transverse_force
                        / 2
                    )

                    input_bearing = (
                        select_bearing(
                            input_shaft[
                                "diameter_mm"
                            ],
                            load_per_bearing,
                            input_rpm,
                            required_life_hours
                        )
                    )

                    output_bearing = (
                        select_bearing(
                            output_shaft[
                                "diameter_mm"
                            ],
                            load_per_bearing,
                            actual_output_rpm,
                            required_life_hours
                        )
                    )

                    if (
                        input_bearing is None
                        or output_bearing is None
                    ):
                        rejected_bearing += 1
                        continue

                    rotating_mass = (
                        estimate_rotating_mass(
                            geometry,
                            face_width,
                            input_shaft,
                            output_shaft,
                            bearing_span,
                            density,
                            input_bearing,
                            output_bearing
                        )
                    )

                    speed_error_percent = (
                        abs(
                            actual_output_rpm
                            - desired_output_rpm
                        )
                        / desired_output_rpm
                    ) * 100

                    valid_designs.append(
                        {
                            "material":
                                material["name"],

                            "pinion_teeth":
                                pinion_teeth,

                            "gear_teeth":
                                gear_teeth,

                            "module_mm":
                                module,

                            "face_width_mm":
                                face_width,

                            "actual_ratio":
                                actual_ratio,

                            "ratio_error_percent":
                                ratio_error,

                            "actual_output_rpm":
                                actual_output_rpm,

                            "speed_error_percent":
                                speed_error_percent,

                            "pinion_pitch_diameter_mm":
                                geometry[
                                    "pinion_pitch_diameter"
                                ],

                            "gear_pitch_diameter_mm":
                                geometry[
                                    "gear_pitch_diameter"
                                ],

                            "center_distance_mm":
                                geometry[
                                    "center_distance"
                                ],

                            "input_torque_nm":
                                input_torque,

                            "output_torque_nm":
                                output_torque,

                            "tangential_force_n":
                                design_tangential_force,

                            "radial_force_n":
                                design_radial_force,

                            "normal_force_n":
                                design_normal_force,

                            "pinion_bending_stress_mpa":
                                gear_analysis[
                                    "pinion_bending_stress"
                                ],

                            "gear_bending_stress_mpa":
                                gear_analysis[
                                    "gear_bending_stress"
                                ],

                            "gear_fos":
                                gear_analysis[
                                    "minimum_gear_fos"
                                ],

                            "input_shaft_diameter_mm":
                                input_shaft[
                                    "diameter_mm"
                                ],

                            "input_shaft_fos":
                                input_shaft[
                                    "factor_of_safety"
                                ],

                            "output_shaft_diameter_mm":
                                output_shaft[
                                    "diameter_mm"
                                ],

                            "output_shaft_fos":
                                output_shaft[
                                    "factor_of_safety"
                                ],

                            "bearing_span_mm":
                                bearing_span,

                            "input_bearing":
                                input_bearing[
                                    "designation"
                                ],

                            "input_bearing_life_hours":
                                input_bearing[
                                    "life_hours"
                                ],

                            "output_bearing":
                                output_bearing[
                                    "designation"
                                ],

                            "output_bearing_life_hours":
                                output_bearing[
                                    "life_hours"
                                ],

                            "estimated_rotating_mass_kg":
                                rotating_mass
                        }
                    )

    results = pd.DataFrame(
        valid_designs
    )

    if not results.empty:

        results = results.sort_values(
            by=[
                "estimated_rotating_mass_kg",
                "ratio_error_percent"
            ],
            ascending=[
                True,
                True
            ]
        )

        results = results.reset_index(
            drop=True
        )

        results.insert(
            0,
            "design_id",
            range(
                1,
                len(results) + 1
            )
        )

    statistics = {
        "evaluated_designs":
            evaluated_designs,

        "valid_designs":
            len(valid_designs),

        "rejected_ratio":
            rejected_ratio,

        "rejected_packaging":
            rejected_packaging,

        "rejected_gear":
            rejected_gear,

        "rejected_shaft":
            rejected_shaft,

        "rejected_bearing":
            rejected_bearing
    }

    return results, statistics