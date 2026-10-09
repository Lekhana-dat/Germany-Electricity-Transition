"""Germany's electricity transition, 2000-2025 (vs European peers).
Data: Our World in Data energy dataset (legacy release), built on Ember yearly electricity data. CC BY 4.0.
Run: python analysis.py   (downloads the CSV on first run)
"""
import os, urllib.request
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
RAW = "owid-energy-data.csv"
if not os.path.exists(RAW):
    urllib.request.urlretrieve(URL, RAW)

PEERS = ["Germany", "United Kingdom", "France", "Poland", "Spain", "Italy", "Netherlands", "European Union (27)"]
COLS = ["country", "year", "electricity_generation", "electricity_demand", "carbon_intensity_elec",
        "coal_electricity", "gas_electricity", "oil_electricity", "nuclear_electricity", "wind_electricity",
        "solar_electricity", "hydro_electricity", "biofuel_electricity", "other_renewable_exc_biofuel_electricity",
        "renewables_share_elec", "coal_share_elec", "nuclear_share_elec", "fossil_share_elec"]
df = pd.read_csv(RAW, usecols=COLS)
df = df[df.country.isin(PEERS) & df.year.between(2000, 2025)].copy()
df["other_renewables_electricity"] = df.biofuel_electricity.fillna(0) + df.other_renewable_exc_biofuel_electricity.fillna(0)
df["net_imports_twh"] = df.electricity_demand - df.electricity_generation   # >0 = net importer
df.drop(columns=["biofuel_electricity", "other_renewable_exc_biofuel_electricity"]).to_csv("data/energy_clean.csv", index=False)

de = df[df.country == "Germany"].set_index("year")
C = {"coal": "#3b3b3b", "gas": "#d98c2b", "oil": "#8a6d3b", "nuclear": "#8e5bb5", "wind": "#2a9d8f",
     "solar": "#f2c14e", "hydro": "#3a7ca5", "other_renewables": "#7fb069"}
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})

# 1. Mix over time
src = ["coal", "oil", "gas", "nuclear", "hydro", "other_renewables", "wind", "solar"]
mix = pd.DataFrame({s: de[f"{s}_electricity"] for s in src})
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.stackplot(mix.index, [mix[s] for s in src], labels=[s.replace("_", " ").title() for s in src], colors=[C[s] for s in src])
ax.axvline(2023.3, color="k", ls=":", lw=1); ax.text(2023.1, ax.get_ylim()[1] * 0.97, "Last reactors\nclosed Apr 2023", ha="right", va="top", fontsize=8)
ax.set_title("Germany's electricity generation by source (TWh)", loc="left", fontweight="bold")
ax.legend(loc="upper left", ncol=4, fontsize=8, frameon=False, bbox_to_anchor=(0, -0.08)); ax.set_xlim(2000, 2025)
fig.text(0.01, 0.01, "Source: Our World in Data / Ember. 2025 may be provisional.", fontsize=7, color="gray")
fig.tight_layout(); fig.savefig("charts/1_germany_mix.png"); plt.close(fig)

# 2. Change in generation by source, 2010 -> 2025
d = {s: de.loc[2025, f"{s}_electricity"] - de.loc[2010, f"{s}_electricity"] for s in src}
d = pd.Series(d).sort_values()
fig, ax = plt.subplots(figsize=(8, 4.4))
ax.barh([i.replace("_", " ").title() for i in d.index], d.values, color=[C[i] for i in d.index])
for i, v in enumerate(d.values): ax.text(v + (4 if v >= 0 else -4), i, f"{v:+.0f}", va="center", ha="left" if v >= 0 else "right", fontsize=9)
ax.axvline(0, color="k", lw=.8); ax.set_xlim(d.min() * 1.25, d.max() * 1.18)
ax.set_title("Change in German generation, 2010 to 2025 (TWh)", loc="left", fontweight="bold")
fig.text(0.01, 0.01, "Source: Our World in Data / Ember.", fontsize=7, color="gray")
fig.tight_layout(); fig.savefig("charts/2_change_by_source.png"); plt.close(fig)

# 3. Net imports
ni = de.net_imports_twh.dropna()
fig, ax = plt.subplots(figsize=(9, 4))
ax.bar(ni.index, ni.values, color=["#c1121f" if v > 0 else "#2a9d8f" for v in ni.values])
ax.axhline(0, color="k", lw=.8)
ax.set_title("Germany: net electricity imports (demand minus generation, TWh)", loc="left", fontweight="bold")
ax.text(0.01, 0.04, "Red = net importer, green = net exporter", transform=ax.transAxes, fontsize=8)
fig.text(0.01, 0.01, "Source: Our World in Data / Ember. Net imports approximated as electricity demand minus generation.", fontsize=7, color="gray")
fig.tight_layout(); fig.savefig("charts/3_net_imports.png"); plt.close(fig)

