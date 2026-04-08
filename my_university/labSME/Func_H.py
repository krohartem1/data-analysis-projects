import numpy
from typing import Optional
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from const import *

podat1_unload = (1 / strengthening_coefficient_1) - (1 / unloading_young_module_1)
podat2 = (1 / strengthening_coefficient_2) - (1 / young_module_2)

PLANE_SECTION_TOL_ABS = 1e-6
PLANE_SECTION_TOL_REL = 1e-3

SIG1_OUT_ZERO_TOL_ABS = 5e3
SIG1_OUT_ZERO_TOL_REL = 1e-5

MOMENT_CHECK_TOL_ABS = 1e-9
MOMENT_CHECK_TOL_REL = 5e-4

STRAIGHT_SCALE_TOL_ABS = 1e-8
STRAIGHT_SCALE_TOL_REL = 1e-3


def bending_moment_per_width_from_mean_half(sig1: float, s1: float, sig2: float, s2: float) -> float:
    return (h1 * h1 * (3.0 * sig1 + s1) - h2 * h2 * (3.0 * sig2 - s2)) / 6.0


def check_plane_sections_hypothesis(
    eps1_out: float,
    eps1_in: float,
    eps2_in: float,
    eps2_out: float,
    *,
    len_o1: float,
    delta: float,
    h1: float,
    h2: float,
    tol_abs: float = PLANE_SECTION_TOL_ABS,
    tol_rel: float = PLANE_SECTION_TOL_REL,
    context: str = "",
    apply_delta_correction: bool = True,
):
    eps1_out_corr = eps1_out - delta / len_o1 if apply_delta_correction else eps1_out
    denom = eps2_in - eps2_out
    num = eps1_out_corr - eps1_in
    near_zero = tol_abs
    if abs(denom) < near_zero:
        if abs(num) < near_zero:
            return h1 / h2
        raise ValueError(
            "Провал проверки гипотезы плоских сечений: (eps2_in - eps2_out) ~ 0, но (eps1_out - eps1_in) != 0. "
            f"context={context}, eps1_out={eps1_out}, eps1_in={eps1_in}, eps2_in={eps2_in}, eps2_out={eps2_out}"
        )

    ratio = num / denom
    target = h1 / h2
    err = ratio - target
    allowed = tol_abs + tol_rel * abs(target)
    if abs(err) > allowed:
        raise ValueError(
            "Провал проверки гипотезы плоских сечений: "
            f"ratio={ratio}, target={target}, err={err}, allowed={allowed}. "
            f"context={context}, eps1_out={eps1_out}, eps1_in={eps1_in}, "
            f"eps2_in={eps2_in}, eps2_out={eps2_out}, len_o1={len_o1}, delta={delta}"
        )
    return ratio


def Hev(x: float) -> int:
    if x <= 0:
        return 0
    else:
        return 1


def force_reaction_per_width(
    sig1: float,
    s1: float,
    sig2: float,
    s2: float,
    sig1_ref: float,
    s1_ref: float,
    sig2_ref: float,
    s2_ref: float,
) -> float:
    delta_M = (h1 * h1 * (3 * (sig1 - sig1_ref) + (s1 - s1_ref))
               - h2 * h2 * (3 * (sig2 - sig2_ref) - (s2 - s2_ref))) / 6.0
    return 1.5 * delta_M / part_len


def plot_graph(
    y_values,
    x_values,
    y_label="Y-Axis",
    x_label="X-Axis",
    title="График зависимости",
    *,
    show: bool = True,
    save_path: Optional[str] = None,
):
    if len(y_values) != len(x_values):
        raise ValueError("Массивы x_values и y_values должны быть одинаковой длины.")

    plt.figure(figsize=(8, 5))
    plt.plot(x_values, y_values, marker=".", linestyle="-")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches="tight")
    if show and plt.get_backend().lower() != "agg":
        plt.show()
    else:
        plt.close()


def loading():
    eps_start = delta / ((arc_length / rad) * (h1 + h2 + rad) - delta)
    sig1 = 0.5 * (Hev(strenght_yield_1 / loading_young_module_1 - eps_start)*(eps_start*loading_young_module_1) + Hev(eps_start - strenght_yield_1 / loading_young_module_1)*(strenght_yield_1 + (eps_start - strenght_yield_1 / loading_young_module_1) * strengthening_coefficient_1))
    s1 = 0.5 * (Hev(strenght_yield_1 / loading_young_module_1 - eps_start)*(eps_start*loading_young_module_1) + Hev(eps_start - strenght_yield_1 / loading_young_module_1)*(strenght_yield_1 + (eps_start - strenght_yield_1 / loading_young_module_1) * strengthening_coefficient_1))
    sig2 = 0
    s2 = 0

    sig1_out = sig1 + s1
    sig1_in = sig1 - s1
    sig2_in = sig2 + s2
    sig2_out = sig2 - s2

    eps1_out = eps_start
    eps1_in = 0
    eps2_out = 0
    eps2_in = 0

    eps1_out_max = eps1_out
    eps1_in_max = eps1_in

    bending_moment = h1 * h1 * ((3 * sig1 + s1) / 6)

    eps_elastic = (eps1_out - eps2_out) / (2 * (1 + eps2_out))

    len_o1 = (arc_length / rad) * (h1 + h2 + rad) - delta
    check_plane_sections_hypothesis(
        eps1_out,
        eps1_in,
        eps2_in,
        eps2_out,
        len_o1=len_o1,
        delta=delta,
        h1=h1,
        h2=h2,
        context="loading",
        apply_delta_correction=True,
    )

    return (
        bending_moment,
        sig1_out,
        sig1_in,
        sig2_in,
        sig2_out,
        eps1_out,
        eps1_in,
        eps2_out,
        eps2_in,
        eps1_out_max,
        eps1_in_max,
        eps_elastic,
    )


