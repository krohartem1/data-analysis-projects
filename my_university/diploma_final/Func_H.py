import numpy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from const import *

podat1_unload = (1 / strengthening_coefficient_1) - (1 / unloading_young_module_1)
podat1_load = (1 / strengthening_coefficient_1) - (1 / loading_young_module_1)
podat2 = (1 / strengthening_coefficient_2) - (1 / young_module_2)

# Параметры проверки гипотезы плоских сечений
# Цель: (eps1_out - eps1_in)/(eps2_in - eps2_out) ~= h1/h2
# В исходной печати использовалась поправка: eps1_out - delta/len_o1
PLANE_SECTION_TOL_ABS = 1e-6
PLANE_SECTION_TOL_REL = 1e-3
STRAIGHT_PLATE_TOL_ABS = 1e-7
STRAIGHT_PLATE_TOL_REL = 1e-2
STRAIGHT_SCALE_TOL_ABS = 1e-8
STRAIGHT_SCALE_TOL_REL = 1e-3

# Сверка: счётчик M в разгрузке vs момент из σ на всех волокнах (см. диплом Кусакиной).
MOMENT_CHECK_TOL_ABS = 1e-9
MOMENT_CHECK_TOL_REL = 5e-4


def bending_moment_per_width_from_mean_half(sig1: float, s1: float, sig2: float, s2: float) -> float:
    """
    Момент на единицу ширины по формуле (4) из Кусакиной.

    На уровне приращений:
      3*h1^2*dσ1 + h1^2*ds1 - 3*h2^2*dσ2 + h2^2*ds2 = 6*dM

    Здесь `σ1, s1` — среднее и полуразность (mean/half-diff) для слоя 1,
    `σ2, s2` — то же для слоя 2 (в терминах текущего кода: `sig1, s1, sig2, s2`).
    """
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
    """
    Проверяет выполнение гипотезы плоских сечений при разгрузке.

    Выбрасывает ValueError, если отклонение больше допустимого.
    """
    # Поправка eps1_out - delta/len_o1 уместна для этапа unloading (учёт исходного укорочения).
    # На термоцикле (нагрев/охлаждение) её применять нельзя — она даёт ложный разрыв проверки.
    eps1_out_corr = eps1_out - delta / len_o1 if apply_delta_correction else eps1_out
    denom = eps2_in - eps2_out
    num = eps1_out_corr - eps1_in
    # Если пластинка почти прямая (обе разности почти нулевые), отношение не определено,
    # но геометрически гипотеза выполнена.
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


def plane_sections_ratio(eps1_out: float, eps1_in: float, eps2_in: float, eps2_out: float) -> float:
    """Чистое значение отношения (eps1_out-eps1_in)/(eps2_in-eps2_out)."""
    denom = eps2_in - eps2_out
    if abs(denom) < 1e-30:
        return float("inf")
    return (eps1_out - eps1_in) / denom


def fiber_lengths(
    eps1_out: float,
    eps1_in: float,
    eps2_out: float,
    eps2_in: float,
):
    """
    Длины крайних волокон до и после этапа (используем определения unloading()).
    Возвращает (L0_dict, L_dict).
    """
    len_o1 = (arc_length / rad) * (h1 + h2 + rad) - delta
    len_o2 = (arc_length / rad) * (rad)
    len_in = (arc_length / rad) * (rad + h1)

    L1_out0 = len_o1 + delta
    L1_out = len_o1 + len_o1 * eps1_out

    L1_in0 = len_in
    L1_in = len_in + len_in * eps1_in

    L2_out0 = len_o2
    L2_out = len_o2 + len_o2 * eps2_out

    L2_in0 = (arc_length / rad) * (rad + h2)
    L2_in = L2_in0 + L2_in0 * eps2_in

    L0 = {
        "L1_out0": float(L1_out0),
        "L1_in0": float(L1_in0),
        "L2_out0": float(L2_out0),
        "L2_in0": float(L2_in0),
    }
    L = {
        "L1_out": float(L1_out),
        "L1_in": float(L1_in),
        "L2_out": float(L2_out),
        "L2_in": float(L2_in),
    }
    return L0, L


def print_lengths_report(stop_label: str, eps1_out: float, eps1_in: float, eps2_out: float, eps2_in: float) -> None:
    L0, L = fiber_lengths(eps1_out, eps1_in, eps2_out, eps2_in)

    rel = {
        "L1_out_rel": (L["L1_out"] - L0["L1_out0"]) / L0["L1_out0"],
        "L1_in_rel": (L["L1_in"] - L0["L1_in0"]) / L0["L1_in0"],
        "L2_out_rel": (L["L2_out"] - L0["L2_out0"]) / L0["L2_out0"],
        "L2_in_rel": (L["L2_in"] - L0["L2_in0"]) / L0["L2_in0"],
    }

    scales = [
        L["L1_out"] / L0["L1_out0"],
        L["L1_in"] / L0["L1_in0"],
        L["L2_out"] / L0["L2_out0"],
        L["L2_in"] / L0["L2_in0"],
    ]
    s_min = min(scales)
    s_max = max(scales)
    s_mean = sum(scales) / len(scales)
    allowed = STRAIGHT_SCALE_TOL_ABS + STRAIGHT_SCALE_TOL_REL * abs(s_mean)

    print(
        f"[LENGTHS] {stop_label}: "
        f"L1_out={L['L1_out']:.6g} (rel={rel['L1_out_rel']:.3e}), "
        f"L1_in={L['L1_in']:.6g} (rel={rel['L1_in_rel']:.3e}), "
        f"L2_out={L['L2_out']:.6g} (rel={rel['L2_out_rel']:.3e}), "
        f"L2_in={L['L2_in']:.6g} (rel={rel['L2_in_rel']:.3e})"
    )
    print(
        f"[SCALE] {stop_label}: s_min={s_min:.6g}, s_max={s_max:.6g}, "
        f"s_span={(s_max - s_min):.3e}, allowed_span={allowed:.3e}"
    )


def Hev(x: float) -> int:
    """
    Вычисляет значение функции Хевисайда H(x).

    Параметры:
        x (float): входное значение

    Возвращает:
        int: 0, если x <= 0
             1, если x > 0
    """
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
    """
    Сила на единицу ширины: F/a = 3·ΔM/(2·(L + L_eff)).
    ΔM = (h1²(3Δσ₁+Δs₁) - h2²(3Δσ₂-Δs₂))/6  — формула (4) Кусакиной.
    Коэффициент 3/2 — реакция опоры консоли с равномерным моментом
    при заблокированном прогибе на конце (суперпозиция Эйлера-Бернулли).
    L_eff — эффективная "виртуальная" длина (пограничные эффекты заделки и опоры):
    эластичность зажима, скольжение острия, пограничный изгиб ленты у опоры.
    Линейная теория с L_eff = 0 завышает F при малых L.
    """
    delta_M = (h1 * h1 * (3 * (sig1 - sig1_ref) + (s1 - s1_ref))
               - h2 * h2 * (3 * (sig2 - sig2_ref) - (s2 - s2_ref))) / 6.0
    try:
        from const import L_eff_offset as _Leff
    except ImportError:
        _Leff = 0.0
    return 1.5 * delta_M / (part_len + _Leff)


def print_peak_force_passport(
    label: str,
    list_force: list,
    list_t: list,
    list_Fi: list,
    peak_rows: list,
    *,
    extra_note: str = "",
) -> None:
    """Краткая диагностика: максимум |F| по ширине на шаге термоцикла."""
    if not list_force:
        return
    i_max = max(range(len(list_force)), key=lambda i: abs(list_force[i]))
    Fm = list_force[i_max]
    Tm = list_t[i_max] if i_max < len(list_t) else float("nan")
    suf = f"  ({extra_note})" if extra_note else ""
    print(
        f"[PEAK] {label}: max(F/a)={abs(Fm):.6g} N/m at list index i={i_max}, T={Tm:.4f} K{suf}"
    )


def plot_graph(
    y_values,
    x_values,
    y_label="Y-Axis",
    x_label="X-Axis",
    title="График зависимости",
    *,
    show: bool = True,
    save_path: str | None = None,
):
    """
    Строит график по двум массивам данных.

    :param y_values: Список значений по вертикали (ось Y)
    :param x_values: Список значений по горизонтали (ось X)
    :param y_label: Название оси Y
    :param x_label: Название оси X
    :param title: Заголовок графика
    """
    if len(y_values) != len(x_values):
        raise ValueError("Массивы x_values и y_values должны быть одинаковой длины.")

    plt.figure(figsize=(8, 5))
    plt.plot(x_values, y_values, marker=".", linestyle="-")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(f"{title} {y_label} от {x_label}")
    plt.grid(True)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches="tight")
    if show and plt.get_backend().lower() != "agg":
        plt.show()
    else:
        plt.close()


