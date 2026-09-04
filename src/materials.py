import csv


def load_materials(csv_path):
    materials = []

    with open(
        csv_path,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            materials.append(
                {
                    "name":
                        row["name"],

                    "yield_strength_mpa":
                        float(
                            row[
                                "yield_strength_mpa"
                            ]
                        ),

                    "density_kg_m3":
                        float(
                            row[
                                "density_kg_m3"
                            ]
                        ),

                    "elastic_modulus_gpa":
                        float(
                            row[
                                "elastic_modulus_gpa"
                            ]
                        )
                }
            )

    return materials