def unloading(
    bending_moment,
    sig1_out,
    sig1_in,
    sig2_in,
    sig2_out,
    eps1_out,
    eps1_in,
    eps2_out,
    eps2_in,
    *,
    stop_mode: str = "sig1_out_zero",
    max_unload_steps: int = 500000,
    moment_check_strict: bool = False,
):
    d_M = 1e-6
    M = bending_moment
    sig1_out_zero_tol = SIG1_OUT_ZERO_TOL_ABS + SIG1_OUT_ZERO_TOL_REL * strenght_yield_1

    sig1, s1, sig2, s2 = sig1_out / 2, sig1_out / 2, 0, 0

    list_e1o, list_e2o, list_e1i, list_e2i = [eps1_out], [eps2_out], [eps1_in], [eps2_in]

    len_o1 = (arc_length / rad) * (h1 + h2 + rad) - delta
    len_o2 = (arc_length / rad) * rad
    len_in = (arc_length / rad) * (rad + h1)

    def is_curvature_zero_by_straightness(
        eps1_out_val: float,
        eps1_in_val: float,
        eps2_out_val: float,
        eps2_in_val: float,
    ) -> bool:
        L1_out0 = len_o1 + delta
        L1_out = len_o1 + len_o1 * eps1_out_val
        L1_in0 = len_in
        L1_in = len_in + len_in * eps1_in_val
        L2_out0 = len_o2
        L2_out = len_o2 + len_o2 * eps2_out_val
        L2_in0 = (arc_length / rad) * (rad + h2)
        L2_in = L2_in0 + L2_in0 * eps2_in_val
        scales = [
            L1_out / L1_out0,
            L1_in / L1_in0,
            L2_out / L2_out0,
            L2_in / L2_in0,
        ]
        s_mean = sum(scales) / len(scales)
        allowed = STRAIGHT_SCALE_TOL_ABS + STRAIGHT_SCALE_TOL_REL * abs(s_mean)
        return (max(scales) - min(scales)) <= allowed

    steps = 0
    while M > 0 and steps < max_unload_steps:
        steps += 1
        M -= d_M
        if M < 1e-12:
            break
        #Константы для расчетов
        D1_unload = 1 / unloading_young_module_1
        D2 = 1 / young_module_2

        # Определяем нужные коэффициенты для решения системы по методу Крамера
        A = (D1_unload + podat1_unload * Hev(abs(sig1_in) - strenght_yield_1)) / (D2 + podat2 * Hev(abs(sig2_in) - strenght_yield_2))

        k1 = podat1_unload * (Hev(abs(sig1_out) - strenght_yield_1) - Hev(abs(sig1_in) - strenght_yield_1)) + ((h1 / h2) ** 2) * podat2 * (Hev(abs(sig2_in) - strenght_yield_2) - Hev(abs(sig2_out) - strenght_yield_2)) - (h1 / h2) * (A + h1 / h2) * (2 * D2 + podat2 * (Hev(abs(sig2_in) - strenght_yield_2) + Hev(abs(sig2_out) - strenght_yield_2)))

        k2 = 2 * D1_unload + podat1_unload * (Hev(abs(sig1_out) - strenght_yield_1) + Hev(abs(sig1_in) - strenght_yield_1)) + (h1 / h2) * A * (2 * D2 + podat2 * (Hev(abs(sig2_in) - strenght_yield_2) + Hev(abs(sig2_out) - strenght_yield_2)))

        q1 = 3 * (h1 / h2) ** 2 + 4 * (h1 / h2) + A

        q2 = (h1 / h2) ** 2 - A

        # Находим определители по методу Крамера

        Det_Glav = k1 * q2 - k2 * q1
        Det_sig1 = -(6 * (-1)*d_M / h2**2) * k2
        Det_s1 = (6 * (-1)*d_M / h2**2) * k1

        # Определяем d_sig1, d_s1, d_sig2, d_s2
        d_sig1 = Det_sig1 / Det_Glav
        d_s1 = Det_s1 / Det_Glav

        d_sig2 = -(h1 / h2) * d_sig1
        d_s2 = (A + (h1 / h2)) * d_sig1 - A * d_s1
        #Проверка на H(d|sig|)
        sig1_out_test = sig1 + s1
        sig1_in_test = sig1 - s1
        sig2_in_test = sig2 + s2
        sig2_out_test = sig2 - s2

        sig1_out_new = sig1 + d_sig1 + s1 + d_s1
        sig1_in_new = sig1 + d_sig1 - s1 - d_s1
        sig2_in_new = sig2 + d_sig2 + s2 + d_s2
        sig2_out_new = sig2 + d_sig2 - s2 - d_s2
        while(sig1_out_new != sig1_out_test or sig1_in_new != sig1_in_test or sig2_in_new != sig2_in_test or sig2_out_new != sig2_out_test):
            # Снова определяем нужные коэффициенты для решения системы по методу Крамера и дописываем Хевисайды
            A = (D1_unload + podat1_unload * Hev(abs(sig1_in_new) - strenght_yield_1) * Hev(abs(sig1_in_new) - abs(sig1_in))) / (D2 + podat2 * Hev(abs(sig2_in_new) - strenght_yield_2) * Hev(abs(sig2_in_new) - abs(sig2_in)))

            k1 = podat1_unload * (Hev(abs(sig1_out_new) - strenght_yield_1) * Hev(abs(sig1_out_new) - abs(sig1_out)) - Hev(abs(sig1_in_new) - strenght_yield_1) * Hev(abs(sig1_in_new) - abs(sig1_in))) + ((h1 / h2) ** 2) * podat2 * (Hev(abs(sig2_in_new) - strenght_yield_2) * Hev(abs(sig2_in_new) - abs(sig2_in)) - Hev(abs(sig2_out_new) - strenght_yield_2) * Hev(abs(sig2_out_new) - abs(sig2_out))) - (h1 / h2) * (A + h1 / h2) * (2 * D2 + podat2 * (Hev(abs(sig2_in_new) - strenght_yield_2) * Hev(abs(sig2_in_new) - abs(sig2_in)) + Hev(abs(sig2_out_new) - strenght_yield_2) * Hev(abs(sig2_out_new) - abs(sig2_out))))

            k2 = 2 * D1_unload + podat1_unload * (Hev(abs(sig1_out_new) - strenght_yield_1) * Hev(abs(sig1_out_new) - abs(sig1_out)) + Hev(abs(sig1_in_new) - strenght_yield_1) * Hev(abs(sig1_in_new) - abs(sig1_in))) + (h1 / h2) * A * (2 * D2 + podat2 * (Hev(abs(sig2_in_new) - strenght_yield_2) * Hev(abs(sig2_in_new) - abs(sig2_in)) + Hev(abs(sig2_out_new) - strenght_yield_2) * Hev(abs(sig2_out_new) - abs(sig2_out))))

            q1 = 3 * (h1 / h2) ** 2 + 4 * (h1 / h2) + A

            q2 = (h1 / h2) ** 2 - A

            # Находим определители по методу Крамера

            Det_Glav = k1 * q2 - k2 * q1
            Det_sig1 = -(6 * (-1)*d_M / h2**2) * k2
            Det_s1 = (6 * (-1)*d_M / h2**2) * k1

            # Определяем d_sig1, d_s1, d_sig2, d_s2
            d_sig1 = Det_sig1 / Det_Glav
            d_s1 = Det_s1 / Det_Glav

            d_sig2 = -(h1 / h2) * d_sig1
            d_s2 = (A + (h1 / h2)) * d_sig1 - A * d_s1

            sig1_out_test = sig1_out_new
            sig1_in_test = sig1_in_new
            sig2_in_test = sig2_in_new
            sig2_out_test = sig2_out_new

            sig1_out_new = sig1 + d_sig1 + s1 + d_s1
            sig1_in_new = sig1 + d_sig1 - s1 - d_s1
            sig2_in_new = sig2 + d_sig2 + s2 + d_s2
            sig2_out_new = sig2 + d_sig2 - s2 - d_s2


        #-----------------------------------------------------------

        sig1_out_old = sig1_out
        sig1_in_old = sig1_in
        sig2_in_old = sig2_in
        sig2_out_old = sig2_out

        sig1 += d_sig1
        s1 += d_s1
        sig2 += d_sig2
        s2 += d_s2

        sig1_out = sig1 + s1
        sig1_in = sig1 - s1
        sig2_in = sig2 + s2
        sig2_out = sig2 - s2

        # Вычисляем новые напряжения и деформации в каждом из слоев
        eps1_out += (d_sig1 + d_s1) / unloading_young_module_1 + podat1_unload * (d_sig1 + d_s1) * Hev(abs(sig1_out) - strenght_yield_1)*Hev(abs(sig1_out) - abs(sig1_out_old))
        eps1_in += (d_sig1 - d_s1) / unloading_young_module_1 + podat1_unload * (d_sig1 - d_s1) * Hev(abs(sig1_in) - strenght_yield_1)*Hev(abs(sig1_in) - abs(sig1_in_old))
        eps2_in += (d_sig2 + d_s2) / young_module_2 + podat2 * (d_sig2 + d_s2) * Hev(abs(sig2_in) - strenght_yield_2)*Hev(abs(sig2_in) - abs(sig2_in_old))
        eps2_out += (d_sig2 - d_s2) / young_module_2 + podat2 * (d_sig2 - d_s2) * Hev(abs(sig2_out) - strenght_yield_2)*Hev(abs(sig2_out) - abs(sig2_out_old))

        # Промежуточная проверка гипотезы плоских сечений на каждой итерации
        check_plane_sections_hypothesis(
            eps1_out,
            eps1_in,
            eps2_in,
            eps2_out,
            len_o1=len_o1,
            delta=delta,
            h1=h1,
            h2=h2,
            context=f"unloading step, M={M}",
            apply_delta_correction=True,
        )

        list_e1o.append(eps1_out)
        list_e2o.append(eps2_out)
        list_e1i.append(eps1_in)
        list_e2i.append(eps2_in)

        if stop_mode == "sig1_out_zero":
            if sig1_out_old > 0.0 and sig1_out <= 0.0:
                break
            if abs(sig1_out) <= sig1_out_zero_tol:
                break

        if stop_mode == "curvature_zero":
            if is_curvature_zero_by_straightness(eps1_out, eps1_in, eps2_out, eps2_in):
                break

    M_from_sigma = bending_moment_per_width_from_mean_half(sig1, s1, sig2, s2)
    mom_tol = MOMENT_CHECK_TOL_ABS + MOMENT_CHECK_TOL_REL * max(
        abs(M), abs(M_from_sigma), 1.0
    )
    if moment_check_strict and abs(M_from_sigma - M) > mom_tol:
        raise ValueError(
            f"unloading moment check: M_counter={M} M_sigma={M_from_sigma} tol={mom_tol}"
        )

    # Деформации после разгрузки — для этапа нагрева (ε0 в отчёте: «начальная деформация» перед термоциклированием)
    eps1_out_after_unload = list_e1o[-1]
    eps1_in_after_unload = list_e1i[-1]
    eps2_out_after_unload = list_e2o[-1]
    eps2_in_after_unload = list_e2i[-1]
    return (
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
        M,
    )


