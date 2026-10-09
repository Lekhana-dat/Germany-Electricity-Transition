# Germany's Electricity Transition, 2000-2025

How has Germany's electricity mix changed, what happened after the 2023 nuclear exit, and how does Germany compare with its European peers?

**Data:** Our World in Data energy dataset (legacy release, CC BY 4.0), built on Ember's yearly electricity data. Peers: UK, France, Poland, Spain, Italy, Netherlands, EU-27.
**Tools:** Python (pandas, matplotlib). `analysis.py` downloads the data and reproduces every chart and number below.

## Key findings

**1. Renewables went from 6% to 59% of generation.** Wind (27%) and solar (18%) now lead; in 2000 coal supplied 52% and nuclear 30%.

![Generation mix](charts/1_germany_mix.png)

**2. Wind and solar covered only part of what coal and nuclear lost.** Between 2010 and 2025, coal fell by 160 TWh and nuclear by 141 TWh (301 TWh combined), while wind (+97 TWh) and solar (+78 TWh) added 175 TWh, about 58% of that. The rest came from lower generation overall (624 to 500 TWh) as demand fell and imports grew. Gas stayed roughly flat (-6 TWh), so it did not fill the gap.

![Change by source](charts/2_change_by_source.png)

**3. Germany switched from net electricity exporter to net importer.** It exported 27 TWh in 2022 and has imported 9 to 26 TWh a year since 2023. This coincides with the last reactors closing in April 2023, but it does not prove the closure caused it: demand fell sharply in 2023, and the 2022 energy crisis, fuel prices and neighbours' cheap supply all play a role. This data cannot separate those effects.

![Net imports](charts/3_net_imports.png)

**4. Coal rose during the 2022 energy crisis, then resumed falling.** Coal's share went 28.4% (2021), 31.7% (2022), 24.6% (2023), 20.6% (2025).

**5. Germany is decarbonising more slowly than most peers.** Between 2010 and 2025 its electricity carbon intensity fell 36%, versus 43% for the EU-27 average, 47% for France, Spain and the Netherlands, and 58% for the UK. At 330 gCO2e/kWh it remains well above the EU average (210), though far below Poland (589).

![Carbon intensity](charts/4_carbon_intensity.png)

**6. Power-sector emissions fell about 156 Mt (322 to 167 Mt, 2010 to 2024).** A two-factor split attributes roughly 57% to a cleaner mix (-89 Mt) and 43% to lower generation (-66 Mt). Part of the lower generation reflects imports replacing domestic output, so some emissions moved abroad rather than disappearing.

**7. A straight-line trend falls short of the 2030 target.** Renewables grew by about 3.2 percentage points a year over 2015-2025. Extending that gives roughly 74% by 2030, below the legal target of 80% of gross electricity consumption (EEG 2023). This is an illustration, not a forecast: it assumes growth continues at the same pace, while the policy plans a big increase in wind and solar build-out.

![Renewables trend](charts/5_renewables_trend.png)

## Limitations
- **Different definitions:** this data measures renewables as a share of generation. Germany's official target and statistics use gross electricity consumption (the Federal Environment Agency reports 55.1% for 2025 versus 59.1% here), so the real gap to 80% may be larger than shown.
- Net imports are approximated as demand minus generation.
- The latest year (2025) may be provisional and revised.
- The source dataset is a legacy release that is no longer updated.
- Findings are descriptive, not causal.

## Files
- `analysis.py` reproduces everything (`pip install -r requirements.txt`, then `python analysis.py`)
- `data/energy_clean.csv`: the cleaned subset used (8 regions, 2000-2025)
- `charts/`: the five charts above

## Credit
Data: Our World in Data (Energy), CC BY 4.0, based on Ember Yearly Electricity Data. https://github.com/owid/energy-data
