# GearOpt — Design Validation

## 1. Final Design

GearOpt selected the following gearbox configuration from 630 evaluated candidate designs:

| Parameter | Final Design |
|---|---:|
| Input Power | 5 kW |
| Input Speed | 3500 RPM |
| Target Output Speed | 500 RPM |
| Gear Ratio | 7.00:1 |
| Pinion Teeth | 28 |
| Gear Teeth | 196 |
| Module | 1.50 mm |
| Face Width | 12 mm |
| Pinion Pitch Diameter | 42 mm |
| Gear Pitch Diameter | 294 mm |
| Analytical Center Distance | 168 mm |
| CAD Center Distance | 169 mm |
| Shaft Diameter | 15 mm |
| Bearing | 6002 |
| Material | AISI 4140 Steel |

## 2. Analytical Validation

The optimized design was evaluated using preliminary analytical engineering models for gear loading, gear bending stress, shaft strength, and bearing life.

### Gear Loading

- Input torque: 13.64 N·m
- Output torque: 92.63 N·m
- Tangential gear force: 812.02 N
- Radial gear force: 295.55 N
- Normal gear force: 864.13 N

### Gear Strength

- Pinion bending stress: 118.25 MPa
- Gear bending stress: 96.11 MPa
- Minimum gear factor of safety: 5.54

### Shaft Strength

- Input shaft diameter: 15 mm
- Input shaft factor of safety: 9.55
- Output shaft diameter: 15 mm
- Output shaft factor of safety: 2.13

### Bearing Life

The selected bearing for both shafts was the 6002 deep-groove ball bearing.

- Input bearing calculated L10 life: 10,368 hours
- Output bearing calculated L10 life: 72,577 hours
- Required bearing life: 10,000 hours

Both selected bearings satisfy the preliminary life requirement.

## 3. CAD Validation

The optimized gearbox was recreated as a 3D assembly in AutoCAD.

The CAD assembly includes:

- 28-tooth input pinion
- 196-tooth output gear
- 15 mm input and output shafts
- simplified 6002 bearing geometry
- upper and lower bearing supports
- support plates
- gearbox housing
- mounting/support features

Interference checks were performed on the gear mesh and completed assembly.

| CAD Check | Result |
|---|---|
| Gear Mesh Interference | Clear |
| Rebuilt Bearing/Support Assembly | Clear |
| Full Assembly Interference | Clear |

## 4. Analytical-to-CAD Comparison

| Parameter | Analytical Model | CAD Model |
|---|---:|---:|
| Pinion Teeth | 28 | 28 |
| Gear Teeth | 196 | 196 |
| Gear Ratio | 7.00 | 7.00 |
| Module | 1.50 mm | 1.50 mm |
| Face Width | 12 mm | 12 mm |
| Pinion Pitch Diameter | 42 mm | 42 mm |
| Gear Pitch Diameter | 294 mm | 294 mm |
| Shaft Diameter | 15 mm | 15 mm |
| Center Distance | 168 mm | 169 mm |

The analytical center distance is 168 mm. A 169 mm center distance was used in the CAD assembly as a small packaging and clearance adjustment.

## 5. Engineering Limitations

This project is intended as a preliminary gearbox design and optimization tool rather than a production-certified gearbox design.

The following limitations should be considered:

- Gear bending is estimated using a Lewis-type analytical model.
- Gear tooth geometry in CAD is a manually constructed involute approximation.
- Bearing geometry is simplified for assembly visualization.
- Shaft calculations use analytical stress models rather than detailed finite element analysis.
- The design has not been certified to AGMA or ISO gear-design standards.
- Manufacturing tolerances, lubrication, thermal effects, fatigue details, and dynamic vibration require further analysis before physical manufacture.

## 6. Conclusion

The final GearOpt design achieves the target 7:1 reduction ratio and 500 RPM output speed while satisfying the preliminary gear-strength, shaft-strength, bearing-life, and packaging constraints implemented in the optimizer.

The CAD model was used to translate the analytical design into a three-dimensional gearbox assembly and to verify component arrangement and interference.