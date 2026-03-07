import matplotlib.pyplot as plt
import numpy as np

def trimf(x, a, b, c):
    return np.maximum(np.minimum((x - a) / (b - a + 1e-6), (c - x) / (c - b + 1e-6)), 0)

x_AC = np.linspace(0, 100, 300)

def fuzzify_T_in(T_in):
    mu_cold = trimf(T_in, 20, 22, 25)
    mu_comfort = trimf(T_in, 24, 26, 28)
    mu_hot = trimf(T_in, 27, 30, 35)
    return {"cold": float(mu_cold), "comfort": float(mu_comfort), "hot": float(mu_hot)}

def fuzzy_rules(T_in):
    mu = fuzzify_T_in(T_in)
    return {"low": mu["cold"], "med": mu["comfort"], "high": mu["hot"]}

def defuzzify_AC(T_in):
    rules = fuzzy_rules(T_in)
    mu_ac_low = trimf(x_AC, 0, 0, 40)
    mu_ac_med = trimf(x_AC, 20, 50, 80)
    mu_ac_high = trimf(x_AC, 60, 100, 100)
    
    aggregated = np.zeros_like(x_AC)
    aggregated = np.maximum(aggregated, np.minimum(rules["low"], mu_ac_low))
    aggregated = np.maximum(aggregated, np.minimum(rules["med"], mu_ac_med))
    aggregated = np.maximum(aggregated, np.minimum(rules["high"], mu_ac_high))
    
    if aggregated.sum() == 0: return 0.0
    return float(np.sum(aggregated * x_AC) / np.sum(aggregated))

T_in = 29.0
T_out = 32.0
occ_level = 2
T_in_list = []
ac_list = []

for step in range(60):
    if step < 20: occ_level = 2
    elif step < 40: occ_level = 1
    else: occ_level = 0
    
    ac_power = defuzzify_AC(T_in)
    dT = 0.0
    
    if ac_power >= 70: dT -= 0.15
    elif ac_power >= 40: dT -= 0.08
    else: dT -= 0.02
    
    if T_out >= 31: dT += 0.10
    
    if occ_level == 2: dT += 0.08
    elif occ_level == 1: dT += 0.04
    
    T_in += dT
    if T_in < 20: T_in = 20
    if T_in > 35: T_in = 35
    
    T_in_list.append(T_in)
    ac_list.append(ac_power)

plt.figure(figsize=(10, 4))
plt.plot(T_in_list, label="T_in (°C)")
plt.xlabel("Step")
plt.ylabel("T_in")
plt.title("Mô phỏng T_in với fuzzy controller")
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 3))
plt.step(range(len(ac_list)), ac_list, where="post")
plt.xlabel("Step")
plt.ylabel("AC power (%)")
plt.title("Công suất AC (fuzzy)")
plt.tight_layout()
plt.show()