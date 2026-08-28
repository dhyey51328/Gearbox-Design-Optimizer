def select_gear_pair(target_ratio, min_pinion_teeth=18, max_pinion_teeth=40):
    best_design = None
    smallest_error = float("inf")

    for pinion_teeth in range(min_pinion_teeth, max_pinion_teeth + 1):

        gear_teeth = round(target_ratio * pinion_teeth)

        actual_ratio = gear_teeth / pinion_teeth

        ratio_error = abs(actual_ratio - target_ratio)

        if ratio_error < smallest_error:
            smallest_error = ratio_error

            best_design = {
                "pinion_teeth": pinion_teeth,
                "gear_teeth": gear_teeth,
                "actual_ratio": actual_ratio,
                "ratio_error": ratio_error
            }

    return best_design
def calculate_gear_geometry(pinion_teeth, gear_teeth, module):
    pinion_pitch_diameter = module * pinion_teeth
    gear_pitch_diameter = module * gear_teeth

    center_distance = (
        pinion_pitch_diameter + gear_pitch_diameter
    ) / 2

    return {
        "pinion_pitch_diameter": pinion_pitch_diameter,
        "gear_pitch_diameter": gear_pitch_diameter,
        "center_distance": center_distance
    }