def heating_constant_curvature(
    eps1_out_0,
    eps1_in_0,
    eps2_out_0,
    eps2_in_0,
    eps1_out_max_0,
    eps1_in_max_0,
    t_start,
    t_finish,
    sig1,
    s1,
    sig2,
    s2,
    *,
    d_t: float = 0.5,
):
    def compute_dPhi(Fi_old_local: float, t_local: float, dT_local: float) -> float:
        # Косинусная аппроксимация Φ(T) — гладкая S-кривая.
        # Нагрев: Φ = 0.5*(1+cos(π*(T-As)/(Af-As))) на (As,Af), иначе 1 или 0
        # Охлаждение: Φ = 0.5*(1-cos(π*(Ms-T)/(Ms-Mf))) на (Mf,Ms), иначе 0 или 1
        import math
        T_new = t_local + dT_local
        if dT_local > 0:  # heating
            if T_new <= a_start:
                Phi_new = 1.0
            elif T_new >= a_finish:
                Phi_new = 0.0
            else:
                Phi_new = 0.5 * (1 + math.cos(math.pi * (T_new - a_start) / (a_finish - a_start)))
        else:  # cooling
            if T_new >= m_start:
                Phi_new = 0.0
            elif T_new <= m_finish:
                Phi_new = 1.0
            else:
                Phi_new = 0.5 * (1 - math.cos(math.pi * (m_start - T_new) / (m_start - m_finish)))
        return Phi_new - Fi_old_local

    def effective_compliance_formula_9(
        sig_curr_fiber: float,
        sig_trial_fiber: float,
        D: float,
        yield_strength: float,
        strengthening_coefficient: float,
        alpha_dummy: float = 0.0,
    ) -> float:
        # Формула (9) в виде коэффициента при dσ:
        # dε = D*dσ + (1/H - D) * H(|σ*|-σT) * H(d|σ*|) * dσ
        base_yield = Hev(abs(sig_trial_fiber) - yield_strength)
        H_d_abs = Hev(abs(sig_trial_fiber) - abs(sig_curr_fiber))
        podat_local = (1 / strengthening_coefficient) - D
        return D + podat_local * base_yield * H_d_abs

    dT = float(d_t)

    len_o1 = (arc_length / rad) * (h1 + h2 + rad) - delta

    # Референс напряжений: состояние перед нагревом (после разгрузки). F по (18) — отклонение от него.
    sig1_ref, s1_ref, sig2_ref, s2_ref = sig1, s1, sig2, s2

    # Состояния напряжений (используем сиг/и как в текущем коде)
    t = t_start
    Fi = 1.0
    Fi_old = Fi

    list_force = [0.0]
    list_t = [t_start]
    list_sig1 = [sig1]
    list_sig2 = [sig2]
    list_s1 = [s1]
    list_s2 = [s2]
    list_Fi = [Fi]

    eps1_out_strain = eps1_out_0
    eps1_in_strain = eps1_in_0
    eps2_out_strain = eps2_out_0
    eps2_in_strain = eps2_in_0

    # Для постобработки: разделяем полную деформацию на мех/фаз/темп составляющие.
    # Здесь накапливаем только "свободные" (не-механические) части: фазовую и температурную.
    eps1_out_phase = 0.0
    eps1_in_phase = 0.0
    eps1_out_therm = 0.0
    eps1_in_therm = 0.0
    eps2_out_phase = 0.0
    eps2_in_phase = 0.0
    eps2_out_therm = 0.0
    eps2_in_therm = 0.0

    # Списки "механического напряжения" по волокнам (σ_mech = E(T) * ε_mech).
    # ε_mech = ε_total - ε_phase - ε_therm.
    E1_init_for_plot = aust_young_module_1 * (1 - Fi_old) + loading_young_module_1 * Fi_old
    sig1_out_init = sig1 + s1
    sig1_in_init = sig1 - s1
    sig2_out_init = sig2 - s2
    sig2_in_init = sig2 + s2
    list_sig1_out_mech = [E1_init_for_plot * eps1_out_strain]
    list_sig1_in_mech = [E1_init_for_plot * eps1_in_strain]
    list_sig2_out_mech = [young_module_2 * eps2_out_strain]
    list_sig2_in_mech = [young_module_2 * eps2_in_strain]

    eps0_uniform = rec_ratio * (delta / ((arc_length / rad) * (h1 + h2 + rad) - delta))
    eps0_heat_out = eps0_uniform
    eps0_heat_in = eps0_uniform

    alpha1_old = alpha1_aust * (1 - Fi_old) + alpha1_mart * Fi_old
    E1_init = aust_young_module_1 * (1 - Fi_old) + loading_young_module_1 * Fi_old
    D1_old = 1.0 / E1_init

    max_iter = 200
    MIN_IT_FOR_HEV_STABILITY = 5
    prev_hev_state_local = None
    prev_x_vec_local = None

    while t <= t_finish:
        dPhi = compute_dPhi(Fi_old, t, dT)
        Fi = Fi_old + dPhi
        # Численная защита: Φ должна оставаться в [0, 1]
        if Fi < 0.0:
            Fi = 0.0
        elif Fi > 1.0:
            Fi = 1.0

        alpha1 = alpha1_aust * (1 - Fi) + alpha1_mart * Fi

        yield_mix = strenght_yield_1_aust * (1 - Fi) + strenght_yield_1 * Fi
        H1_mix = strengthening_coefficient_1_aust * (1 - Fi) + strengthening_coefficient_1 * Fi

        # (13) E1 = EA(1-Φ) + EMΦ -> D1 = 1/E1
        E1 = aust_young_module_1 * (1 - Fi) + loading_young_module_1 * Fi
        D1 = 1.0 / E1
        D2 = 1.0 / young_module_2

        # Фазовый вклад на нагреве: ε⁰·dΦ + σ*·d(1/E₁) [формула (7) Кусакиной]
        # σ*·d(1/E₁) — деформация из-за смены модуля при фазовом превращении
        d_D1 = D1 - D1_old
        sig1_out_curr_pre = sig1 + s1
        sig1_in_curr_pre = sig1 - s1
        modulus_change_out = sig1_out_curr_pre * d_D1
        modulus_change_in = sig1_in_curr_pre * d_D1
        phase_out = eps0_heat_out * dPhi + modulus_change_out
        phase_in = eps0_heat_in * dPhi + modulus_change_in

        # Тепловой вклад: d(α1 dT) = α1 dT + T dα1
        thermal1_term = alpha1 * dT
        thermal2_term = alpha2 * dT

        sig1_out_curr = sig1 + s1
        sig1_in_curr = sig1 - s1
        sig2_out_curr = sig2 - s2
        sig2_in_curr = sig2 + s2

        # Решатель фиксированной кривизны:
        # 3 кинематических равенства приращений деформаций:
        #   dε1_out = dε1_in
        #   dε1_in  = dε2_in
        #   dε1_out = dε2_out
        # + равновесие по продольной силе:
        #   h1*(x1+x2) + h2*(x3+x4) = 0
        # неизвестные на шаге: x1..x4 = dσ (out/in) для слоёв 1 и 2.
        x1 = x2 = x3 = x4 = 0.0
        tol_res = 1e-9
        converged = False
        for it in range(max_iter):
            # trial-напряжения на волокнах
            sig1_out_trial_g = sig1_out_curr + x1
            sig1_in_trial_g = sig1_in_curr + x2
            sig2_out_trial_g = sig2_out_curr + x3
            sig2_in_trial_g = sig2_in_curr + x4

            # (9) эффективные податливости (коэффициенты при dσ) по trial-напряжениям
            C1_out_g = effective_compliance_formula_9(
                sig1_out_curr, sig1_out_trial_g, D1, yield_mix, H1_mix
            )
            C1_in_g = effective_compliance_formula_9(
                sig1_in_curr, sig1_in_trial_g, D1, yield_mix, H1_mix
            )
            C2_out_g = effective_compliance_formula_9(
                sig2_out_curr,
                sig2_out_trial_g,
                D2,
                strenght_yield_2,
                strengthening_coefficient_2,
            )
            C2_in_g = effective_compliance_formula_9(
                sig2_in_curr,
                sig2_in_trial_g,
                D2,
                strenght_yield_2,
                strengthening_coefficient_2,
            )

            # Строим A*x = b из 4 уравнений:
            #   (1) dε1_out = dε1_in  -> C1_out*x1 - C1_in*x2 = phase_in - phase_out
            #   (2) dε1_in  = dε2_in -> C1_in*x2  - C2_in*x4  = thermal2 - phase_in - thermal1
            #   (3) dε1_out = dε2_out-> C1_out*x1 - C2_out*x3 = thermal2 - phase_out - thermal1
            #   (4) N=0 (приращения): h1*(x1+x2) + h2*(x3+x4)=0
            A = numpy.array(
                [
                    [C1_out_g, -C1_in_g, 0.0, 0.0],
                    [0.0, C1_in_g, 0.0, -C2_in_g],
                    [C1_out_g, 0.0, -C2_out_g, 0.0],
                    [h1, h1, h2, h2],
                ],
                dtype=float,
            )
            b = numpy.array(
                [
                    # (1) dε1_out = dε1_in:
                    # dε1_out = C1_out*x1 + phase_out + thermal1_term
                    # dε1_in  = C1_in*x2  + phase_in  + thermal1_term
                    # thermal1_term одинаков для out/in, поэтому сокращается:
                    # RHS = (phase_in + thermal1_term) - (phase_out + thermal1_term) = phase_in - phase_out
                    (phase_in + thermal1_term) - (phase_out + thermal1_term),
                    thermal2_term - phase_in - thermal1_term,
                    thermal2_term - phase_out - thermal1_term,
                    0.0,
                ],
                dtype=float,
            )

            try:
                x_new = numpy.linalg.solve(A, b)
            except numpy.linalg.LinAlgError as e:
                raise ValueError(
                    f"Singular system in heating fixed-curvature: it={it}, t={t}, Fi={Fi}, A={A}, b={b}"
                ) from e

            x1_new, x2_new, x3_new, x4_new = map(float, x_new)

            # Проверяем согласованность системы на итоговых коэффициентах (9)
            sig1_out_trial_s = sig1_out_curr + x1_new
            sig1_in_trial_s = sig1_in_curr + x2_new
            sig2_out_trial_s = sig2_out_curr + x3_new
            sig2_in_trial_s = sig2_in_curr + x4_new

            C1_out_s = effective_compliance_formula_9(
                sig1_out_curr, sig1_out_trial_s, D1, yield_mix, H1_mix
            )
            C1_in_s = effective_compliance_formula_9(
                sig1_in_curr, sig1_in_trial_s, D1, yield_mix, H1_mix
            )
            C2_out_s = effective_compliance_formula_9(
                sig2_out_curr,
                sig2_out_trial_s,
                D2,
                strenght_yield_2,
                strengthening_coefficient_2,
            )
            C2_in_s = effective_compliance_formula_9(
                sig2_in_curr,
                sig2_in_trial_s,
                D2,
                strenght_yield_2,
                strengthening_coefficient_2,
            )

            A_check = numpy.array(
                [
                    [C1_out_s, -C1_in_s, 0.0, 0.0],
                    [0.0, C1_in_s, 0.0, -C2_in_s],
                    [C1_out_s, 0.0, -C2_out_s, 0.0],
                    [h1, h1, h2, h2],
                ],
                dtype=float,
            )
            x_vec = numpy.array([x1_new, x2_new, x3_new, x4_new], dtype=float)
            res_vec = A_check @ x_vec - b
            res_vec_max = float(numpy.max(numpy.abs(res_vec)))
            if res_vec_max < tol_res:
                x1, x2, x3, x4 = x1_new, x2_new, x3_new, x4_new
                C1_out, C1_in, C2_out, C2_in = C1_out_s, C1_in_s, C2_out_s, C2_in_s
                sig1_out_trial, sig1_in_trial = sig1_out_trial_s, sig1_in_trial_s
                sig2_out_trial, sig2_in_trial = sig2_out_trial_s, sig2_in_trial_s
                converged = True
                break

            # Если Hev-дискретизация и сами dσ стабилизировались,
            # то дальнейшие итерации не дадут нового решения.
            # Это предотвращает выход "тупо по max_iter" в сложных переходах.
            hev_state_iter_local = (
                Hev(abs(sig1_out_trial_s) - yield_mix),
                Hev(abs(sig1_in_trial_s) - yield_mix),
                Hev(abs(sig2_out_trial_s) - strenght_yield_2),
                Hev(abs(sig2_in_trial_s) - strenght_yield_2),
            )
            x_vec_new = numpy.array([x1_new, x2_new, x3_new, x4_new], dtype=float)
            stable_x = (
                prev_x_vec_local is not None
                and float(numpy.max(numpy.abs(x_vec_new - prev_x_vec_local))) < 1e-15
            )
            stable_hev = prev_hev_state_local == hev_state_iter_local
            if it >= MIN_IT_FOR_HEV_STABILITY and stable_x and stable_hev:
                # Выходим без установки converged=True.
                # После цикла сработает "fallback/последний guess" как страховка,
                # но мы не будем тратить лишние итерации.
                break

            prev_hev_state_local = hev_state_iter_local
            prev_x_vec_local = x_vec_new

            # иначе продолжаем итерацию
            x1, x2, x3, x4 = x1_new, x2_new, x3_new, x4_new

        # Если не сошлось — всё равно пересчитаем параметры на последнем guess
        if not converged:
            sig1_out_trial = sig1_out_curr + x1
            sig1_in_trial = sig1_in_curr + x2
            sig2_out_trial = sig2_out_curr + x3
            sig2_in_trial = sig2_in_curr + x4
            C1_out = effective_compliance_formula_9(
                sig1_out_curr, sig1_out_trial, D1, yield_mix, H1_mix
            )
            C1_in = effective_compliance_formula_9(
                sig1_in_curr, sig1_in_trial, D1, yield_mix, H1_mix
            )
            C2_out = effective_compliance_formula_9(
                sig2_out_curr,
                sig2_out_trial,
                D2,
                strenght_yield_2,
                strengthening_coefficient_2,
            )
            C2_in = effective_compliance_formula_9(
                sig2_in_curr,
                sig2_in_trial,
                D2,
                strenght_yield_2,
                strengthening_coefficient_2,
            )

        d_sig1 = 0.5 * (x1 + x2)
        d_s1 = 0.5 * (x1 - x2)
        d_sig2 = 0.5 * (x3 + x4)
        d_s2 = 0.5 * (x4 - x3)

        sig1 += d_sig1
        s1 += d_s1
        sig2 += d_sig2
        s2 += d_s2

        force = force_reaction_per_width(sig1, s1, sig2, s2, sig1_ref, s1_ref, sig2_ref, s2_ref)
        list_force.append(force)

        list_sig1.append(sig1)
        list_sig2.append(sig2)
        list_s1.append(s1)
        list_s2.append(s2)

        # Обновляем t/Fi/alpha/D1_old
        t += dT
        list_t.append(t)
        Fi_old = Fi
        list_Fi.append(Fi)
        alpha1_old = alpha1
        D1_old = D1

        d_eps_out1 = C1_out * x1 + phase_out + thermal1_term
        d_eps_in1 = C1_in * x2 + phase_in + thermal1_term
        d_eps_out2 = C2_out * x3 + thermal2_term
        d_eps_in2 = C2_in * x4 + thermal2_term

        eps1_out_strain += d_eps_out1
        eps1_in_strain += d_eps_in1
        eps2_out_strain += d_eps_out2
        eps2_in_strain += d_eps_in2

        # Накопление "свободных" деформаций
        eps1_out_phase += phase_out
        eps1_in_phase += phase_in
        eps1_out_therm += thermal1_term
        eps1_in_therm += thermal1_term
        # В слое 2 фазовой составляющей нет в используемой модели (только тепловая)
        eps2_out_phase += 0.0
        eps2_in_phase += 0.0
        eps2_out_therm += thermal2_term
        eps2_in_therm += thermal2_term

        # "Механические" напряжения как E(T)*ε_mech
        eps1_out_mech = eps1_out_strain - eps1_out_phase - eps1_out_therm
        eps1_in_mech = eps1_in_strain - eps1_in_phase - eps1_in_therm
        eps2_out_mech = eps2_out_strain - eps2_out_phase - eps2_out_therm
        eps2_in_mech = eps2_in_strain - eps2_in_phase - eps2_in_therm
        list_sig1_out_mech.append(E1 * eps1_out_mech)
        list_sig1_in_mech.append(E1 * eps1_in_mech)
        list_sig2_out_mech.append(young_module_2 * eps2_out_mech)
        list_sig2_in_mech.append(young_module_2 * eps2_in_mech)

        try:
            check_plane_sections_hypothesis(
                eps1_out_strain,
                eps1_in_strain,
                eps2_in_strain,
                eps2_out_strain,
                len_o1=len_o1,
                delta=delta,
                h1=h1,
                h2=h2,
                context="heating",
                apply_delta_correction=True,
            )
        except ValueError:
            pass

    return (
        sig1,
        s1,
        sig2,
        s2,
        list_force[-1],
        eps1_out_strain,
        eps1_in_strain,
        eps2_out_strain,
        eps2_in_strain,
        list_t,
        list_sig1,
        list_sig2,
        list_s1,
        list_s2,
        list_force,
        Fi,
        list_Fi,
        list_sig1_out_mech,
        list_sig1_in_mech,
        list_sig2_out_mech,
        list_sig2_in_mech,
    )