# 4. Carbon intensity vs peers
fig, ax = plt.subplots(figsize=(9, 4.8))
for c in PEERS:
    s = df[df.country == c].set_index("year").carbon_intensity_elec.dropna()
    ax.plot(s.index, s.values, lw=3 if c == "Germany" else 1.3, color="#c1121f" if c == "Germany" else None,
            alpha=1 if c == "Germany" else .8, label=c, zorder=3 if c == "Germany" else 2)
ax.set_title("Carbon intensity of electricity (gCO2e per kWh)", loc="left", fontweight="bold")
ax.legend(fontsize=8, frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.08))
fig.text(0.01, 0.01, "Source: Our World in Data / Ember.", fontsize=7, color="gray")
fig.tight_layout(); fig.savefig("charts/4_carbon_intensity.png"); plt.close(fig)

# 5. Renewables share, trend extrapolation vs 2030 target
r = de.renewables_share_elec.dropna()
fit_years = np.arange(2015, 2026); slope, icpt = np.polyfit(fit_years, r.loc[fit_years].values, 1)
proj_years = np.arange(2025, 2031); proj = slope * proj_years + icpt
fig, ax = plt.subplots(figsize=(9, 4.4))
ax.plot(r.index, r.values, color="#2a9d8f", lw=2.5, label="Renewables share of generation (Ember)")
ax.plot(proj_years, proj, color="#2a9d8f", ls="--", label=f"Straight-line trend from 2015-2025 (+{slope:.1f} pts/year)")
ax.axhline(80, color="#c1121f", ls=":", lw=1.2); ax.text(2000.3, 81, "Official 2030 target: 80% of gross consumption (EEG 2023)", color="#c1121f", fontsize=8)
ax.set_ylim(0, 100); ax.legend(loc="upper left", bbox_to_anchor=(0, 0.8), frameon=False, fontsize=8)
ax.set_title("Renewables share of German electricity: history and simple trend", loc="left", fontweight="bold")
fig.text(0.01, 0.01, "Illustrative extrapolation, not a forecast. The official target uses gross consumption, not generation.", fontsize=7, color="gray")
fig.tight_layout(); fig.savefig("charts/5_renewables_trend.png"); plt.close(fig)

# ---------------- numbers for the README ----------------
print("MIX % (share of generation)"); tot = de.electricity_generation
for y in (2000, 2010, 2020, 2022, 2025):
    print(y, {s: round(100 * de.loc[y, f"{s}_electricity"] / tot[y], 1) for s in src})
print("\nCHANGE 2010->2025 TWh:", d.round(0).to_dict()); print("gen 2010/2025:", round(tot[2010]), round(tot[2025]), " demand:", round(de.electricity_demand[2010]), round(de.electricity_demand[2025]))
print("\nNET IMPORTS TWh:", ni.loc[[2010, 2015, 2019, 2021, 2022, 2023, 2024, 2025]].round(1).to_dict())
print("\nCOAL share:", de.coal_share_elec.loc[[2019, 2020, 2021, 2022, 2023, 2024, 2025]].round(1).to_dict())
print("\nCARBON INTENSITY 2000 / 2010 / 2025 and % change 2010->2025")
for c in PEERS:
    s = df[df.country == c].set_index("year").carbon_intensity_elec
    print(f"{c:22s}", round(s.get(2000, np.nan)), round(s[2010]), round(s[2025]), f"{(s[2025] / s[2010] - 1) * 100:+.0f}%")
# two-factor decomposition of power-sector emissions change 2010->2024 (Mt = TWh * g/kWh / 1000)
g0, g1 = de.electricity_generation[2010], de.electricity_generation[2024]; i0, i1 = de.carbon_intensity_elec[2010], de.carbon_intensity_elec[2024]
e0, e1 = g0 * i0 / 1000, g1 * i1 / 1000
print(f"\nEMISSIONS 2010 {e0:.0f} Mt -> 2024 {e1:.0f} Mt (change {e1 - e0:+.0f}); generation effect {(g1 - g0) * i0 / 1000:+.0f}, intensity effect {g1 * (i1 - i0) / 1000:+.0f}")
print(f"\nTREND: slope {slope:.2f} pts/yr, projected 2030 = {proj[-1]:.1f}% (renewables share of generation); 2025 actual {r[2025]:.1f}")
print("Renewables share:", r.loc[[2000, 2010, 2015, 2020, 2024, 2025]].round(1).to_dict())
