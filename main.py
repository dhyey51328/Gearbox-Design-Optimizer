from pathlib import Path

from src.optimizer import (
    optimize_gearbox
)

from src.plotting import (
    plot_top_designs,
    plot_mass_vs_size
)


print("==============================================")
print("           GEAROPT DESIGN OPTIMIZER")
print("==============================================")

print(
    "\nPreliminary spur gearbox design tool"
)

print(
    "Lewis bending + shaft von Mises "
    "+ bearing L10 analysis"
)


# ==================================================
# USER INPUTS
# ==================================================

power_kw = float(
    input(
        "\nEnter motor power (kW): "
    )
)

input_rpm = float(
    input(
        "Enter input speed (RPM): "
    )
)

desired_output_rpm = float(
    input(
        "Enter desired output speed (RPM): "
    )
)


# ==================================================
# DESIGN REQUIREMENTS
# ==================================================

required_life_hours = 10000

minimum_gear_fos = 2.0

minimum_shaft_fos = 2.0

max_ratio_error_percent = 1.0

max_center_distance_mm = 300.0

pressure_angle_deg = 20.0

gear_efficiency = 0.97

service_factor = 1.25


# ==================================================
# FILE PATHS
# ==================================================

base_directory = (
    Path(__file__)
    .resolve()
    .parent
)

materials_path = (
    base_directory
    / "data"
    / "materials.csv"
)

results_directory = (
    base_directory
    / "results"
)

results_directory.mkdir(
    exist_ok=True
)


# ==================================================
# RUN OPTIMIZATION
# ==================================================

print(
    "\nSearching candidate gearbox designs..."
)

results, statistics = optimize_gearbox(
    power_kw=power_kw,

    input_rpm=input_rpm,

    desired_output_rpm=
        desired_output_rpm,

    materials_path=
        materials_path,

    required_life_hours=
        required_life_hours,

    minimum_gear_fos=
        minimum_gear_fos,

    minimum_shaft_fos=
        minimum_shaft_fos,

    max_ratio_error_percent=
        max_ratio_error_percent,

    max_center_distance_mm=
        max_center_distance_mm,

    pressure_angle_deg=
        pressure_angle_deg,

    efficiency=
        gear_efficiency,

    service_factor=
        service_factor
)


# ==================================================
# SEARCH SUMMARY
# ==================================================

print(
    "\n=============================================="
)

print(
    "              SEARCH SUMMARY"
)

print(
    "=============================================="
)

print(
    f"Candidate Designs Evaluated: "
    f"{statistics['evaluated_designs']}"
)

print(
    f"Valid Designs: "
    f"{statistics['valid_designs']}"
)

print(
    f"Rejected - Ratio Error: "
    f"{statistics['rejected_ratio']}"
)

print(
    f"Rejected - Packaging: "
    f"{statistics['rejected_packaging']}"
)

print(
    f"Rejected - Gear Strength: "
    f"{statistics['rejected_gear']}"
)

print(
    f"Rejected - Shaft Strength: "
    f"{statistics['rejected_shaft']}"
)

print(
    f"Rejected - Bearing Life: "
    f"{statistics['rejected_bearing']}"
)


# ==================================================
# HANDLE NO VALID DESIGN
# ==================================================

if results.empty:

    print(
        "\nNO VALID DESIGN FOUND"
    )

    print(
        "Try changing the input requirements "
        "or design constraints."
    )

    raise SystemExit


# ==================================================
# BEST DESIGN
# ==================================================

best = results.iloc[0]


print(
    "\n=============================================="
)

print(
    "              OPTIMAL DESIGN"
)

print(
    "=============================================="
)


print(
    f"\nMaterial: "
    f"{best['material']}"
)


print(
    "\n--- GEAR GEOMETRY ---"
)

print(
    f"Pinion Teeth: "
    f"{int(best['pinion_teeth'])}"
)

print(
    f"Gear Teeth: "
    f"{int(best['gear_teeth'])}"
)

print(
    f"Module: "
    f"{best['module_mm']:.2f} mm"
)

print(
    f"Face Width: "
    f"{best['face_width_mm']:.2f} mm"
)

print(
    f"Pinion Pitch Diameter: "
    f"{best['pinion_pitch_diameter_mm']:.2f} mm"
)

