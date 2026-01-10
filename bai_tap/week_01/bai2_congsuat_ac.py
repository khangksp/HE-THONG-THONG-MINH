t_in = float(input("Nhap nhiet do trong phong: "))
t_out = float(input("Nhap nhiet do ngoai troi: "))
n_people = int(input("Nhap so nguoi: "))

power = 30

if t_out > 35:
    power += 20
if n_people > 30:
    power += 20
if t_in > 28:
    power += 20

if power > 100:
    power = 100

print(f"Nhiet do trong phong: {t_in}, Ngoai troi: {t_out}")
print(f"So nguoi: {n_people}")
print(f"Cong suat de xuat: {power}%")