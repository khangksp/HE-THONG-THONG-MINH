count_high = 0
count_off = 0

for step in range(1, 6):
    print(f"\n--- Bước {step} ---")
    t_in = float(input("Nhap T_in: "))
    n_people = int(input("Nhap n_people: "))
    decision = "AC MEDIUM"
    
    if t_in < 24:
        decision = "AC OFF"
        count_off += 1
    elif t_in > 30 or n_people > 20:
        decision = "AC HIGH"
        count_high += 1
        
    print(f"Buoc {step}: T_in={t_in}, n_people={n_people}, Quyet dinh={decision}")

print(f"Số lần AC HIGH: {count_high}")
print(f"Số lần AC OFF: {count_off}")