print(
    f"Gear Pitch Diameter: "
    f"{best['gear_pitch_diameter_mm']:.2f} mm"
)

print(
    f"Center Distance: "
    f"{best['center_distance_mm']:.2f} mm"
)


print(
    "\n--- SPEED & RATIO ---"
)

print(
    f"Actual Gear Ratio: "
    f"{best['actual_ratio']:.4f}:1"
)

print(
    f"Ratio Error: "
    f"{best['ratio_error_percent']:.4f}%"
)

print(
    f"Actual Output Speed: "
    f"{best['actual_output_rpm']:.2f} RPM"
)

print(
    f"Output Speed Error: "
    f"{best['speed_error_percent']:.4f}%"
)


print(
    "\n--- TORQUE ---"
)

print(
    f"Input Torque: "
    f"{best['input_torque_nm']:.2f} N·m"
)

print(
    f"Output Torque: "
    f"{best['output_torque_nm']:.2f} N·m"
)

print(
    f"Assumed Gear Efficiency: "
    f"{gear_efficiency * 100:.1f}%"
)

print(
    f"Service Factor: "
    f"{service_factor:.2f}"
)


print(
    "\n--- GEAR FORCES ---"
)

print(
    f"Tangential Force: "
    f"{best['tangential_force_n']:.2f} N"
)

print(
    f"Radial Force: "
    f"{best['radial_force_n']:.2f} N"
)

print(
    f"Normal Force: "
    f"{best['normal_force_n']:.2f} N"
)


print(
    "\n--- GEAR STRENGTH ---"
)

print(
    f"Pinion Bending Stress: "
    f"{best['pinion_bending_stress_mpa']:.2f} MPa"
)

print(
    f"Gear Bending Stress: "
    f"{best['gear_bending_stress_mpa']:.2f} MPa"
)

print(
    f"Minimum Gear FOS: "
    f"{best['gear_fos']:.2f}"
)

print(
    f"Required Gear FOS: "
    f"{minimum_gear_fos:.2f}"
)


print(
    "\n--- INPUT SHAFT ---"
)

print(
    f"Diameter: "
    f"{best['input_shaft_diameter_mm']:.0f} mm"
)

print(
    f"Factor of Safety: "
    f"{best['input_shaft_fos']:.2f}"
)


print(
    "\n--- OUTPUT SHAFT ---"
)

print(
    f"Diameter: "
    f"{best['output_shaft_diameter_mm']:.0f} mm"
)

print(
    f"Factor of Safety: "
    f"{best['output_shaft_fos']:.2f}"
)


print(
    "\n--- BEARINGS ---"
)

print(
    f"Input Bearing: "
    f"{best['input_bearing']}"
)

print(
    f"Input Bearing L10 Life: "
    f"{best['input_bearing_life_hours']:.0f} hr"
)

print(
    f"Output Bearing: "
    f"{best['output_bearing']}"
)

print(
    f"Output Bearing L10 Life: "
    f"{best['output_bearing_life_hours']:.0f} hr"
)

print(
    f"Required Bearing Life: "
    f"{required_life_hours:.0f} hr"
)


print(
    "\n--- OPTIMIZATION ---"
)

print(
    f"Estimated Rotating Mass: "
    f"{best['estimated_rotating_mass_kg']:.3f} kg"
)

print(
    f"Valid Candidate Designs: "
    f"{len(results)}"
)

print(
    "\nDesign Status: PASS"
)


# ==================================================
# SAVE RESULTS
# ==================================================

csv_path = (
    results_directory
    / "optimization_results.csv"
)

results.to_csv(
    csv_path,
    index=False
)


# ==================================================
# CREATE PLOTS
# ==================================================

top_designs_plot = (
    results_directory
    / "top_designs.png"
)

mass_size_plot = (
    results_directory
    / "mass_vs_size.png"
)

plot_top_designs(
    results,
    top_designs_plot
)

plot_mass_vs_size(
    results,
    mass_size_plot
)


# ==================================================
# FINAL MESSAGE
# ==================================================

print(
    "\n=============================================="
)

print(
    "                FILE OUTPUTS"
)

print(
    "=============================================="
)

