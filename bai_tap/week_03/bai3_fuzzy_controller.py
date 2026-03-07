import numpy as np

def trimf(x, a, b, c):
    return np.maximum(
        np.minimum((x - a) / (b - a + 1e-6), (c - x) / (c - b + 1e-6)), 0
    )

x_T = np.linspace(20, 35, 300)
x_AC = np.linspace(0, 100, 300)

def fuzzify_T_in(T_in):
    # Dùng lại tham số đã chỉnh ở Bài 1
    mu_cold = trimf(T_in, 20, 21, 24)
    mu_comfort = trimf(T_in, 23, 25, 27)
    mu_hot = trimf(T_in, 26, 29, 35)
    return {
        "cold": float(mu_cold),
        "comfort": float(mu_comfort),
        "hot": float(mu_hot)
    }

def fuzzy_rules(T_in):
    mu = fuzzify_T_in(T_in)
    
    # LUẬT MỜ ĐÃ CHỈNH SỬA
    # IF T_in is LẠNH -> AC Thấp
    # IF T_in is DỄ CHỊU -> AC Thấp (Tiết kiệm hơn theo yêu cầu)
    # IF T_in is NÓNG -> AC Cao
    
    ac_low_strength = max(mu["cold"], mu["comfort"]) # OR logic cho luật gom
    ac_med_strength = 0.0 # Không sử dụng mức Vừa trong luật mới này
    ac_high_strength = mu["hot"]
    
    return {
        "low": ac_low_strength,
        "med": ac_med_strength,
        "high": ac_high_strength
    }

def defuzzify_AC(T_in):
    rules = fuzzy_rules(T_in)
    
    mu_ac_low = trimf(x_AC, 0, 0, 40)
    mu_ac_med = trimf(x_AC, 20, 50, 80)
    mu_ac_high = trimf(x_AC, 60, 100, 100)
    
    aggregated = np.zeros_like(x_AC)
    aggregated = np.maximum(aggregated, np.minimum(rules["low"], mu_ac_low))
    aggregated = np.maximum(aggregated, np.minimum(rules["med"], mu_ac_med))
    aggregated = np.maximum(aggregated, np.minimum(rules["high"], mu_ac_high))
    
    if aggregated.sum() == 0:
        ac_crisp = 0.0
    else:
        ac_crisp = float(np.sum(aggregated * x_AC) / np.sum(aggregated))
    return ac_crisp, aggregated

if __name__ == "__main__":
    test_T = [22, 25, 29, 32]
    for T in test_T:
        ac, _ = defuzzify_AC(T)
        print(f"T_in = {T}°C -> AC fuzzy ~ {ac:.2f} %")