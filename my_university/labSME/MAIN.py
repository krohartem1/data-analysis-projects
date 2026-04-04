import matplotlib
matplotlib.use("Agg")
from Func_H import *
from const import *
import matplotlib.pyplot as plt

(bending_moment, sig1_out, sig1_in, sig2_in, sig2_out, eps1_out, eps1_in, eps2_out, eps2_in, eps1_out_max, eps1_in_max, eps_elastic) = loading()
print(f'bending_moment : {bending_moment}')
print(f'sig1_out : {sig1_out}')
print(f'sig1_in : {sig1_in}')
print(f'sig2_in : {sig2_in}')
print(f'sig2_out : {sig2_out}')
print(f'eps1_out : {eps1_out}')
print(f'eps1_in : {eps1_in}')
print(f'eps2_out : {eps2_out}')
print(f'eps2_in : {eps2_in}')
print(f'eps1_out_max : {eps1_out_max}')
print(f'eps1_in_max : {eps1_in_max}')
print(f'eps_elastic : {eps_elastic}')

(
    sig1_out,
    sig1_in,
    sig2_in,
    sig2_out,
    sig1,
    s1,
    sig2,
    s2,
    eps1_out_after_unload,
    eps1_in_after_unload,
    eps2_out_after_unload,
    eps2_in_after_unload,
    M_applied_remaining,
) = unloading(
    bending_moment,
    sig1_out,
    sig1_in,
    sig2_in,
    sig2_out,
    eps1_out,
    eps1_in,
    eps2_out,
    eps2_in,
    stop_mode="sig1_out_zero",
)
print(
    f"После разгрузки: остаток внешнего момента в счётчике M={M_applied_remaining:.6g} N*m/m "
    f"(сверка с моментом по напряжениям на всех волокнах: см. [CHECK] unloading выше)"
)
# Нагрев/охлаждение решаются по σ с фиксированной кривизной: начальные sig1,s1,... уже содержат
# остаточный изгиб после разгрузки. Формула (18) для F — через Δσ к этому состоянию; отдельно
# «прибавлять M_sec» к уравнениям приращений не требуется, пока нет явного 5-го уравнения dM=0.

# Референс σ для силы по (18): холодное состояние после разгрузки (F=0 в начале нагрева)
sig1_ref, s1_ref, sig2_ref, s2_ref = sig1, s1, sig2, s2

# Нагрев: ε0 по отчёту — начальная деформация перед термоциклированием (после разгрузки)
(sig1, s1, sig2, s2, force, eps1_out_strain, eps1_in_strain, eps2_out_strain, eps2_in_strain, list_t, list_sig1, list_sig2, list_force, Fi, list_Fi) = heating_constant_curvature(
    eps1_out_after_unload,
    eps1_in_after_unload,
    eps2_out_after_unload,
    eps2_in_after_unload,
    eps1_out_max,
    eps1_in_max,
    t_start,
    t_finish,
    sig1,
    s1,
    sig2,
    s2,
    d_t=0.05,
)

force_per_width_heat = list_force  # по (18) из отчёта: N/m (≡ mN/mm)

plot_graph(
    force_per_width_heat,
    list_t,
    y_label="Force per width, N/m (≡ mN/mm)",
    x_label="T, K",
    title="Heating",
    show=False,
    save_path="force_per_width_vs_temp_heating.png",
)

plot_graph(
    list_Fi,
    list_t,
    y_label="Fi",
    x_label="t, K",
    title="Heating",
    show=False,
    save_path="Fi_vs_temp_heating.png",
)

# Охлаждение (полный цикл): от t_finish обратно к t_start
(sig1, s1, sig2, s2, force_cool, eps1_out_strain, eps1_in_strain, eps2_out_strain, eps2_in_strain, list_t_c, list_sig1_c, list_sig2_c, list_force_c) = cooling(
    t_finish,
    t_start,
    eps1_out_strain,
    eps1_in_strain,
    eps2_out_strain,
    eps2_in_strain,
    sig1,
    s1,
    sig2,
    s2,
    Fi,
    sig1_ref=sig1_ref,
    s1_ref=s1_ref,
    sig2_ref=sig2_ref,
    s2_ref=s2_ref,
    d_t=0.05,
)

force_per_width_cool = list_force_c  # величина на единицу ширины (N/m)

plot_graph(
    force_per_width_cool,
    list_t_c,
    y_label="Force per width, N/m (≡ mN/mm)",
    x_label="T, K",
    title="Cooling",
    show=False,
    save_path="force_per_width_vs_temp_cooling.png",
)

