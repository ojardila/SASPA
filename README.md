# SASPA — Soil–Water–Plant–Atmosphere System

*Sistema Agua–Suelo–Planta–Ambiente.*

A collection of teaching tools developed for an agrometeorology course, focused on the
water and energy exchanges between the soil, plants and the atmosphere.

## Contents

### ☀️ Radiation — [`radiation/`](./radiation)

Estimates the **solar radiation components** used in evapotranspiration and crop‑water
studies, following the **FAO‑56 Penman–Monteith** methodology. From sunshine hours and
temperature it computes, per month:

- **Ra** — extraterrestrial radiation
- **Rs** — solar / shortwave radiation (Ångström–Prescott)
- **Rns** — net shortwave radiation
- **Rnl** — net longwave radiation
- **Rn** — net radiation (`Rns − Rnl`)

A command‑line script reads a CSV of monthly data (sunshine hours + temperatures) and
prints the radiation components per month. See the module's
[README](./radiation/README.md) for the equations, input format and usage.

## Reference

Allen, R.G., Pereira, L.S., Raes, D., Smith, M. (1998). *Crop evapotranspiration — Guidelines
for computing crop water requirements.* FAO Irrigation and Drainage Paper 56, FAO, Rome.