# Охлаждение и рассчет силы
def cooling(
    t_start,
    t_finish,
    eps1_out_strain,
    eps1_in_strain,
    eps2_out_strain,
    eps2_in_strain,
    sig1,
    s1,
    sig2,
    s2,
    Fi,
    *,
    sig1_ref: float,
    s1_ref: float,
    sig2_ref: float,
    s2_ref: float,
    d_t: float = 0.5,
):
    def compute_dPhi(Fi_old_local: float, t_local: float, dT_local: float) -> float:
        # Косинусная аппроксимация Φ(T) для охлаждения
        import math
        T_new = t_local + dT_local
        if dT_local < 0:  # cooling
            if T_new >= m_start:
                Phi_new = 0.0
            elif T_new <= m_finish:
                Phi_new = 1.0
            else:
                Phi_new = 0.5 * (1 - math.cos(math.pi * (m_start - T_new) / (m_start - m_finish)))
        else:  # heating (если вызвали cooling с dT>0)
            if T_new <= a_start:
                Phi_new = 1.0
            elif T_new >= a_finish:
                Phi_new = 0.0
            else:
                Phi_new = 0.5 * (1 + math.cos(math.pi * (T_new - a_start) / (a_finish - a_start)))
        return Phi_new - Fi_old_local

    def effective_compliance_formula_9(
        sig_curr_fiber: float,
        sig_trial_fiber: float,
        D: float,
        yield_strength: float,
        strengthening_coefficient: float,
    ) -> float:
        # Формула (9) как коэффициент при dσ:
        # dε = D*dσ + (1/H - D)*H(|σ*|-σT)*H(d|σ*|)*dσ
        base_yield = Hev(abs(sig_trial_fiber) - yield_strength)
        H_d_abs = Hev(abs(sig_trial_fiber) - abs(sig_curr_fiber))
        podat_local = (1 / strengthening_coefficient) - D
        return D + podat_local * base_yield * H_d_abs

    dT = -float(d_t)

    len_o1 = (arc_length / rad) * (h1 + h2 + rad) - delta

    t = t_start
    # Та же F(σ−σ_ref), что и на нагреве: конец нагрева даёт тот же F, что и ∫dF раньше, без «наследования» лишнего смещения
    force = force_reaction_per_width(sig1, s1, sig2, s2, sig1_ref, s1_ref, sig2_ref, s2_ref)
    list_force = [force]
    list_t = [t_start]
    list_sig1 = [sig1]
    list_sig2 = [sig2]
    list_s1 = [s1]
    list_s2 = [s2]

    Fi_old = Fi
    alpha1_old = alpha1_aust * (1 - Fi_old) + alpha1_mart * Fi_old
    list_Fi = [Fi]

    # Накопление "свободных" деформаций (фаза/температура) для выделения мех. части.
    eps1_out_phase = 0.0
    eps1_in_phase = 0.0
    eps1_out_therm = 0.0
    eps1_in_therm = 0.0
    eps2_out_phase = 0.0
    eps2_in_phase = 0.0
    eps2_out_therm = 0.0
    eps2_in_therm = 0.0

    # Списки "механического напряжения" по волокнам: σ_mech = E(T) * ε_mech.
    E1_init_for_plot = aust_young_module_1 * (1 - Fi_old) + loading_young_module_1 * Fi_old
    list_sig1_out_mech = [E1_init_for_plot * eps1_out_strain]
    list_sig1_in_mech = [E1_init_for_plot * eps1_in_strain]
    list_sig2_out_mech = [young_module_2 * eps2_out_strain]
    list_sig2_in_mech = [young_module_2 * eps2_in_strain]

    # Фазовая деформация на охлаждении.
    # В Belyaev et al. (2015): dε_ph = (σ*/E_TP + Ω * ε*) dΦ,
    # где ε* — необратимая деформация после нагрева (константа на протяжении охлаждения),
    # σ* — текущие напряжения. Поэтому:
    eps_star_out = float(eps1_out_strain)
    eps_star_in = float(eps1_in_strain)

    E1_init_cool = aust_young_module_1 * (1 - Fi_old) + loading_young_module_1 * Fi_old
    D1_old_cool = 1.0 / E1_init_cool

    max_iter = 200

    while t >= t_finish:
        dPhi = compute_dPhi(Fi_old, t, dT)
        Fi = Fi_old + dPhi
        # Численная защита: Φ должна оставаться в [0, 1]
        if Fi < 0.0:
            Fi = 0.0
        elif Fi > 1.0:
            Fi = 1.0

        alpha1 = alpha1_aust * (1 - Fi) + alpha1_mart * Fi

        E1 = aust_young_module_1 * (1 - Fi) + loading_young_module_1 * Fi
        D1 = 1.0 / E1
        D2 = 1.0 / young_module_2

        yield_mix = strenght_yield_1_aust * (1 - Fi) + strenght_yield_1 * Fi
        H1_mix = strengthening_coefficient_1_aust * (1 - Fi) + strengthening_coefficient_1 * Fi

        # Текущие напряжения на волокнах
        sig1_out_curr = sig1 + s1
        sig1_in_curr = sig1 - s1
        sig2_out_curr = sig2 - s2
        sig2_in_curr = sig2 + s2

        # (6) Belyaev: фазовый вклад на охлаждении + σ*·d(1/E₁) [формула (7)]
        eps0_cool_out = (sig1_out_curr) / young_module_TP + lam * eps_star_out
        eps0_cool_in = (sig1_in_curr) / young_module_TP + lam * eps_star_in
        d_D1 = D1 - D1_old_cool
        modulus_change_out = sig1_out_curr * d_D1
        modulus_change_in = sig1_in_curr * d_D1
        phase_out = eps0_cool_out * dPhi + modulus_change_out
        phase_in = eps0_cool_in * dPhi + modulus_change_in

        # Тепловой вклад
        thermal1_term = alpha1 * dT
        thermal2_term = alpha2 * dT

        x1 = x2 = x3 = x4 = 0.0
        tol_res = 1e-6
        converged = False

        for it in range(max_iter):
            # 4 уравнения (5 по смыслу: 3 кинематических равенства + N=0),
            # матрица решает неизвестные x1..x4 = dσ по out/in на слоях.
            # (1) dε1_out = dε1_in  -> C1_out*x1 - C1_in*x2 = phase_in - phase_out
            # (1) dε1_out = dε1_in:
            # dε1_out = C1_out*x1 + phase_out + thermal1_term
            # dε1_in  = C1_in*x2  + phase_in  + thermal1_term
            # thermal1_term одинаков для out/in => сокращается:
            RHS1 = (phase_in + thermal1_term) - (phase_out + thermal1_term)
            # (2) dε1_in  = dε2_in  -> C1_in*x2  - C2_in*x4  = thermal2 - phase_in - thermal1
            RHS2 = thermal2_term - phase_in - thermal1_term
            # (3) dε1_out = dε2_out -> C1_out*x1 - C2_out*x3 = thermal2 - phase_out - thermal1
            RHS3 = thermal2_term - phase_out - thermal1_term
            # (4) N=0: h1*(x1+x2) + h2*(x3+x4)=0
            RHS4 = 0.0
            b = numpy.array([RHS1, RHS2, RHS3, RHS4], dtype=float)

            # Коэффициенты (9) от текущего guess для trial-напряжений
            sig1_out_trial = sig1_out_curr + x1
            sig1_in_trial = sig1_in_curr + x2
            sig2_out_trial = sig2_out_curr + x3
            sig2_in_trial = sig2_in_curr + x4

            C1_out_g = effective_compliance_formula_9(
                sig1_out_curr, sig1_out_trial, D1, yield_mix, H1_mix
            )
            C1_in_g = effective_compliance_formula_9(
                sig1_in_curr, sig1_in_trial, D1, yield_mix, H1_mix
            )
            C2_out_g = effective_compliance_formula_9(
                sig2_out_curr, sig2_out_trial, D2, strenght_yield_2, strengthening_coefficient_2
            )
            C2_in_g = effective_compliance_formula_9(
                sig2_in_curr, sig2_in_trial, D2, strenght_yield_2, strengthening_coefficient_2
            )

            A = numpy.array(
                [
                    [C1_out_g, -C1_in_g, 0.0, 0.0],
                    [0.0, C1_in_g, 0.0, -C2_in_g],
                    [C1_out_g, 0.0, -C2_out_g, 0.0],
                    [h1, h1, h2, h2],
                ],
                dtype=float,
            )

            try:
                x_new = numpy.linalg.solve(A, b)
            except numpy.linalg.LinAlgError as e:
                raise ValueError(
                    f"Singular system in cooling: it={it}, t={t}, Fi={Fi}, A={A}, b={b}"
                ) from e

            x1_solved, x2_solved, x3_solved, x4_solved = (
                float(x_new[0]),
                float(x_new[1]),
                float(x_new[2]),
                float(x_new[3]),
            )

            # Проверка согласованности системы на solved-коэффициентах
            sig1_out_trial_s = sig1_out_curr + x1_solved
            sig1_in_trial_s = sig1_in_curr + x2_solved
            sig2_out_trial_s = sig2_out_curr + x3_solved
            sig2_in_trial_s = sig2_in_curr + x4_solved

            C1_out_s = effective_compliance_formula_9(
                sig1_out_curr, sig1_out_trial_s, D1, yield_mix, H1_mix
            )
            C1_in_s = effective_compliance_formula_9(
                sig1_in_curr, sig1_in_trial_s, D1, yield_mix, H1_mix
            )
            C2_out_s = effective_compliance_formula_9(
                sig2_out_curr, sig2_out_trial_s, D2, strenght_yield_2, strengthening_coefficient_2
            )
            C2_in_s = effective_compliance_formula_9(
                sig2_in_curr, sig2_in_trial_s, D2, strenght_yield_2, strengthening_coefficient_2
            )

            A_check = numpy.array(
                [
                    [C1_out_s, -C1_in_s, 0.0, 0.0],
                    [0.0, C1_in_s, 0.0, -C2_in_s],
                    [C1_out_s, 0.0, -C2_out_s, 0.0],
                    [h1, h1, h2, h2],
                ],
                dtype=float,
            )
            x_vec = numpy.array([x1_solved, x2_solved, x3_solved, x4_solved], dtype=float)
            res_vec = A_check @ x_vec - b
            if float(numpy.max(numpy.abs(res_vec))) < tol_res:
                x1, x2, x3, x4 = x1_solved, x2_solved, x3_solved, x4_solved
                C1_out, C1_in, C2_out, C2_in = C1_out_s, C1_in_s, C2_out_s, C2_in_s
                converged = True
                break

            x1, x2, x3, x4 = x1_solved, x2_solved, x3_solved, x4_solved
        if not converged:
            RHS1 = phase_in - phase_out
            RHS2 = thermal2_term - phase_in - thermal1_term
            RHS3 = thermal2_term - phase_out - thermal1_term
            RHS4 = 0.0
            b = numpy.array([RHS1, RHS2, RHS3, RHS4], dtype=float)

            C1_out = D1
            C1_in = D1
            C2_out = D2
            C2_in = D2

            A = numpy.array(
                [
                    [C1_out, -C1_in, 0.0, 0.0],
                    [0.0, C1_in, 0.0, -C2_in],
                    [C1_out, 0.0, -C2_out, 0.0],
                    [h1, h1, h2, h2],
                ],
                dtype=float,
            )
            x_new = numpy.linalg.solve(A, b)
            x1, x2, x3, x4 = float(x_new[0]), float(x_new[1]), float(x_new[2]), float(x_new[3])

        # Финальные trial-напряжения и коэффициенты (9)
        sig1_out_trial = sig1_out_curr + x1
        sig1_in_trial = sig1_in_curr + x2
        sig2_out_trial = sig2_out_curr + x3
        sig2_in_trial = sig2_in_curr + x4
        C1_out = effective_compliance_formula_9(
            sig1_out_curr,
            sig1_out_trial,
            D1,
            yield_mix,
            H1_mix,
        )
        C1_in = effective_compliance_formula_9(
            sig1_in_curr,
            sig1_in_trial,
            D1,
            yield_mix,
            H1_mix,
        )
        C2_out = effective_compliance_formula_9(
            sig2_out_curr,
            sig2_out_trial,
            D2,
            strenght_yield_2,
            strengthening_coefficient_2,
        )
        C2_in = effective_compliance_formula_9(
            sig2_in_curr,
            sig2_in_trial,
            D2,
            strenght_yield_2,
            strengthening_coefficient_2,
        )

        d_sig1 = 0.5 * (x1 + x2)
        d_s1 = 0.5 * (x1 - x2)
        d_sig2 = 0.5 * (x3 + x4)
        d_s2 = 0.5 * (x4 - x3)

        sig1 += d_sig1
        s1 += d_s1
        sig2 += d_sig2
        s2 += d_s2

        force = force_reaction_per_width(sig1, s1, sig2, s2, sig1_ref, s1_ref, sig2_ref, s2_ref)
        list_force.append(force)

        list_sig1.append(sig1)
        list_sig2.append(sig2)
        list_s1.append(s1)
        list_s2.append(s2)

        # t/Fi/alpha
        t += dT
        list_t.append(t)
        Fi_old = Fi
        list_Fi.append(Fi)
        alpha1_old = alpha1
        D1_old_cool = D1

        d_eps_out1 = C1_out * x1 + phase_out + thermal1_term
        d_eps_in1 = C1_in * x2 + phase_in + thermal1_term
        d_eps_out2 = C2_out * x3 + thermal2_term
        d_eps_in2 = C2_in * x4 + thermal2_term

        eps1_out_strain += d_eps_out1
        eps1_in_strain += d_eps_in1
        eps2_out_strain += d_eps_out2
        eps2_in_strain += d_eps_in2

        # Накопление "свободных" деформаций
        eps1_out_phase += phase_out
        eps1_in_phase += phase_in
        eps1_out_therm += thermal1_term
        eps1_in_therm += thermal1_term
        eps2_out_phase += 0.0
        eps2_in_phase += 0.0
        eps2_out_therm += thermal2_term
        eps2_in_therm += thermal2_term

        # "Механические" напряжения как E(T)*ε_mech
        eps1_out_mech = eps1_out_strain - eps1_out_phase - eps1_out_therm
        eps1_in_mech = eps1_in_strain - eps1_in_phase - eps1_in_therm
        eps2_out_mech = eps2_out_strain - eps2_out_phase - eps2_out_therm
        eps2_in_mech = eps2_in_strain - eps2_in_phase - eps2_in_therm
        list_sig1_out_mech.append(E1 * eps1_out_mech)
        list_sig1_in_mech.append(E1 * eps1_in_mech)
        list_sig2_out_mech.append(young_module_2 * eps2_out_mech)
        list_sig2_in_mech.append(young_module_2 * eps2_in_mech)

        try:
            check_plane_sections_hypothesis(
                eps1_out_strain,
                eps1_in_strain,
                eps2_in_strain,
                eps2_out_strain,
                len_o1=len_o1,
                delta=delta,
                h1=h1,
                h2=h2,
                context="cooling",
                apply_delta_correction=True,
            )
        except ValueError:
            pass

    return (
        sig1,
        s1,
        sig2,
        s2,
        list_force[-1],
        eps1_out_strain,
        eps1_in_strain,
        eps2_out_strain,
        eps2_in_strain,
        list_t,
        list_sig1,
        list_sig2,
        list_s1,
        list_s2,
        list_force,
        list_sig1_out_mech,
        list_sig1_in_mech,
        list_sig2_out_mech,
        list_sig2_in_mech,
    )
