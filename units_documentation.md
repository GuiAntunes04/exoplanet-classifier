# 📊 Units Documentation - Exoplanet Classifier

## 🔬 Symbols and Units Used

### Astronomical Units
- **R⊕** = Earth Radius (6,371 km)
- **M⊕** = Earth Mass (5.972 × 10²⁴ kg)
- **R☉** = Solar Radius (696,340 km)
- **M☉** = Solar Mass (1.989 × 10³⁰ kg)
- **S⊕** = Earth Insolation (1,361 W/m²)
- **AU** = Astronomical Unit (149,597,870.7 km)

### Time Units
- **Days** = Earth days (86,400 seconds)
- **Hours** = Earth hours (3,600 seconds)
- **BKJD** = Barycentric Kepler Julian Date (days since January 1, 2000, 12:00 UTC)

### Temperature Units
- **K** = Kelvin (absolute temperature scale)

### Angle Units
- **Degrees** = Sexagesimal degrees (1° = π/180 radians)

### Dimensionless Units
- **Normalized** = Value between 0 and 1
- **Unit (dimensionless)** = Dimensionless ratio
- **Log₁₀ (cgs)** = Base 10 logarithm in cgs units
- **mag** = Magnitude (logarithmic scale)
- **ppm** = Parts per million (10⁻⁶)

### Binary Flags
- **0 or 1** = Binary values (0 = false, 1 = true)

### Text
- **Text** = Character string (e.g., "Kepler", "TOI", "K2")

## 📋 Column Order in Spreadsheet

| # | Technical Name | Concept | Unit | Category |
|---|----------------|---------|------|----------|
| 1 | koi_period | Orbital Period | Days | Transit |
| 2 | koi_time0bk | Time of First Transit | BKJD | Transit |
| 3 | koi_impact | Impact Parameter | Normalized | Transit |
| 4 | koi_duration | Transit Duration | Hours | Transit |
| 5 | koi_depth | Transit Depth | ppm | Transit |
| 6 | koi_prad | Planetary Radius | R⊕ | Planet |
| 7 | koi_teq | Equilibrium Temperature | K | Planet |
| 8 | koi_insol | Insolation | S⊕ | Planet |
| 9 | koi_model_snr | Signal-to-Noise Ratio | Unit (dimensionless) | Quality |
| 10 | koi_steff | Stellar Temperature | K | Star |
| 11 | koi_slogg | Stellar Log g | Log₁₀ (cgs) | Star |
| 12 | koi_srad | Stellar Radius | R☉ | Star |
| 13 | ra | Right Ascension | Degrees | Coordinate |
| 14 | dec | Declination | Degrees | Coordinate |
| 15 | koi_kepmag | Kepler Magnitude | mag | Star |
| 16 | koi_fpflag_nt | Flag: Non-Transit | 0 or 1 | FP Flag |
| 17 | koi_fpflag_ss | Flag: Secondary Eclipse | 0 or 1 | FP Flag |
| 18 | koi_fpflag_co | Flag: Centroid Offset | 0 or 1 | FP Flag |
| 19 | koi_fpflag_ec | Flag: Contamination | 0 or 1 | FP Flag |
| 20 | mission | Mission Context | Text | Mission |
| 21 | pl_orbsmax | Semi-Major Axis | AU | Extra Orbit |
| 22 | pl_bmasse | Planetary Mass | M⊕ | Extra Mass |
| 23 | pl_orbeccen | Orbital Eccentricity | (Value from 0 to 1) | Extra Orbit |
| 24 | st_mass | Stellar Mass | M☉ | Extra Stellar Mass |

## ⚠️ Important Notes

1. **Missing Values**: Leave blank or use NaN for unknown values
2. **FP Flags**: Use only 0 or 1 (do not use values like "True"/"False")
3. **Mission**: Use exactly "Kepler", "TOI", "K2" or leave blank for "NO-MISSION"
4. **Eccentricity**: Must be between 0 and 1 (0 = circular orbit, 1 = parabolic orbit)
5. **Impact Parameter**: Normalized between 0 and 1 (0 = central transit, 1 = tangential transit)

## 📁 Example Spreadsheet

Refer to the `example_exoplanet_spreadsheet.csv` file to see a practical example of the correct format.
