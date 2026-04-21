# === ГЕОМЕТРИЯ (оригинал из репозитория, АК1) ===
h1 = 6.86e-06
h2 = 2.407e-05
delta = 0.0003
arc_length = 0.0471
rad = 0.0075
part_len = 0.003

# === ТЕМПЕРАТУРЫ (оригинал) ===
a_start = 311.15
a_finish = 343.15
m_finish = 308.15
m_start = 340.15
t_start = 298.15
t_finish = 373.15

# === КРИСТАЛЛИЧЕСКИЙ СЛОЙ (оригинал, кроме E2/alpha2/E_TP/lam) ===
loading_young_module_1 = 17.5e9
unloading_young_module_1 = 17.5e9
aust_young_module_1 = 29.9e9
strenght_yield_1 = 10000000.0
strenght_yield_1_aust = 600000000.0
strengthening_coefficient_1 = 4000000000.0
strengthening_coefficient_1_aust = 5000000000.0
alpha1_mart = 9.2e-06
alpha1_aust = 1.54e-05

# === АМОРФНЫЙ СЛОЙ (исправлено: TiNiCu, не сталь) ===
young_module_2 = 21.0e9
strenght_yield_2 = 2000000000.0
strengthening_coefficient_2 = 49000000000.0
alpha2 = 10.0e-06

# === ПАРАМЕТРЫ МОДЕЛИ (исправлено по Belyaev 2015) ===
rec_ratio = 0.785
lam = 0.1
young_module_TP = 10000000000.0