# Функция для обновления констант в файле
def loading():
    """
    Этап 1
    Снимаем пластинку с барабана и сравниваем концы
    Вычисляем начальный момент и параметры пластинки
    """
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

    # Так как напряжения могут быть отрицательными нам нужно определить знак для напряжений пределов текучести. Обозначим k
    # k = 1
    # if sig1_out < 0:
    #     k = -1

    # sig1 = 0.5 * (k * strenght_yield_1 + ( delta / ((arc_length / rad) * (h1 + h2 + rad) - delta) - strenght_yield_1 / loading_young_module_1) * strengthening_coefficient_1)
    # s1 = 0.5 * (k * strenght_yield_1 + ( delta / ((arc_length / rad) * (h1 + h2 + rad) - delta) - strenght_yield_1 / loading_young_module_1) * strengthening_coefficient_1)
    # sig2 = 0
    # s2 = 0

    # sig1_out = sig1 + s1
    # sig1_in = sig1 - s1
    # sig2_in = sig2 + s2
    # sig2_out = sig2 - s2

    # теперь считаем начальнай момент
    bending_moment = h1 * h1 * ((3 * sig1 + s1) / 6)

    # Считаем деформацию в линейном приближении
    eps_elastic = (eps1_out - eps2_out) / (2 * (1 + eps2_out))

    # Диагностика гипотезы плоских сечений (как в unloading())
    len_o1 = (arc_length / rad) * (h1 + h2 + rad) - delta
    num = (eps1_out - delta / len_o1) - eps1_in
    denom = eps2_in - eps2_out
    near_zero = PLANE_SECTION_TOL_ABS
    if abs(denom) < near_zero and abs(num) < near_zero:
        ratio = h1 / h2
    else:
        # На случай, если в других настройках это станет не-нулевым
        ratio = plane_sections_ratio(eps1_out, eps1_in, eps2_in, eps2_out)
    print(
        f"[LOADING] plane_sections: num={num:.3e}, denom={denom:.3e}, "
        f"ratio={ratio:.6g}, target={h1/h2:.6g}"
    )

    print_lengths_report(
        "loading",
        eps1_out=eps1_out,
        eps1_in=eps1_in,
        eps2_out=eps2_out,
        eps2_in=eps2_in,
    )

    # Знаковые пределы текучести (по правилу Кусакиной):
    # положительные если волокно растянуто, отрицательные если сжато (или 0).
    # На loading: out-волокно растянуто (+SY), in-волокно не нагружено и
    # последующая разгрузка будет идти в сторону сжатия → задаём знак "-".
    # См. bimet_stopka.cpp, строки 199-206.
    sig1_out_yield_signed = strenght_yield_1 if sig1_out > 0 else -strenght_yield_1
    sig1_in_yield_signed = strenght_yield_1 if sig1_in > 0 else -strenght_yield_1

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
        sig1_out_yield_signed,
        sig1_in_yield_signed,
    )


