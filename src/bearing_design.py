BEARING_CATALOG = [
    {
        "designation": "6002",
        "bore_mm": 15,
        "dynamic_rating_n": 5600,
        "mass_kg": 0.030
    },
    {
        "designation": "6203",
        "bore_mm": 17,
        "dynamic_rating_n": 9500,
        "mass_kg": 0.065
    },
    {
        "designation": "6204",
        "bore_mm": 20,
        "dynamic_rating_n": 12800,
        "mass_kg": 0.106
    },
    {
        "designation": "6205",
        "bore_mm": 25,
        "dynamic_rating_n": 14000,
        "mass_kg": 0.129
    },
    {
        "designation": "6206",
        "bore_mm": 30,
        "dynamic_rating_n": 19500,
        "mass_kg": 0.199
    },
    {
        "designation": "6207",
        "bore_mm": 35,
        "dynamic_rating_n": 25700,
        "mass_kg": 0.288
    },
    {
        "designation": "6208",
        "bore_mm": 40,
        "dynamic_rating_n": 29100,
        "mass_kg": 0.366
    }
]


def calculate_l10_life_hours(
    dynamic_rating_n,
    equivalent_load_n,
    rpm,
    exponent=3
):
    """
    Basic L10 life relationship.

    Ball bearing exponent p = 3.
    """

    if (
        equivalent_load_n <= 0
        or rpm <= 0
    ):
        return float("inf")

    life_million_revolutions = (
        dynamic_rating_n
        / equivalent_load_n
    ) ** exponent

    total_revolutions = (
        life_million_revolutions
        * 1_000_000
    )

    life_hours = (
        total_revolutions
        / (60 * rpm)
    )

    return life_hours


def select_bearing(
    bore_mm,
    radial_load_n,
    rpm,
    required_life_hours
):
    possible_bearings = []

    for bearing in BEARING_CATALOG:

        if bearing["bore_mm"] != bore_mm:
            continue

        life_hours = (
            calculate_l10_life_hours(
                bearing["dynamic_rating_n"],
                radial_load_n,
                rpm
            )
        )

        if life_hours >= required_life_hours:
            result = bearing.copy()

            result["life_hours"] = (
                life_hours
            )

            possible_bearings.append(
                result
            )

    if not possible_bearings:
        return None

    possible_bearings.sort(
        key=lambda bearing:
            bearing["mass_kg"]
    )

    return possible_bearings[0]