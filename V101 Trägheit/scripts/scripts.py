import numpy as np

f = np.array([0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.14, 0.17, 0.18, 0.19])
u_f = 0.01
phi = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
phi_rad = np.deg2rad(phi)

r = 0.2

D = (f * r) / phi_rad

N = len(D)
D_mean = np.mean(D)
s_D = np.std(D, ddof=1)
u_D = (r / phi_rad) * u_f

u_ablese = np.sqrt(np.sum(u_D**2)) / N
u_stat = s_D / np.sqrt(N)
u_ges = np.sqrt(u_stat**2 + u_ablese**2)


print(f"Werte D: {D}")
print(f"D gemittelt = ({D_mean} +- {u_ges})")