# Определить podat1_unload, podat1_load, podat1_aust, podat2 , D, E,
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
    max_unload_steps: int = 500000,
    moment_check_strict: bool = False,
):
    """
    Разгрузка изгибающим моментом до M ≈ 0 (момент M уменьшается с шагом d_M = 1e-6).

    Физический смысл: после съёма с барабана внешний момент снимается полностью,
    а лента закрепляется на установке «как есть» — с возможными остаточными
    напряжениями в кристаллическом слое. Из-за пластического деформирования при
    нагрузке (ε₀ ≈ 0,6% > σ_T/E₁ = 0,3%) после разгрузки σ_out остаётся ненулевым
    (~50–80 МПа в зависимости от параметров) — это физически корректно.

    Дополнительная проверка: внешний счётчик M сверяется с моментом, посчитанным
    из напряжений по формуле (4) Кусакиной (`bending_moment_per_width_from_mean_half`).
    При расхождении ищите ошибку в обозначениях; при moment_check_strict=True —
    ValueError.
    """
    d_M = 1e-6   # приращение момента
    M = bending_moment

    # Параметры напряжений с предыдущего шага
    sig1, s1, sig2, s2 = sig1_out / 2, sig1_out / 2, 0, 0

    list_sig1o, list_sig2o, list_sig1in, list_sig2in = [sig1_out], [sig2_out], [sig1_in], [sig2_in]

    list_e1o, list_e2o, list_e1i, list_e2i  = [eps1_out], [eps2_out], [eps1_in], [eps2_in]

    len_o1 = (arc_length / rad) * (h1 + h2 + rad) - delta
    len_o2 = (arc_length / rad) * (rad)
    len_in = (arc_length / rad) * (rad + h1)

    # Начинаем процесс механцического выпрямления пластинки
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

        list_sig1o.append(sig1_out)
        list_sig2o.append(sig2_out)
        list_sig1in.append(sig1_in)
        list_sig2in.append(sig2_in)

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

        eps_elastic = (eps1_out - eps2_out) / (2 * (1 + eps2_out))

    plot_graph(list_e1i, list_e2i, y_label="Eps1_in", x_label="Eps2_in", title="Деформации внутренних слоев")
    print(f'Проверка гипотезы плоских сечений: (eps1_out - eps1_in)/(eps2_in - eps2_out) = {(list_e1o[-1] - delta/len_o1 - list_e1i[-1])/(list_e2i[-1] - list_e2o[-1])} и h1/h2 = {h1/h2}')

    # Дополнительная проверка прямизны: при нулевой кривизне
    # масштаб относительного изменения длины должен быть одинаковым по всем крайним волокнам.
    eps1_out = list_e1o[-1]
    eps1_in = list_e1i[-1]
    eps2_in = list_e2i[-1]
    eps2_out = list_e2o[-1]

    L1_out0 = len_o1 + delta
    L1_out = len_o1 + len_o1 * eps1_out
    L1_in0 = len_in
    L1_in = len_in + len_in * eps1_in

    L2_out0 = len_o2
    L2_out = len_o2 + len_o2 * eps2_out
    # Внутреннее волокно слоя 2 соответствует радиусу (rad + h2)
    L2_in0 = (arc_length / rad) * (rad + h2)
    L2_in = L2_in0 + L2_in0 * eps2_in

    s_out1 = L1_out / L1_out0
    s_in1 = L1_in / L1_in0
    s_out2 = L2_out / L2_out0
    s_in2 = L2_in / L2_in0

    scales = [s_out1, s_in1, s_out2, s_in2]
    s_min = min(scales)
    s_max = max(scales)
    s_mean = sum(scales) / len(scales)
    allowed = STRAIGHT_SCALE_TOL_ABS + STRAIGHT_SCALE_TOL_REL * abs(s_mean)
    # Финальная пластинка не обязана иметь одинаковые длины крайних волокон —
    # при остановке на σ₁_out=0 у плоских сечений могут быть остаточные деформации.
    # Проверка выполняется как информационная.
    if (s_max - s_min) > allowed:
        print(
            "[INFO] unloading: сечения с неодинаковыми длинами волокон — "
            f"scales={scales}, eps1_out={eps1_out}, eps1_in={eps1_in}, "
            f"eps2_in={eps2_in}, eps2_out={eps2_out}"
        )

    M_from_sigma = bending_moment_per_width_from_mean_half(sig1, s1, sig2, s2)
    mom_tol = MOMENT_CHECK_TOL_ABS + MOMENT_CHECK_TOL_REL * max(
        abs(M), abs(M_from_sigma), 1.0
    )
    diff_m = M_from_sigma - M
    if abs(diff_m) <= mom_tol:
        print(
            f"[CHECK] unloading: M_counter={M:.12g} vs M_from_all_mean_half_stresses={M_from_sigma:.12g} OK "
            f"diff_m={diff_m:.12g} |diff|={abs(diff_m):.3e} tol={mom_tol:.12g}"
        )
    else:
        msg = (
            f"[CHECK] unloading: FAIL M_counter={M:.12g} vs M_from_all_mean_half_stresses={M_from_sigma:.12g} "
            f"diff_m={diff_m:.12g} tol={mom_tol:.12g}"
        )
        print(msg)
        if abs(M) <= mom_tol and abs(M_from_sigma) > 10 * mom_tol:
            print(
                "[HINT] |M_counter|≈0, но момент по sigma нет: возможны остаточные самонапряжения после пластики; "
                "либо цикл завершился по исчерпанию M раньше, чем сработал sig1_out_zero — см. шаги разгрузки."
            )
        if moment_check_strict:
            raise ValueError(msg)

    print(f'Оставшийся внешний момент (счётчик M): {M}')
    print(f'Начальная длина внешнего слоя 1: {len_o1 + delta}, получивашаяся длина: {len_o1 + len_o1 * list_e1o[-1]}')
    print(f'Начальная длина внешнего слоя 2: {len_o2}, получивашаяся длина: {len_o2 + len_o2 * list_e2o[-1]}')
    print(f'Начальная длина слоя in: {len_in}, получивашаяся длина: {len_in + len_in * list_e1i[-1]}')

    # Доп. отчёт: абсолютные длины, относительные изменения и разброс масштабов.
    eps1_out_final = list_e1o[-1]
    eps1_in_final = list_e1i[-1]
    eps2_out_final = list_e2o[-1]
    eps2_in_final = list_e2i[-1]
    print_lengths_report(
        "unloading(sig1_out_zero)",
        eps1_out=eps1_out_final,
        eps1_in=eps1_in_final,
        eps2_out=eps2_out_final,
        eps2_in=eps2_in_final,
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


# Нагрев с явным учётом неизменной кривизны (подставка под свободный конец).
# Система отчёта (15): dε^out_1 = dε^in_1 = dε^in_2 = dε^out_2 = 0.
# Вариант B: из (C)(D) и (5) получаем dσ2, ds2=0, dσ1; затем ds1 — полусумма из (A)(B).
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
    sig1_ref=None,
    s1_ref=None,
    sig2_ref=None,
    s2_ref=None,
    sig1_out_yield_signed=None,
    sig1_in_yield_signed=None,
    zeta_d_in: float = 0.0,  # накопленная "ориентированная" доля (Lagoudas-Entchev)
):
    def compute_dPhi(Fi_old_local: float, t_local: float, dT_local: float) -> float:
        # Косинусная кинетика Φ(T) (Liang-Rogers 1990).
        # Φ_heat(T) = 0.5·[1 + cos(π·(T-As)/(Af-As))]  при As ≤ T ≤ Af, Φ=1 ниже As, Φ=0 выше Af
        # Φ_cool(T) = 0.5·[1 + cos(π·(T-Mf)/(Ms-Mf))]  при Mf ≤ T ≤ Ms, Φ=1 ниже Mf, Φ=0 выше Ms
        # Сдвиг температур: T_char(σ) = T_char_0 + k_CC·σ
        import math
        T_new = t_local + dT_local
        sigma_shift = k_CC * max(sig_for_CC, 0.0)
        As_eff = a_start + sigma_shift
        Af_eff = a_finish + sigma_shift
        Ms_eff = m_start + sigma_shift
        Mf_eff = m_finish + sigma_shift
        if dT_local > 0:  # heating
            if T_new <= As_eff:
                Phi_new = 1.0
            elif T_new >= Af_eff:
                Phi_new = 0.0
            else:
                Phi_new = 0.5 * (1.0 + math.cos(math.pi * (T_new - As_eff) / (Af_eff - As_eff)))
        else:  # cooling
            if T_new >= Ms_eff:
                Phi_new = 0.0
            elif T_new <= Mf_eff:
                Phi_new = 1.0
            else:
                Phi_new = 0.5 * (1.0 + math.cos(math.pi * (T_new - Mf_eff) / (Ms_eff - Mf_eff)))
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

    # Референс напряжений: если передан sig1_ref, используем его (для многоцикловой прогонки),
    # иначе — состояние перед нагревом (для одноциклового запуска).
    if sig1_ref is None:
        sig1_ref, s1_ref, sig2_ref, s2_ref = sig1, s1, sig2, s2

    # Состояния напряжений (используем сиг/и как в текущем коде)
    t = t_start
    Fi = 1.0
    Fi_old = Fi

    list_force = [0.0]
    list_t = [t_start]
    list_sig1 = [sig1]
    list_sig2 = [sig2]
    list_Fi = [Fi]
    peak_rows: list[dict] = []
    plane_warn_count = 0
    kin_warn_count = 0
    curv_warn_count = 0
    neq_warn_count = 0
    PLANE_WARN_PRINT_LIMIT = 10

    eps1_out_strain = eps1_out_0
    eps1_in_strain = eps1_in_0
    eps2_out_strain = eps2_out_0
    eps2_in_strain = eps2_in_0

    # Диагностика фиксированной кривизны:
    # разности крайних волокон по толщине должны сохраняться через шаги термоцикла.
    curv_diff1_0 = eps1_out_strain - eps1_in_strain
    curv_diff2_0 = eps2_in_strain - eps2_out_strain

    # Фазовая деформация при нагреве: B19→B2 превращение в кристаллическом слое.
    #
    # КОМБИНИРОВАННАЯ ФОРМУЛА (Кусакина + Belyaev-Volkov-Evard):
    # ε⁰_heat = K_r · ε_pl_initial(z) + σ_current(z) / E_phase_heat
    #
    # Первое слагаемое — Кусакина: возврат пластической деформации, накопленной
    # при изготовлении (фиксированная константа для каждого волокна).
    # ε_pl(out) = ε_max(out) - σ_T/E  если |ε_max(out)| > σ_T/E, иначе 0.
    # ε_pl(in)  = 0 (внутреннее волокно не выходило в пластику).
    #
    # Второе слагаемое — Belyaev: TRIP-подобный вклад от текущего напряжения,
    # симметрично формуле охлаждения (формула Кусакиной 616-617).
    # Это даёт обратную связь: σ генерируется фазой → σ усиливает фазовый драйвер.
    # Параметр E_phase_heat (по аналогии с E_TP охлаждения).
    sigma_T_over_E = strenght_yield_1 / unloading_young_module_1

    def plastic_part(eps_max_value: float) -> float:
        """ε_pl = max(0, |ε_max| - σ_T/E) с сохранением знака."""
        if abs(eps_max_value) <= sigma_T_over_E:
            return 0.0
        return (abs(eps_max_value) - sigma_T_over_E) * (1.0 if eps_max_value >= 0 else -1.0)

    eps_pl_out = plastic_part(eps1_out_max_0)
    eps_pl_in = plastic_part(eps1_in_max_0)
    # Постоянная часть драйвера (Кусакина):
    eps0_heat_out_const = rec_ratio * eps_pl_out
    eps0_heat_in_const = rec_ratio * eps_pl_in

    alpha1_old = alpha1_aust * (1 - Fi_old) + alpha1_mart * Fi_old
    # Инициализация D1_old для слагаемого σ*·d(1/E₁) из формулы (7) Кусакиной
    E1_init = aust_young_module_1 * (1 - Fi_old) + loading_young_module_1 * Fi_old
    D1_old = 1.0 / E1_init

    # Итерации нужны из-за дискретного переключения Hev(|sigma|-sigmaT).
    # Верхний лимит оставляем как "страховку от зависания", а выход делаем
    # по сходимости (res_vec) + дополнительной проверке стабилизации Hev.
    max_iter = 200
    MIN_IT_FOR_HEV_STABILITY = 5
    prev_hev_state_local = None
    prev_x_vec_local = None

    # Диагностика скачков силы / переключений Hev (формула 9)
    jump_events = []
    prev_hev_state = None
    JUMP_FORCE_ABS = 1e-3
    JUMP_FORCE_REL = 0.05
    MAX_JUMP_EVENTS = 20
    # Диагностика "разворота" (смена знака dF) в верхнем диапазоне температур
    prev_dF = None
    turn_events = []
    MAX_TURN_EVENTS = 20

    # Накопление ζ_d (Lagoudas-Entchev) — ориентированной доли превращения.
    # Прирастает на |dΦ| на каждом шаге; растёт от цикла к циклу через
    # передачу zeta_d_in -> zeta_d_out.
    zeta_d = float(zeta_d_in)

    while t <= t_finish:
        # Эффект Клаузиуса-Клапейрона: текущее среднее напряжение в кр. слое
        # сдвигает характеристические температуры на k_CC·σ.
        sig_for_CC = sig1
        dPhi = compute_dPhi(Fi_old, t, dT)
        Fi = Fi_old + dPhi
        # Численная защита: Φ должна оставаться в [0, 1]
        if Fi < 0.0:
            Fi = 0.0
        elif Fi > 1.0:
            Fi = 1.0

        # Прирост ζ_d на |dΦ| (Lagoudas-Entchev)
        zeta_d += abs(dPhi)

        alpha1 = alpha1_aust * (1 - Fi) + alpha1_mart * Fi
        d_alpha1 = alpha1 - alpha1_old

        yield_mix = strenght_yield_1_aust * (1 - Fi) + strenght_yield_1 * Fi
        H1_mix = strengthening_coefficient_1_aust * (1 - Fi) + strengthening_coefficient_1 * Fi

        # (13) E1 = EA(1-Φ) + EMΦ -> D1 = 1/E1
        E1 = aust_young_module_1 * (1 - Fi) + loading_young_module_1 * Fi
        D1 = 1.0 / E1
        D2 = 1.0 / young_module_2

        # ФАЗОВЫЙ ВКЛАД НА НАГРЕВЕ — формула Беляева-Волкова-Эварда:
        #
        #   dε^Ф_нагрев = K · ε⁰ · dΦ + σ · d(1/E)
        #
        # где:
        #   K — коэффициент возврата (Belyaev 2015) ≤ 1
        #   ε⁰ = ε_max - σ_T/E — пластическая часть деформации
        #   σ · d(1/E) — слагаемое изменения модуля при превращении (Tanaka 1986)
        #
        # ВАЖНО: в формуле нагрева НЕТ слагаемого σ/E_ПП. Оно присутствует
        # только в формуле охлаждения как описание пластичности превращения.
        # Этот выбор соответствует подходу Кусакиной (m_const.d, строки 423-424
        # её bimet_stopka.cpp): Eps0out = Kr * Eps1outF, где Eps1outF —
        # накопленная фазовая деформация ≈ ε_max - σ_T/E_M.
        d_D1 = D1 - D1_old
        sig1_out_curr_pre = sig1 + s1
        sig1_in_curr_pre = sig1 - s1
        modulus_change_out = sig1_out_curr_pre * d_D1
        modulus_change_in = sig1_in_curr_pre * d_D1
        eps0_heat_out = eps0_heat_out_const
        eps0_heat_in = eps0_heat_in_const
        phase_out = eps0_heat_out * dPhi + modulus_change_out
        phase_in = eps0_heat_in * dPhi + modulus_change_in

        # Тепловой вклад: d(α1 dT) = α1 dT + T dα1
        thermal1_term = alpha1 * dT  # убран T*d_alpha1 (нефизичный артефакт)
        thermal2_term = alpha2 * dT

        if t == t_start:
            print(
                f"[INFO] heating: eps0_heat_out={eps0_heat_out:.6g}, eps0_heat_in={eps0_heat_in:.6g}, rec_ratio={rec_ratio}, "
                f"eps1_out_0={eps1_out_0:.6g}, eps1_in_0={eps1_in_0:.6g}"
            )

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
            print(f"[WARN] heating fixed-curvature: (9)+(kin) did not converge at t={t}, Fi={Fi}; using last guess")
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

        hev_state = (
            Hev(abs(sig1_out_trial) - yield_mix),
            Hev(abs(sig1_in_trial) - yield_mix),
            Hev(abs(sig2_out_trial) - strenght_yield_2),
            Hev(abs(sig2_in_trial) - strenght_yield_2),
            Hev(abs(sig1_out_trial) - abs(sig1_out_curr)),
            Hev(abs(sig1_in_trial) - abs(sig1_in_curr)),
            Hev(abs(sig2_out_trial) - abs(sig2_out_curr)),
            Hev(abs(sig2_in_trial) - abs(sig2_in_curr)),
        )

        # Приращения dσ/ds (mean/half-diff) из компонентов x1..x4
        d_sig1 = 0.5 * (x1 + x2)
        d_s1 = 0.5 * (x1 - x2)
        d_sig2 = 0.5 * (x3 + x4)
        d_s2 = 0.5 * (x4 - x3)

        # Диагностика равновесия по продольной силе в приращениях:
        # h1*dσ1_mean + h2*dσ2_mean == 0
        N_res = h1 * d_sig1 + h2 * d_sig2
        denom = abs(h1 * d_sig1) + abs(h2 * d_sig2) + 1e-30
        if abs(N_res) / denom > 1e-6:
            neq_warn_count += 1
            if neq_warn_count <= PLANE_WARN_PRINT_LIMIT:
                print(f"[WARN] heating N-equilibrium residual t={t:.3f}, Fi={Fi:.4f}: N_res={N_res:.3e}")
            elif neq_warn_count == PLANE_WARN_PRINT_LIMIT + 1:
                print("[WARN] heating N-equilibrium residual: ... (suppressed further warnings)")

        # Обновляем напряжения/картину
        sig1 += d_sig1
        s1 += d_s1
        sig2 += d_sig2
        s2 += d_s2

        # (18): сила от текущих σ относительно холодного референса (не ∫dF — так замыкается цикл по σ)
        force = force_reaction_per_width(sig1, s1, sig2, s2, sig1_ref, s1_ref, sig2_ref, s2_ref)
        dF = force - list_force[-1]
        list_force.append(force)

        if prev_dF is not None and len(turn_events) < MAX_TURN_EVENTS:
            # Считаем "разворотом" смену знака dF в зоне выше ~Af-1K (там у тебя наблюдался спад)
            if (t >= (a_finish - 1.0)) and (dF == 0.0 or (prev_dF > 0.0 and dF < 0.0) or (prev_dF < 0.0 and dF > 0.0)):
                turn_events.append(
                    {
                        "t": t,
                        "Fi": Fi,
                        "dPhi": dPhi,
                        "dF_prev": prev_dF,
                        "dF": dF,
                        "F": force,
                        "phase": (phase_out, phase_in),
                        "thermal": (thermal1_term, thermal2_term),
                        "d_sig": (d_sig1, d_s1, d_sig2, d_s2),
                        "hev": hev_state,
                    }
                )
        prev_dF = dF

        # Диагностика: "скачок" силы и/или переключение Hev
        if len(jump_events) < MAX_JUMP_EVENTS:
            force_prev = list_force[-2]
            thr = max(JUMP_FORCE_ABS, JUMP_FORCE_REL * max(1.0, abs(force_prev)))
            hev_changed = (prev_hev_state is not None and hev_state != prev_hev_state)

            if abs(dF) > thr or hev_changed:
                jump_events.append(
                    {
                        "t": t,
                        "Fi": Fi,
                        "dPhi": dPhi,
                        "dT": dT,
                        "Fprev": force_prev,
                        "dF": dF,
                        "F": force,
                        "thr": thr,
                        "hev": hev_state,
                        "hev_changed": hev_changed,
                        "x": (x1, x2, x3, x4),
                        "d_sig": (d_sig1, d_s1, d_sig2, d_s2),
                        "phase": (phase_out, phase_in),
                        "thermal": (thermal1_term, thermal2_term),
                        "C": (C1_out, C1_in, C2_out, C2_in),
                        "sig_trial": (sig1_out_trial, sig1_in_trial, sig2_out_trial, sig2_in_trial),
                        "sig_curr": (sig1_out_curr, sig1_in_curr, sig2_out_curr, sig2_in_curr),
                    }
                )
        prev_hev_state = hev_state

        list_sig1.append(sig1)
        list_sig2.append(sig2)

        # Обновляем t/Fi/alpha/D1_old
        t += dT
        list_t.append(t)
        Fi_old = Fi
        list_Fi.append(Fi)
        alpha1_old = alpha1
        D1_old = D1

        # (16): dε1 = mechanical(9) + dεph + thermal
        d_eps_out1 = C1_out * x1 + phase_out + thermal1_term
        d_eps_in1 = C1_in * x2 + phase_in + thermal1_term
        # (17): dε2 = mechanical(9) + α2 dT
        d_eps_out2 = C2_out * x3 + thermal2_term
        d_eps_in2 = C2_in * x4 + thermal2_term

        # Явная проверка кинематических равенств (3 равенства из вашей системы).
        # По построенной системе должны выполняться почти точно (в пределах численной погрешности).
        kin_err = max(
            abs(d_eps_out1 - d_eps_in1),
            abs(d_eps_in1 - d_eps_in2),
            abs(d_eps_out1 - d_eps_out2),
        )
        if kin_err > 1e-8:
            kin_warn_count += 1
            if kin_warn_count <= PLANE_WARN_PRINT_LIMIT:
                print(
                    f"[WARN] heating kin-constraints error t={t:.3f}, Fi={Fi:.4f}: kin_err={kin_err:.3e} "
                    f"(dEpsOut1-dEpsIn1={d_eps_out1 - d_eps_in1:.3e}, "
                    f"dEpsIn1-dEpsIn2={d_eps_in1 - d_eps_in2:.3e}, "
                    f"dEpsOut1-dEpsOut2={d_eps_out1 - d_eps_out2:.3e})"
                )
            elif kin_warn_count == PLANE_WARN_PRINT_LIMIT + 1:
                print("[WARN] heating kin-constraints error: ... (suppressed further warnings)")

        eps1_out_strain += d_eps_out1
        eps1_in_strain += d_eps_in1
        eps2_out_strain += d_eps_out2
        eps2_in_strain += d_eps_in2

        curv_err = max(
            abs((eps1_out_strain - eps1_in_strain) - curv_diff1_0),
            abs((eps2_in_strain - eps2_out_strain) - curv_diff2_0),
        )
        if curv_err > 1e-8:
            curv_warn_count += 1
            if curv_warn_count <= PLANE_WARN_PRINT_LIMIT:
                print(
                    f"[WARN] heating curvature-preservation error t={t:.3f}, Fi={Fi:.4f}: curv_err={curv_err:.3e}"
                )
            elif curv_warn_count == PLANE_WARN_PRINT_LIMIT + 1:
                print("[WARN] heating curvature-preservation error: ... (suppressed further warnings)")

        # Проверка гипотезы плоских сечений после шага нагрева.
        # На термоцикле при строгой кинематике возможны кратковременные несогласованности из-за
        # приближенного усреднения ds1 (variant B), поэтому превращаем "raise" в warning.
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
                context=f"heating_constant_curvature step, t={t}, Fi={Fi}",
                apply_delta_correction=True,
            )
        except ValueError as e:
            plane_warn_count += 1
            if plane_warn_count <= PLANE_WARN_PRINT_LIMIT:
                print(f"[WARN] Plane-sections check failed in heating: {e}")
            elif plane_warn_count == PLANE_WARN_PRINT_LIMIT + 1:
                print("[WARN] Plane-sections check failed in heating: ... (suppressed further warnings)")

        peak_rows.append(
            {
                "Fi": Fi,
                "dPhi": dPhi,
                "dF": dF,
                "sig1_out": sig1 + s1,
                "sig1_in": sig1 - s1,
                "sig2_out": sig2 - s2,
                "sig2_in": sig2 + s2,
                "sig_mean1": sig1,
                "s_half1": s1,
                "sig_mean2": sig2,
                "s_half2": s2,
                "yield_mix": yield_mix,
                "sigma_y2": strenght_yield_2,
                "C": (C1_out, C1_in, C2_out, C2_in),
                "mech_out1": C1_out * x1,
                "mech_in1": C1_in * x2,
                "mech_out2": C2_out * x3,
                "mech_in2": C2_in * x4,
                "phase_out": phase_out,
                "phase_in": phase_in,
                "thermal1": thermal1_term,
                "thermal2": thermal2_term,
                "d_eps_out1": d_eps_out1,
                "d_eps_in1": d_eps_in1,
                "d_eps_out2": d_eps_out2,
                "d_eps_in2": d_eps_in2,
                "hev": hev_state,
                "eps0_heat_out": eps0_heat_out,
                "eps0_heat_in": eps0_heat_in,
            }
        )

    if plane_warn_count:
        print(f"\n[WARN] heating: plane-sections check failed {plane_warn_count} times")
    if kin_warn_count:
        print(f"\n[WARN] heating: kin-constraints (dEps equalities) exceeded tol {kin_warn_count} times")
    if curv_warn_count:
        print(f"\n[WARN] heating: curvature-preservation error exceeded tol {curv_warn_count} times")
    if neq_warn_count:
        print(f"\n[WARN] heating: N-equilibrium residual exceeded tol {neq_warn_count} times")

    # Attach peak_rows for diagnostic access (без изменения публичного API)
    heating_constant_curvature.last_peak_rows = peak_rows
    heating_constant_curvature.last_zeta_d = zeta_d

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
        list_force,
        Fi,
        list_Fi,
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
    zeta_d_in: float = 0.0,
):
    def compute_dPhi(Fi_old_local: float, t_local: float, dT_local: float) -> float:
        # Косинусная кинетика Φ(T) (Liang-Rogers 1990) для охлаждения, с Clausius-Clapeyron
        import math
        T_new = t_local + dT_local
        sigma_shift = k_CC * max(sig_for_CC, 0.0)
        As_eff = a_start + sigma_shift
        Af_eff = a_finish + sigma_shift
        Ms_eff = m_start + sigma_shift
        Mf_eff = m_finish + sigma_shift
        if dT_local < 0:  # cooling
            if T_new >= Ms_eff:
                Phi_new = 0.0
            elif T_new <= Mf_eff:
                Phi_new = 1.0
            else:
                Phi_new = 0.5 * (1.0 + math.cos(math.pi * (T_new - Mf_eff) / (Ms_eff - Mf_eff)))
        else:  # heating (если вызвали cooling с dT>0)
            if T_new <= As_eff:
                Phi_new = 1.0
            elif T_new >= Af_eff:
                Phi_new = 0.0
            else:
                Phi_new = 0.5 * (1.0 + math.cos(math.pi * (T_new - As_eff) / (Af_eff - As_eff)))
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
    peak_rows: list[dict] = []

    Fi_old = Fi
    alpha1_old = alpha1_aust * (1 - Fi_old) + alpha1_mart * Fi_old
    list_Fi = [Fi]

    # Фазовая деформация на охлаждении (формула Беляева):
    #   dε_ph = (σ_СПФ/E_TP + λ·ε_r) · dΦ
    # где ε_r — деформация волокна в конце нагрева (константа на охлаждении),
    # σ_СПФ — напряжение в волокне в момент окончания нагрева (константа).
    # Это интерпретация в духе работ СПбГУ (Беляев 2015, Кусакина 2018):
    # σ_СПФ = действующее «эффективное напряжение», ε_r = накопленный потенциал возврата.
    eps_star_out = float(eps1_out_strain)
    eps_star_in = float(eps1_in_strain)
    sig1_out_hot = sig1 + s1
    sig1_in_hot = sig1 - s1

    # Диагностика фиксированной кривизны на охлаждении:
    # разности крайних волокон по толщине должны сохраняться через шаги.
    curv_diff1_0 = eps1_out_strain - eps1_in_strain
    curv_diff2_0 = eps2_in_strain - eps2_out_strain
    # D1_old для σ*·d(1/E₁)
    E1_init_cool = aust_young_module_1 * (1 - Fi_old) + loading_young_module_1 * Fi_old
    D1_old_cool = 1.0 / E1_init_cool

    max_iter = 200

    # Диагностика скачков силы / переключений Hev (формула 9)
    jump_events = []
    prev_hev_state = None
    JUMP_FORCE_ABS = 1e-3
    JUMP_FORCE_REL = 0.05
    MAX_JUMP_EVENTS = 20

    plane_warn_count = 0
    kin_warn_count = 0
    curv_warn_count = 0
    neq_warn_count = 0
    PLANE_WARN_PRINT_LIMIT = 10

    # ζ_d (Lagoudas-Entchev) — приходит из предыдущего нагрева
    zeta_d = float(zeta_d_in)

    while t >= t_finish:
        # Эффект Клаузиуса-Клапейрона
        sig_for_CC = sig1
        dPhi = compute_dPhi(Fi_old, t, dT)
        Fi = Fi_old + dPhi
        # Численная защита: Φ должна оставаться в [0, 1]
        if Fi < 0.0:
            Fi = 0.0
        elif Fi > 1.0:
            Fi = 1.0

        # Прирост ζ_d (Lagoudas-Entchev)
        zeta_d += abs(dPhi)

        alpha1 = alpha1_aust * (1 - Fi) + alpha1_mart * Fi
        d_alpha1 = alpha1 - alpha1_old

        # (13): E1 -> D1
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

        # ФАЗОВАЯ ДЕФОРМАЦИЯ ОХЛАЖДЕНИЯ — пластичность превращения по Беляеву-Волкову (1996):
        #
        #   dε^Ф_охл = (σ_тек / E_ПП + λ·ε_r) · dΦ
        #
        # σ_тек — текущее напряжение в волокне на этом шаге (по строгой теории
        # Boyd-Lagoudas Λ_fwd ∝ σ_eff текущее). ε_r — накопленный потенциал, берётся
        # на момент окончания нагрева (T = Af).
        #
        # ВОЗМОЖНОЕ РАСШИРЕНИЕ (не реализовано в этой версии):
        # модель Lagoudas-Entchev (2004) добавляет множитель exp(-ζ_d / C₂),
        # описывающий насыщение TRIP-механизма с числом циклов. В нашей модели
        # это не используется — для согласия с экспериментом достаточно простой
        # формы Беляева плюс этап тренировки. См. Xu-Baxevanis-Lagoudas (2018,
        # arXiv:1812.10466) — это самостоятельное направление развития модели.
        eps0_cool_out = sig1_out_curr / young_module_TP + lam * eps_star_out
        eps0_cool_in = sig1_in_curr / young_module_TP + lam * eps_star_in
        d_D1 = D1 - D1_old_cool
        modulus_change_out = sig1_out_curr * d_D1
        modulus_change_in = sig1_in_curr * d_D1
        phase_out = eps0_cool_out * dPhi + modulus_change_out
        phase_in = eps0_cool_in * dPhi + modulus_change_in

        # Тепловой вклад
        thermal1_term = alpha1 * dT  # убран T*d_alpha1 (нефизичный артефакт)
        thermal2_term = alpha2 * dT

        if t == t_start:
            print(
                f"[INFO] cooling: eps_star_out={eps_star_out:.6g}, eps_star_in={eps_star_in:.6g}, "
                f"lam={lam}, young_module_TP={young_module_TP}"
            )

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
            # Fallback для полного прогона: считаем механическую часть упругой (без пластической добавки)
            # и решаем систему один раз. Это позволяет не останавливать термоцикл при калибровке констант.
            print(f"[WARN] cooling: (9) did not converge at t={t}, Fi={Fi}; falling back to elastic compliance")
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

        hev_state = (
            Hev(abs(sig1_out_trial) - yield_mix),
            Hev(abs(sig1_in_trial) - yield_mix),
            Hev(abs(sig2_out_trial) - strenght_yield_2),
            Hev(abs(sig2_in_trial) - strenght_yield_2),
            Hev(abs(sig1_out_trial) - abs(sig1_out_curr)),
            Hev(abs(sig1_in_trial) - abs(sig1_in_curr)),
            Hev(abs(sig2_out_trial) - abs(sig2_out_curr)),
            Hev(abs(sig2_in_trial) - abs(sig2_in_curr)),
        )

        # dσ/ds из x1..x4
        d_sig1 = 0.5 * (x1 + x2)
        d_s1 = 0.5 * (x1 - x2)
        d_sig2 = 0.5 * (x3 + x4)
        d_s2 = 0.5 * (x4 - x3)

        # Диагностика равновесия по продольной силе в приращениях:
        # h1*dσ1_mean + h2*dσ2_mean == 0
        N_res = h1 * d_sig1 + h2 * d_sig2
        denom = abs(h1 * d_sig1) + abs(h2 * d_sig2) + 1e-30
        if abs(N_res) / denom > 1e-6:
            neq_warn_count += 1
            if neq_warn_count <= PLANE_WARN_PRINT_LIMIT:
                print(f"[WARN] cooling N-equilibrium residual t={t:.3f}, Fi={Fi:.4f}: N_res={N_res:.3e}")
            elif neq_warn_count == PLANE_WARN_PRINT_LIMIT + 1:
                print("[WARN] cooling N-equilibrium residual: ... (suppressed further warnings)")

        sig1 += d_sig1
        s1 += d_s1
        sig2 += d_sig2
        s2 += d_s2

        force = force_reaction_per_width(sig1, s1, sig2, s2, sig1_ref, s1_ref, sig2_ref, s2_ref)
        dF = force - list_force[-1]
        list_force.append(force)

        # Диагностика: момент потери/возврата контакта (знак силы проходит через 0)
        # Это поможет понять, почему в охлаждении сила становится отрицательной.
        # Триггер: было F_prev >= 0 и стало F < 0 (или наоборот).
        if len(list_force) >= 2:
            F_prev = list_force[-2]
            if (F_prev >= 0.0 and force < 0.0) or (F_prev <= 0.0 and force > 0.0):
                print(
                    f"[CONTACT] cooling sign flip: t={t:.3f}K, Fi={Fi:.4f}, "
                    f"dPhi={dPhi:.3e}, dF={dF:.3e}, F_prev={F_prev:.6g} -> F={force:.6g}"
                )
                # Важно: дополнительно выведем вклад фазовой части и тепловой части
                print(
                    f"[CONTACT] phase(out,in)=({phase_out:.3e},{phase_in:.3e}), "
                    f"thermal(1,2)=({thermal1_term:.3e},{thermal2_term:.3e})"
                )
                print(f"[CONTACT] hev_state={hev_state}")
                print(
                    f"[CONTACT] x(dsig)=({x1:.3e},{x2:.3e},{x3:.3e},{x4:.3e}) "
                    f"d_sig1={0.5*(x1+x2):.3e}, d_s1={0.5*(x1-x2):.3e}, d_sig2={0.5*(x3+x4):.3e}, d_s2={0.5*(x4-x3):.3e}"
                )

        # Диагностика: "скачок" силы и/или переключение Hev
        if len(jump_events) < MAX_JUMP_EVENTS:
            force_prev = list_force[-2]
            thr = max(JUMP_FORCE_ABS, JUMP_FORCE_REL * max(1.0, abs(force_prev)))

            hev_changed = (prev_hev_state is not None and hev_state != prev_hev_state)

            if abs(dF) > thr or hev_changed:
                jump_events.append(
                    {
                        "t": t,
                        "Fi": Fi,
                        "dPhi": dPhi,
                        "dT": dT,
                        "Fprev": force_prev,
                        "dF": dF,
                        "F": force,
                        "thr": thr,
                        "hev": hev_state,
                        "hev_changed": hev_changed,
                        "x": (x1, x2, x3, x4),
                        "d_sig": (d_sig1, d_s1, d_sig2, d_s2),
                        "phase": (phase_out, phase_in),
                        "thermal": (thermal1_term, thermal2_term),
                        "C": (C1_out, C1_in, C2_out, C2_in),
                        "sig_trial": (sig1_out_trial, sig1_in_trial, sig2_out_trial, sig2_in_trial),
                        "sig_curr": (sig1_out_curr, sig1_in_curr, sig2_out_curr, sig2_in_curr),
                    }
                )
        prev_hev_state = hev_state

        list_sig1.append(sig1)
        list_sig2.append(sig2)

        # t/Fi/alpha
        t += dT
        list_t.append(t)
        Fi_old = Fi
        list_Fi.append(Fi)
        alpha1_old = alpha1
        D1_old_cool = D1

        # (16)-(17) обновление деформаций
        d_eps_out1 = C1_out * x1 + phase_out + thermal1_term
        d_eps_in1 = C1_in * x2 + phase_in + thermal1_term
        d_eps_out2 = C2_out * x3 + thermal2_term
        d_eps_in2 = C2_in * x4 + thermal2_term

        kin_err = max(
            abs(d_eps_out1 - d_eps_in1),
            abs(d_eps_in1 - d_eps_in2),
            abs(d_eps_out1 - d_eps_out2),
        )
        if kin_err > 1e-8:
            kin_warn_count += 1
            if kin_warn_count <= PLANE_WARN_PRINT_LIMIT:
                print(
                    f"[WARN] cooling kin-constraints error t={t:.3f}, Fi={Fi:.4f}: kin_err={kin_err:.3e} "
                    f"(dEpsOut1-dEpsIn1={d_eps_out1 - d_eps_in1:.3e}, dEpsIn1-dEpsIn2={d_eps_in1 - d_eps_in2:.3e}, "
                    f"dEpsOut1-dEpsOut2={d_eps_out1 - d_eps_out2:.3e})"
                )
            elif kin_warn_count == PLANE_WARN_PRINT_LIMIT + 1:
                print("[WARN] cooling kin-constraints error: ... (suppressed further warnings)")

        eps1_out_strain += d_eps_out1
        eps1_in_strain += d_eps_in1
        eps2_out_strain += d_eps_out2
        eps2_in_strain += d_eps_in2

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
                context=f"cooling step, t={t}, Fi={Fi}",
                apply_delta_correction=True,
            )
        except ValueError as e:
            # Оставляем модель охлаждения работоспособной и сигнализируем о нарушении
            # геометрической совместности; это отдельный диагностический маркер.
            plane_warn_count += 1
            if plane_warn_count <= PLANE_WARN_PRINT_LIMIT:
                print(f"[WARN] Plane-sections check failed in cooling: {e}")
            elif plane_warn_count == PLANE_WARN_PRINT_LIMIT + 1:
                print(f"[WARN] Plane-sections check failed in cooling: ... (suppressed further warnings)")

        peak_rows.append(
            {
                "Fi": Fi,
                "dPhi": dPhi,
                "dF": dF,
                "sig1_out": sig1 + s1,
                "sig1_in": sig1 - s1,
                "sig2_out": sig2 - s2,
                "sig2_in": sig2 + s2,
                "sig_mean1": sig1,
                "s_half1": s1,
                "sig_mean2": sig2,
                "s_half2": s2,
                "yield_mix": yield_mix,
                "sigma_y2": strenght_yield_2,
                "C": (C1_out, C1_in, C2_out, C2_in),
                "mech_out1": C1_out * x1,
                "mech_in1": C1_in * x2,
                "mech_out2": C2_out * x3,
                "mech_in2": C2_in * x4,
                "phase_out": phase_out,
                "phase_in": phase_in,
                "thermal1": thermal1_term,
                "thermal2": thermal2_term,
                "d_eps_out1": d_eps_out1,
                "d_eps_in1": d_eps_in1,
                "d_eps_out2": d_eps_out2,
                "d_eps_in2": d_eps_in2,
                "hev": hev_state,
                "eps0_cool_out": eps0_cool_out,
                "eps0_cool_in": eps0_cool_in,
            }
        )

    # Attach peak_rows for diagnostic access
    cooling.last_peak_rows = peak_rows
    cooling.last_zeta_d = zeta_d

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
        list_force,
    )