print(
    f"Optimization Results:\n"
    f"{csv_path}"
)

print(
    f"\nTop Designs Plot:\n"
    f"{top_designs_plot}"
)

print(
    f"\nMass vs Size Plot:\n"
    f"{mass_size_plot}"
)
# ==================================================
# SAVE OPTIMAL DESIGN SPECIFICATION
# ==================================================

design_summary_path = (
    results_directory
    / "optimal_design_summary.txt"
)

with open(
    design_summary_path,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "GEAROPT OPTIMAL DESIGN\n"
    )

    file.write(
        "======================\n\n"
    )

    file.write(
        f"Material: "
        f"{best['material']}\n\n"
    )

    file.write(
        "GEAR GEOMETRY\n"
    )

    file.write(
        f"Pinion Teeth: "
        f"{int(best['pinion_teeth'])}\n"
    )

    file.write(
        f"Gear Teeth: "
        f"{int(best['gear_teeth'])}\n"
    )

    file.write(
        f"Module: "
        f"{best['module_mm']:.2f} mm\n"
    )

    file.write(
        f"Face Width: "
        f"{best['face_width_mm']:.2f} mm\n"
    )

    file.write(
        f"Pinion Pitch Diameter: "
        f"{best['pinion_pitch_diameter_mm']:.2f} mm\n"
    )

    file.write(
        f"Gear Pitch Diameter: "
        f"{best['gear_pitch_diameter_mm']:.2f} mm\n"
    )

    file.write(
        f"Center Distance: "
        f"{best['center_distance_mm']:.2f} mm\n\n"
    )

    file.write(
        "PERFORMANCE\n"
    )

    file.write(
        f"Gear Ratio: "
        f"{best['actual_ratio']:.4f}:1\n"
    )

    file.write(
        f"Input Speed: "
        f"{input_rpm:.2f} RPM\n"
    )

    file.write(
        f"Output Speed: "
        f"{best['actual_output_rpm']:.2f} RPM\n"
    )

    file.write(
        f"Input Torque: "
        f"{best['input_torque_nm']:.2f} N.m\n"
    )

    file.write(
        f"Output Torque: "
        f"{best['output_torque_nm']:.2f} N.m\n\n"
    )

    file.write(
        "GEAR LOADS\n"
    )

    file.write(
        f"Tangential Force: "
        f"{best['tangential_force_n']:.2f} N\n"
    )

    file.write(
        f"Radial Force: "
        f"{best['radial_force_n']:.2f} N\n"
    )

    file.write(
        f"Normal Force: "
        f"{best['normal_force_n']:.2f} N\n\n"
    )

    file.write(
        "STRENGTH\n"
    )

    file.write(
        f"Pinion Bending Stress: "
        f"{best['pinion_bending_stress_mpa']:.2f} MPa\n"
    )

    file.write(
        f"Gear Bending Stress: "
        f"{best['gear_bending_stress_mpa']:.2f} MPa\n"
    )

    file.write(
        f"Minimum Gear FOS: "
        f"{best['gear_fos']:.2f}\n\n"
    )

    file.write(
        "SHAFTS\n"
    )

    file.write(
        f"Input Shaft Diameter: "
        f"{best['input_shaft_diameter_mm']:.0f} mm\n"
    )

    file.write(
        f"Output Shaft Diameter: "
        f"{best['output_shaft_diameter_mm']:.0f} mm\n\n"
    )

    file.write(
        "BEARINGS\n"
    )

    file.write(
        f"Input Bearing: "
        f"{best['input_bearing']}\n"
    )

    file.write(
        f"Output Bearing: "
        f"{best['output_bearing']}\n"
    )

    file.write(
        f"Input Bearing L10 Life: "
        f"{best['input_bearing_life_hours']:.0f} hr\n"
    )

    file.write(
        f"Output Bearing L10 Life: "
        f"{best['output_bearing_life_hours']:.0f} hr\n"
    )

    file.write(
        f"\nEstimated Rotating Mass: "
        f"{best['estimated_rotating_mass_kg']:.3f} kg\n"
    )
    print(
    f"\nOptimal Design Summary:\n"
    f"{design_summary_path}"
)
print(
    "\nOptimization complete."
)

print(
    "=============================================="
)