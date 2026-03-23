from Func_H import *
from const import *

# Вариант нагрева: True — с явной неизменной кривизной (15) и действием подставки (отчёт)
USE_CONSTANT_CURVATURE_HEATING = True

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

(sig1_out, sig1_in, sig2_in, sig2_out, sig1, s1, sig2, s2, eps1_out_after_unload, eps1_in_after_unload) = unloading(
    bending_moment, sig1_out, sig1_in, sig2_in, sig2_out, eps1_out, eps1_in, eps2_out, eps2_in
)

# Нагрев: ε0 по отчёту — начальная деформация перед термоциклированием (после разгрузки)
if USE_CONSTANT_CURVATURE_HEATING:
    (sig1, s1, sig2, s2, force, eps1_out_strain, eps1_in_strain, list_t, list_sig1, list_sig2, list_force, Fi, list_Fi) = heating_constant_curvature(
        eps1_out_after_unload, eps1_in_after_unload, t_start, t_finish, sig1, s1, sig2, s2
    )
else:
    (sig1, s1, sig2, s2, force, eps1_out_strain, eps1_in_strain, list_t, list_sig1, list_sig2, list_force, Fi, list_Fi) = heating(
        eps1_out_after_unload, eps1_in_after_unload, t_start, t_finish, sig1, s1, sig2, s2
    )

plot_graph(list_force, list_t, y_label="Force, N", x_label="t, K", title="График зависимости")

plot_graph(list_Fi, list_t, y_label="Fi", x_label="t, K", title="График зависимости")