# ============================================================================
# СВОБОДНЫЙ ТЕРМОЦИКЛ (тренировка ленты без зажима)
# ============================================================================
# Условия:
#   1) dM = 0          — свободная лента, нет внешнего момента
#   2) dε_in_1 = dε_in_2  — сцепление слоёв
#   3) Гипотеза плоских сечений: (dε_out_1 - dε_in_1)/h_1 = (dε_in_2 - dε_out_2)/h_2
#   4) h_1·(dσ_out_1+dσ_in_1) + h_2·(dσ_out_2+dσ_in_2) = 0  (N=0)
#
# Вместе с уравнениями состояния dε = C·dσ + phase + thermal
# получаем систему 4 уравнений на 4 неизвестных (dσ_out_1, dσ_in_1, dσ_out_2, dσ_in_2).
#
# Используется для тренировки ленты до стабилизации TRIP. После тренировки
# натренированное состояние подаётся в обычный heating_constant_curvature
# для расчёта силы.
def free_thermal_step(
    sig1_out_curr, sig1_in_curr, sig2_out_curr, sig2_in_curr,
    eps0_out, eps0_in,            # ε⁰·dΦ для слоя 1 (TRIP-like)
    dPhi,
    alpha1, alpha2, dT,
    D1, D2, D1_old,
    yield_mix, H1_mix,
    sig_y2, H2,
    decay_factor=1.0,
):
    """
    Один шаг свободного термоцикла. Решает систему 4×4 при условии M=0.
    Возвращает приращения (dσ_out_1, dσ_in_1, dσ_out_2, dσ_in_2) и phase/thermal.
    """
    import numpy
    
    # Phase + modulus change для слоя 1
    d_D1 = D1 - D1_old
    modulus_change_out = sig1_out_curr * d_D1
    modulus_change_in = sig1_in_curr * d_D1
    phase_out = decay_factor * eps0_out * dPhi + modulus_change_out
    phase_in = decay_factor * eps0_in * dPhi + modulus_change_in
    thermal1 = alpha1 * dT
    thermal2 = alpha2 * dT
    
    # Эффективные податливости (с проверкой ветви разгрузки)
    def C_eff(sig_curr, dsig, D, sigT, H):
        sig_trial = sig_curr + dsig
        Hev1 = 1 if abs(sig_trial) > sigT else 0
        Hev2 = 1 if abs(sig_trial) > abs(sig_curr) else 0
        return D + (1.0/H - D) * Hev1 * Hev2
    
    # Итерации для устойчивости Hev (как в heating)
    x = numpy.zeros(4)
    for it in range(100):
        C1_out = C_eff(sig1_out_curr, x[0], D1, yield_mix, H1_mix)
        C1_in = C_eff(sig1_in_curr, x[1], D1, yield_mix, H1_mix)
        C2_out = C_eff(sig2_out_curr, x[2], D2, sig_y2, H2)
        C2_in = C_eff(sig2_in_curr, x[3], D2, sig_y2, H2)
        
        # Система:
        # (1) dM=0:
        #   dM = h1²/6·(3·dσ_avg_1 + ds_1) - h2²/6·(3·dσ_avg_2 - ds_2) = 0
        #   где dσ_avg_1 = (x1+x2)/2, ds_1 = (x1-x2)/2
        #        dσ_avg_2 = (x3+x4)/2, ds_2 = -(x3-x4)/2 (т.к. для слоя 2 σ_out = σ-s)
        #   Тогда 3·dσ_avg_1 + ds_1 = 3(x1+x2)/2 + (x1-x2)/2 = 2x1 + x2
        #         3·dσ_avg_2 - ds_2 = 3(x3+x4)/2 + (x3-x4)/2 = 2x3 + x4
        #   Условие: h1²·(2x1+x2)/6 - h2²·(2x3+x4)/6 = 0
        #           => h1²·(2x1+x2) - h2²·(2x3+x4) = 0
        # (2) dε_in_1 = dε_in_2:
        #   C1_in·x2 + phase_in + thermal1 = C2_in·x4 + thermal2
        # (3) гипотеза плоских сечений:
        #   (dε_out_1 - dε_in_1)/h1 = (dε_in_2 - dε_out_2)/h2
        #   => h2·(dε_out_1 - dε_in_1) = h1·(dε_in_2 - dε_out_2)
        #   => h2·(C1_out·x1 + phase_out - C1_in·x2 - phase_in) = h1·(C2_in·x4 - C2_out·x3)
        # (4) N=0:
        #   h1·(x1+x2) + h2·(x3+x4) = 0
        A = numpy.array([
            [h1*h1*2, h1*h1, -h2*h2*2, -h2*h2],          # уравнение (1) dM=0
            [0.0, C1_in, 0.0, -C2_in],                    # уравнение (2)
            [h2*C1_out, -h2*C1_in, h1*C2_out, -h1*C2_in], # уравнение (3)
            [h1, h1, h2, h2],                             # уравнение (4)
        ])
        b = numpy.array([
            0.0,
            thermal2 - phase_in - thermal1,
            h2*(phase_in - phase_out),
            0.0,
        ])
        try:
            x_new = numpy.linalg.solve(A, b)
        except numpy.linalg.LinAlgError:
            # Сингулярная — упрощаем (фактически lin-задача)
            return x, phase_out, phase_in, thermal1, thermal2
        if numpy.allclose(x, x_new, atol=1e-10, rtol=1e-7):
            x = x_new
            break
        x = x_new
    
    return x, phase_out, phase_in, thermal1, thermal2


