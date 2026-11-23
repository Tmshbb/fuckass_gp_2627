import os
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent.as_posix()
os.environ["TEXINPUTS"] = f"{parent_dir};" + os.environ.get("TEXINPUTS", "")

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

phi = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
F = np.array([0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.14, 0.17, 0.18, 0.19])

r = 0.2
u_F = 0.01 / np.sqrt(3)
phi_rad = np.deg2rad(phi)

def linear(x, m):
    return m * x

popt, pcov = curve_fit(linear, phi_rad, F)
m = popt[0]
u_m = np.sqrt(np.diag(pcov))[0]

D = m * r
u_D = r * u_m

print(f"m  = ({m:.4f} ± {u_m:.4f})")
print(f"D  = ({D:.4f} ± {u_D:.4f})")

fig1, ax1 = plt.subplots(figsize=(7, 4.5))

phi_fit = np.linspace(0, np.max(phi_rad) * 1.05, 200)
ax1.plot(
    phi_fit, linear(phi_fit, m),
    color="tab:blue", linewidth=1.5,
    label=rf"Ausgleichsgerade ($D = ({D:.4f} \pm {u_D:.4f})\,\mathrm{{N\,m\,rad^{{-1}}}}$)"
)

ax1.plot(phi_rad, F, "o", color="black", markersize=5, zorder=3, label="Messwerte",)

ax1.set_xlabel(r"Auslenkung $\varphi\,/\,\mathrm{rad}$")
ax1.set_ylabel(r"Rücktreibende Kraft $F\,/\,\mathrm{N}$")
ax1.set_xlim(left=0)
ax1.set_ylim(bottom=0)
ax1.grid(True, linestyle="--", alpha=0.5)
ax1.legend()

fig1.savefig("build/v101D.pdf")

# 2.
a_cm = np.array([15, 11, 25, 18, 3, 7, 9, 13, 17, 29], dtype=float)
T1 = np.array([4.76, 3.70, 7.54, 5.77, 2.32, 3.33, 3.25, 4.17, 5.35, 8.47])
T2 = np.array([5.24, 4.11, 7.58, 6.11, 2.20, 3.03, 3.46, 4.53, 5.76, 8.56])

mass = 0.2611
a = a_cm / 100.0
T_mean = 0.5 * (T1 + T2)

x = a**2
y = T_mean**2

# Lineare Regression mit Ansatz s * x + t
def linear2(x, s, t):
    return s * x + t

popt, pcov = curve_fit(linear2, x, y)
s, t = popt
u_s, u_t = np.sqrt(np.diag(pcov))

# Trägheitsmoment I_D aus dem Achsenabschnitt t berechnen
I_D = (t * D) / (4 * np.pi**2)
u_ID = np.sqrt((D * u_t)**2 + (t * u_D)**2) / (4 * np.pi**2)

print(f"Steigung s = ({s:.1f} ± {u_s:.1f}) s^2/m^2")
print(f"Offset   t = ({t:.2f} ± {u_t:.2f}) s^2")
print(f"I_D        = ({I_D:.5f} ± {u_ID:.5f}) kg*m^2")

fig2, ax2 = plt.subplots()
ax2.plot(x, y, "o", color="black", markersize=5, zorder=3, label="Messwerte")

x_fit = np.linspace(0, np.max(x) * 1.05, 200)
ax2.plot(
    x_fit,
    s * x_fit + t,
    color="tab:blue",
    linewidth=1.5,
    label=r"Ausgleichsgerade $T^2 = s \cdot a^2 + t$",
)

ax2.set_xlabel(r"Quadrierter Abstand $a^2\,/\,\mathrm{m^2}$")
ax2.set_ylabel(r"Quadrierte Periodendauer $T^2\,/\,\mathrm{s^2}$")
ax2.set_xlim(left=0)
ax2.set_ylim(bottom=0)
ax2.grid(True, linestyle="--", alpha=0.5)
ax2.legend()

fig2.savefig("build/v101steiner.pdf")