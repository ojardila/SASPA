# Solar Radiation

Part of **SASPA** (*Sistema Agua–Suelo–Planta–Ambiente* / Soil–Water–Plant–Atmosphere System),
a set of teaching tools for agrometeorology.

This module estimates the **solar radiation components** used in evapotranspiration and
crop-water studies, following the **FAO‑56 Penman–Monteith** methodology
(Allen et al., 1998). From sunshine hours and temperature it computes, per month:

| Symbol | Component | Meaning |
|--------|-----------|---------|
| **Ra**  | Extraterrestrial radiation | Radiation at the top of the atmosphere for the site/latitude |
| **Rs**  | Solar / shortwave radiation | Radiation reaching the surface (Ångström–Prescott from sunshine hours) |
| **Rns** | Net shortwave radiation | Rs minus what the surface reflects (albedo) |
| **Rnl** | Net longwave radiation | Net outgoing thermal radiation (Stefan–Boltzmann) |
| **Rn**  | Net radiation | `Rns − Rnl` — the energy available at the surface |

## How it works

For each period the model applies the standard FAO‑56 equations:

- **Solar geometry:** day of year `j`, solar declination `δ`, and sunset hour angle `ωs`
  from the latitude `φ`.
- **Extraterrestrial radiation:**
  `Ra = (24·60/π)·Gsc·[ωs·sin φ·sin δ + cos φ·cos δ·sin ωs]`, with the solar constant
  `Gsc = 0.082 MJ m⁻² min⁻¹`.
- **Solar radiation (Ångström–Prescott):** `Rs = (a_s + b_s·n/N)·Ra`, where
  `n` = actual daily sunshine hours (`BS / days-in-month`), `N` = maximum possible daylight
  hours (`24/π·ωs`), and `a_s = 0.25`, `b_s = 0.50`.
- **Net shortwave radiation:** `Rns = (1 − α)·Rs`, with albedo `α = 0.23`.
- **Net longwave radiation:**
  `Rnl = σ·((Tmax_K⁴ + Tmin_K⁴)/2)·(0.34 − 0.14·√e_a)·(1.35·Rs/Rso − 0.35)`,
  with `σ = 4.903·10⁻⁹ MJ K⁻⁴ m⁻² day⁻¹` and clear‑sky radiation `Rso = (a_s + b_s)·Ra`.
- **Net radiation:** `Rn = Rns − Rnl`.

`solar_radiation_with_bs.py` reports results in **kWh m⁻² day⁻¹** (converting from
MJ m⁻² day⁻¹ with the factor `0.2778`).

## Files

| File | Description |
|------|-------------|
| `solar_radiation_with_bs.py` | Main CLI tool — reads a CSV of monthly data and prints Ra/Rs/Rns/Rnl/Rn per month |
| `main.py` | Minimal standalone example with hard‑coded inputs (single computation, prints MJ m⁻² day⁻¹) |
| `data1.csv` | Sample monthly dataset |
| `requirements.txt` | Python dependencies (`LatLon`, `pyproj`) |

## Input data (CSV)

The CSV passed with `--data` must have a header row with these columns:

| Column | Description | Used for |
|--------|-------------|----------|
| `DATE` | Date of the period (monthly) | Day of year, days in month |
| `BS`   | Monthly bright‑sunshine (insolation) hours | `n = BS / days-in-month` |
| `TV`   | Vapour indicator; actual vapour pressure `e_a = TV / 10` (kPa) | Rnl |
| `TMAX` | Mean monthly maximum air temperature (°C) | Rnl |
| `TMIN` | Mean monthly minimum air temperature (°C) | Rnl |
| `TS`   | Surface/soil temperature (°C) | Present in the sample; not used by the script |

If `TMAX`, `TMIN` or `TV` are missing for a row, `Rnl` is skipped (set to 0) and only the
shortwave components are reported.

## Usage

```bash
pip install -r requirements.txt

python solar_radiation_with_bs.py \
  --hemisphere S \
  --latitude 22.9 \
  --data data1.csv
```

Arguments:

| Flag | Required | Description |
|------|----------|-------------|
| `--hemisphere` | yes | `N` or `S` |
| `--latitude`, `-l` | yes | Latitude magnitude in decimal degrees (positive; hemisphere sets the sign) |
| `--data`, `-d` | yes | Path to the input CSV |

### Output

CSV printed to stdout, one row per month, in **kWh m⁻² day⁻¹**:

```
DATE,BS,RA,RS,RNS,RNL,RN
```

## Notes

- The scripts are written for **Python 2.7** (they use `print` statements and the
  `LatLon 1.0.2` / `pyproj 1.9.5.1` libraries). To run on modern systems, use a Python 2.7
  environment or port the `print` statements and dependencies to Python 3.
- `main.py` hard‑codes its inputs (latitude 22°54′ S, day 135, etc.) as a worked example;
  edit the variables at the top to try other values.
- The inverse Earth–Sun distance `dr` is computed but not applied to `Ra` in the current
  code; results are otherwise consistent with FAO‑56.

## Reference

Allen, R.G., Pereira, L.S., Raes, D., Smith, M. (1998). *Crop evapotranspiration — Guidelines
for computing crop water requirements.* FAO Irrigation and Drainage Paper 56, FAO, Rome.