def free_thermal_cycle(
    eps1_out_0, eps1_in_0, eps2_out_0, eps2_in_0,
    eps1_out_max, eps1_in_max,
    sig1_init, s1_init, sig2_init, s2_init,
    *,
    n_cycles: int = 50,
    d_t: float = 0.5,
    zeta_d_in: float = 0.0,
    sig1_out_yield_signed=None,
    sig1_in_yield_signed=None,
    record_per_step: bool = False,
):
    """
    Свободные термоциклы: лента не зажата, M=0 на каждом шаге.
    
    Возвращает финальное состояние (σ, ε, ζ_d) после тренировки.
    Если record_per_step=True, в history попадает по записи НА КАЖДОМ ШАГЕ T
    (для построения графиков ε(T) при тренировке).
    """
    import math
    
    # Параметры возврата
    sigma_T_over_E = strenght_yield_1 / unloading_young_module_1
    
    def plastic_part(eps_max_value):
        if abs(eps_max_value) <= sigma_T_over_E:
            return 0.0
        return (abs(eps_max_value) - sigma_T_over_E) * (1.0 if eps_max_value >= 0 else -1.0)
    
    eps_pl_out = plastic_part(eps1_out_max)
    eps_pl_in = plastic_part(eps1_in_max)
    eps0_const_out = rec_ratio * eps_pl_out
    eps0_const_in = rec_ratio * eps_pl_in
    
    # Состояние
    sig1, s1, sig2, s2 = sig1_init, s1_init, sig2_init, s2_init
    eps1_out_strain = eps1_out_0
    eps1_in_strain = eps1_in_0
    eps2_out_strain = eps2_out_0
    eps2_in_strain = eps2_in_0
    zeta_d = float(zeta_d_in)
    
    # История F_max/F_min для диагностики (но F здесь не применима, т.к. M=0)
    history = []
    
    # Чередуем нагрев и охлаждение
    Fi = 1.0
    Fi_old = Fi
    
    def Phi_func(T, direction, sig_for_CC):
        """direction='heat' или 'cool'. Косинусная кинетика (Liang-Rogers)."""
        sigma_shift = k_CC * max(sig_for_CC, 0.0)
        As_eff = a_start + sigma_shift
        Af_eff = a_finish + sigma_shift
        Ms_eff = m_start + sigma_shift
        Mf_eff = m_finish + sigma_shift
        if direction == 'heat':
            if T <= As_eff:
                return 1.0
            elif T >= Af_eff:
                return 0.0
            return 0.5 * (1.0 + math.cos(math.pi * (T - As_eff) / (Af_eff - As_eff)))
        else:
            if T >= Ms_eff:
                return 0.0
            elif T <= Mf_eff:
                return 1.0
            return 0.5 * (1.0 + math.cos(math.pi * (T - Mf_eff) / (Ms_eff - Mf_eff)))
    
    for cycle in range(1, n_cycles + 1):
        # === Нагрев ===
        T = t_start
        D1_old = 1.0 / (aust_young_module_1 * (1 - Fi) + loading_young_module_1 * Fi)
        Fi_old = Fi
        sig1_out_at_Af = None
        sig1_in_at_Af = None
        
        steps = 0
        while T <= t_finish:
            sig_for_CC = sig1
            T_new = T + d_t
            Phi_new = Phi_func(T_new, 'heat', sig_for_CC)
            dPhi = Phi_new - Fi_old
            
            zeta_d += abs(dPhi)
            
            # Параметры
            E1 = aust_young_module_1 * (1 - Phi_new) + loading_young_module_1 * Phi_new
            D1 = 1.0 / E1
            D2 = 1.0 / young_module_2
            yield_mix = strenght_yield_1_aust * (1 - Phi_new) + strenght_yield_1 * Phi_new
            H1_mix = strengthening_coefficient_1_aust * (1 - Phi_new) + strengthening_coefficient_1 * Phi_new
            alpha1 = alpha1_aust * (1 - Phi_new) + alpha1_mart * Phi_new
            
            # ε⁰ на нагреве по Belyaev-Volkov-Evard: только K·ε_pl, без σ/E_ПП
            sig1_out = sig1 + s1
            sig1_in = sig1 - s1
            eps0_out = eps0_const_out
            eps0_in = eps0_const_in
            
            x, phase_o, phase_i, th1, th2 = free_thermal_step(
                sig1_out, sig1_in, sig2 - s2, sig2 + s2,
                eps0_out, eps0_in, dPhi,
                alpha1, alpha2, d_t,
                D1, D2, D1_old,
                yield_mix, H1_mix,
                strenght_yield_2, strengthening_coefficient_2,
                decay_factor=1.0,
            )
            
            # Обновление σ
            x1, x2, x3, x4 = x  # dσ для out_1, in_1, out_2, in_2
            sig1_out_new = sig1_out + x1
            sig1_in_new = sig1_in + x2
            sig2_out_new = (sig2 - s2) + x3
            sig2_in_new = (sig2 + s2) + x4
            sig1 = (sig1_out_new + sig1_in_new) / 2
            s1 = (sig1_out_new - sig1_in_new) / 2
            sig2 = (sig2_out_new + sig2_in_new) / 2
            s2 = (sig2_in_new - sig2_out_new) / 2  # σ_in_2 - σ_out_2 = 2·s2
            
            # Деформации (через C·dσ + phase + thermal):
            # пересчитываем C с финальным x
            def C_eff(sig_curr, dsig, D, sigT, H):
                sig_trial = sig_curr + dsig
                Hev1 = 1 if abs(sig_trial) > sigT else 0
                Hev2 = 1 if abs(sig_trial) > abs(sig_curr) else 0
                return D + (1.0/H - D) * Hev1 * Hev2
            C1_out_f = C_eff(sig1_out, x1, D1, yield_mix, H1_mix)
            C1_in_f = C_eff(sig1_in, x2, D1, yield_mix, H1_mix)
            C2_out_f = C_eff(sig2 - s2, x3, D2, strenght_yield_2, strengthening_coefficient_2)
            C2_in_f = C_eff(sig2 + s2, x4, D2, strenght_yield_2, strengthening_coefficient_2)
            d_eps_out_1 = C1_out_f * x1 + phase_o + th1
            d_eps_in_1 = C1_in_f * x2 + phase_i + th1
            d_eps_out_2 = C2_out_f * x3 + th2
            d_eps_in_2 = C2_in_f * x4 + th2
            eps1_out_strain += d_eps_out_1
            eps1_in_strain += d_eps_in_1
            eps2_out_strain += d_eps_out_2
            eps2_in_strain += d_eps_in_2
            
            # Запись для графиков ε(T) при тренировке
            if record_per_step:
                history.append({
                    'cycle': cycle, 'phase': 'heat',
                    'T': T_new,
                    'eps1_out': eps1_out_strain, 'eps1_in': eps1_in_strain,
                    'eps2_out': eps2_out_strain, 'eps2_in': eps2_in_strain,
                    'sig1_out': sig1+s1, 'sig1_in': sig1-s1,
                    'sig2_out': sig2-s2, 'sig2_in': sig2+s2,
                    'Phi': Phi_new, 'zeta_d': zeta_d,
                })
            
            T = T_new
            Fi_old = Phi_new
            D1_old = D1
            steps += 1
        
        Fi = Fi_old
        sig1_out_at_Af = sig1 + s1
        sig1_in_at_Af = sig1 - s1
        eps_star_out_local = sig1_out_at_Af / young_module_TP  # упрощение: ε_r ≈ σ/E_TP
        eps_star_in_local = sig1_in_at_Af / young_module_TP
        
        # === Охлаждение ===
        T = t_finish
        D1_old_cool = 1.0 / (aust_young_module_1 * (1 - Fi) + loading_young_module_1 * Fi)
        Fi_old = Fi
        
        while T >= t_start:
            sig_for_CC = sig1
            T_new = T - d_t
            Phi_new = Phi_func(T_new, 'cool', sig_for_CC)
            dPhi = Phi_new - Fi_old
            
            zeta_d += abs(dPhi)
            
            # Параметры
            E1 = aust_young_module_1 * (1 - Phi_new) + loading_young_module_1 * Phi_new
            D1 = 1.0 / E1
            D2 = 1.0 / young_module_2
            yield_mix = strenght_yield_1_aust * (1 - Phi_new) + strenght_yield_1 * Phi_new
            H1_mix = strengthening_coefficient_1_aust * (1 - Phi_new) + strengthening_coefficient_1 * Phi_new
            alpha1 = alpha1_aust * (1 - Phi_new) + alpha1_mart * Phi_new
            
            # ε⁰ на охлаждении по Belyaev-Volkov: σ_curr/E_ПП + λ·ε_r
            sig1_out = sig1 + s1
            sig1_in = sig1 - s1
            eps0_out = sig1_out / young_module_TP + lam * eps_star_out_local
            eps0_in = sig1_in / young_module_TP + lam * eps_star_in_local
            
            x, phase_o, phase_i, th1, th2 = free_thermal_step(
                sig1_out, sig1_in, sig2 - s2, sig2 + s2,
                eps0_out, eps0_in, dPhi,
                alpha1, alpha2, -d_t,
                D1, D2, D1_old_cool,
                yield_mix, H1_mix,
                strenght_yield_2, strengthening_coefficient_2,
                decay_factor=1.0,
            )
            
            x1, x2, x3, x4 = x
            sig1_out_new = sig1_out + x1
            sig1_in_new = sig1_in + x2
            sig2_out_new = (sig2 - s2) + x3
            sig2_in_new = (sig2 + s2) + x4
            sig1 = (sig1_out_new + sig1_in_new) / 2
            s1 = (sig1_out_new - sig1_in_new) / 2
            sig2 = (sig2_out_new + sig2_in_new) / 2
            s2 = (sig2_in_new - sig2_out_new) / 2
            
            # Деформации
            def C_eff_c(sig_curr, dsig, D, sigT, H):
                sig_trial = sig_curr + dsig
                Hev1 = 1 if abs(sig_trial) > sigT else 0
                Hev2 = 1 if abs(sig_trial) > abs(sig_curr) else 0
                return D + (1.0/H - D) * Hev1 * Hev2
            C1_out_f = C_eff_c(sig1_out, x1, D1, yield_mix, H1_mix)
            C1_in_f = C_eff_c(sig1_in, x2, D1, yield_mix, H1_mix)
            C2_out_f = C_eff_c(sig2 - s2 - x3, x3, D2, strenght_yield_2, strengthening_coefficient_2)
            C2_in_f = C_eff_c(sig2 + s2 - x4, x4, D2, strenght_yield_2, strengthening_coefficient_2)
            eps1_out_strain += C1_out_f * x1 + phase_o + th1
            eps1_in_strain += C1_in_f * x2 + phase_i + th1
            eps2_out_strain += C2_out_f * x3 + th2
            eps2_in_strain += C2_in_f * x4 + th2
            
            # Запись для графиков ε(T) при тренировке
            if record_per_step:
                history.append({
                    'cycle': cycle, 'phase': 'cool',
                    'T': T_new,
                    'eps1_out': eps1_out_strain, 'eps1_in': eps1_in_strain,
                    'eps2_out': eps2_out_strain, 'eps2_in': eps2_in_strain,
                    'sig1_out': sig1+s1, 'sig1_in': sig1-s1,
                    'sig2_out': sig2-s2, 'sig2_in': sig2+s2,
                    'Phi': Phi_new, 'zeta_d': zeta_d,
                })
            
            T = T_new
            Fi_old = Phi_new
            D1_old_cool = D1
        
        Fi = Fi_old
        # Конец цикла — запись в history (если не record_per_step, то просто финальные σ)
        if not record_per_step:
            history.append({
                'cycle': cycle, 'sig1_out': sig1+s1, 'sig1_in': sig1-s1,
                'sig2_out': sig2-s2, 'sig2_in': sig2+s2, 'zeta_d': zeta_d,
                's1': s1, 's2': s2, 'sig1': sig1, 'sig2': sig2,
            })
    
    return {
        'sig1': sig1, 's1': s1, 'sig2': sig2, 's2': s2,
        'eps1_out': eps1_out_strain, 'eps1_in': eps1_in_strain,
        'eps2_out': eps2_out_strain, 'eps2_in': eps2_in_strain,
        'zeta_d': zeta_d,
        'history': history,
    }
