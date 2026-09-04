import matplotlib.pyplot as plt


def plot_top_designs(
    results,
    output_path,
    number_of_designs=10
):
    top_designs = results.head(
        number_of_designs
    )

    labels = [
        f"D{int(value)}"
        for value
        in top_designs["design_id"]
    ]

    masses = (
        top_designs[
            "estimated_rotating_mass_kg"
        ]
    )

    plt.figure(
        figsize=(10, 6)
    )

    plt.bar(
        labels,
        masses
    )

    plt.xlabel(
        "Optimized Design"
    )

    plt.ylabel(
        "Estimated Rotating Mass (kg)"
    )

    plt.title(
        "Top Gearbox Designs by Estimated Mass"
    )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300
    )

    plt.close()


def plot_mass_vs_size(
    results,
    output_path
):
    plt.figure(
        figsize=(8, 6)
    )

    plt.scatter(
        results[
            "center_distance_mm"
        ],
        results[
            "estimated_rotating_mass_kg"
        ]
    )

    plt.xlabel(
        "Gear Center Distance (mm)"
    )

    plt.ylabel(
        "Estimated Rotating Mass (kg)"
    )

    plt.title(
        "Gearbox Size vs Estimated Mass"
    )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300
    )

    plt.close()