# Единый график F(T) нагрев + охлаждение (как в статье)
plt.figure()
plt.plot(list_t, force_per_width_heat, label="heating")
plt.plot(list_t_c, force_per_width_cool, label="cooling")
plt.xlabel("T, K")
plt.ylabel("Force per width, N/m (≡ mN/mm)")
plt.title("Force/width vs Temperature (heating + cooling)")
plt.grid(True)
plt.legend()
plt.savefig("force_per_width_vs_temp_cycle.png", dpi=200, bbox_inches="tight")
plt.close()

print("\n[COMPARE] AK1 article gives F/a about 4-14 mN/mm (i.e. 4-14 N/m) for AK1 (range depends on L).")
print(
    f"[COMPARE] model heating max(F/a)={max(force_per_width_heat):.6g} N/m, "
    f"min={min(force_per_width_heat):.6g} N/m"
)
print(
    f"[COMPARE] model cooling  max(F/a)={max(force_per_width_cool):.6g} N/m, "
    f"min={min(force_per_width_cool):.6g} N/m"
)

# Вариант B: разгрузка до прямизны/нулевой кривизны
(
    sig1_out_k0,
    sig1_in_k0,
    sig2_in_k0,
    sig2_out_k0,
    sig1,
    s1,
    sig2,
    s2,
    eps1_out_after_unload_k0,
    eps1_in_after_unload_k0,
    eps2_out_after_unload_k0,
    eps2_in_after_unload_k0,
    M_applied_remaining_k0,
) = unloading(
    bending_moment,
    sig1_out,
    sig1_in,
    sig2_in,
    sig2_out,
    eps1_out,
    eps1_in,
    eps2_out,
    eps2_in,
    stop_mode="curvature_zero",
)
print(
    f"Вариант curvature_zero: M_ост={M_applied_remaining_k0:.6g} Н·м/м (см. [CHECK] unloading выше)"
)

sig1_ref_k0, s1_ref_k0, sig2_ref_k0, s2_ref_k0 = sig1, s1, sig2, s2

(sig1, s1, sig2, s2, force_k0, eps1_out_strain_k0, eps1_in_strain_k0, eps2_out_strain_k0, eps2_in_strain_k0, list_t_k0, list_sig1_k0, list_sig2_k0, list_force_k0, Fi_k0, list_Fi_k0) = heating_constant_curvature(
    eps1_out_after_unload_k0,
    eps1_in_after_unload_k0,
    eps2_out_after_unload_k0,
    eps2_in_after_unload_k0,
    eps1_out_max,
    eps1_in_max,
    t_start,
    t_finish,
    sig1,
    s1,
    sig2,
    s2,
    d_t=0.05,
)

force_per_width_heat_k0 = list_force_k0

(sig1, s1, sig2, s2, force_cool_k0, eps1_out_strain_k0, eps1_in_strain_k0, eps2_out_strain_k0, eps2_in_strain_k0, list_t_c_k0, list_sig1_c_k0, list_sig2_c_k0, list_force_c_k0) = cooling(
    t_finish,
    t_start,
    eps1_out_strain_k0,
    eps1_in_strain_k0,
    eps2_out_strain_k0,
    eps2_in_strain_k0,
    sig1,
    s1,
    sig2,
    s2,
    Fi_k0,
    sig1_ref=sig1_ref_k0,
    s1_ref=s1_ref_k0,
    sig2_ref=sig2_ref_k0,
    s2_ref=s2_ref_k0,
    d_t=0.05,
)

force_per_width_cool_k0 = list_force_c_k0

plt.figure()
plt.plot(list_t_k0, force_per_width_heat_k0, label="heating (unload curvature=0)")
plt.plot(list_t_c_k0, force_per_width_cool_k0, label="cooling (unload curvature=0)")
plt.xlabel("T, K")
plt.ylabel("Force per width, N/m (≡ mN/mm)")
plt.title("Force/width vs Temperature (heating + cooling, unload curvature=0)")
plt.grid(True)
plt.legend()
plt.savefig("force_per_width_vs_temp_cycle_unload_curvature0.png", dpi=200, bbox_inches="tight")
plt.close()

print(
    f"[COMPARE] unload curvature=0: heating max(F/a)={max(force_per_width_heat_k0):.6g} N/m, "
    f"min={min(force_per_width_heat_k0):.6g} N/m"
)
print(
    f"[COMPARE] unload curvature=0: cooling max(F/a)={max(force_per_width_cool_k0):.6g} N/m, "
    f"min={min(force_per_width_cool_k0):.6g} N/m"
)
