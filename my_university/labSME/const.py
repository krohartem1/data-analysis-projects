strenght_yield_1 = 50000000.0
strenght_yield_1_aust = 600000000.0
strenght_yield_2 = 2000000000.0
delta = 0.0003
arc_length = 0.0471
rad = 0.0075
h1 = 6.86e-06
h2 = 2.407e-05
loading_young_module_1 = 17.5e9  # E1M_L
unloading_young_module_1 = 17.5e9  # E1M_U
aust_young_module_1 = 29.9e9  # E1A
young_module_2 = 200.0e9  # Elastic layer (steel, approx. 304 stainless E)
strengthening_coefficient_1 = 4000000000.0
strengthening_coefficient_1_aust = 5000000000.0
strengthening_coefficient_2 = 9000000000.0
# Температурные интервалы фазовых превращений (АК1 из твоего источника):
#   Mf..Af : (35..70) °C
#   гистерезис H : (2..4) °C
# В Кельвинах:
a_start = 311.15   # As (≈38°C, Mf+H_mid)
a_finish = 343.15  # Af (70°C)
m_finish = 308.15  # Mf (≈35°C)
m_start = 340.15   # Ms (≈67°C)

# Границы термоцикла по эксперименту: 25..100°C.
t_start = 298.15   # 25°C
t_finish = 373.15  # 100°C
alpha1_mart = 9.2e-06
alpha1_aust = 1.54e-05
alpha2 = 17.5e-06  # CTE (steel, approx. 304 stainless, ~20..200C)
rec_ratio = 0.785
part_len = 0.003
lam = 0.0  # Ω (phase strain coupling) tuned: remove irreversible strain contribution first
young_module_TP = 30000000000.0  # E_TP (reduced phase strain on cooling)
