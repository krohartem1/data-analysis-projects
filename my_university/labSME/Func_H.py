import numpy
from typing import Optional
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

# Разгрузка до σ₁_out≈0: внешнее волокно слоя 1 перестаёт быть растянутым (переход к сжатию).
# Абсолютная и относительная (к σ_y слоя 1) толщина по |σ|.
SIG1_OUT_ZERO_TOL_ABS = 5e3
SIG1_OUT_ZERO_TOL_REL = 1e-5

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


def Hev2(a: float, b: float) -> int:
    """
    Двухаргументный порог, как в `bimet_stopka.cpp`: Hev(a,b) = 1 если a > b, иначе 0.
    Используется в кинетике dFi (Pt, границы по Fi).
    """
    return 1 if a > b else 0


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
    Сила на единицу ширины: F/a = 3·ΔM/(2·L).
    ΔM = (h1²(3Δσ₁+Δs₁) - h2²(3Δσ₂-Δs₂))/6  — формула (4) Кусакиной.
    Коэффициент 3/2 — реакция опоры консоли с равномерным моментом
    при заблокированном прогибе на конце (суперпозиция Эйлера-Бернулли).
    """
    delta_M = (h1 * h1 * (3 * (sig1 - sig1_ref) + (s1 - s1_ref))
               - h2 * h2 * (3 * (sig2 - sig2_ref) - (s2 - s2_ref))) / 6.0
    return 1.5 * delta_M / part_len


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
    save_path: Optional[str] = None,
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
def update_constant(parameter_name, new_value):
    with open(r"D:\GitHub_projects\my_university\labSME\const.py", "r") as f:
        lines = f.readlines()

    found = False
    for i in range(len(lines)):
        # Разбиваем строку на имя параметра и значение
        if "=" in lines[i]:
            key_part, value_part = lines[i].split("=", 1)
            current_param = key_part.strip()

            if current_param == parameter_name:
                # Сохраняем исходные пробелы слева от "=", обновляем значение справа
                lines[i] = f"{key_part} = {new_value}\n"
                found = True
                break

    # Если параметр не найден, добавляем в конец
    if not found:
        lines.append(f"{parameter_name} = {new_value}\n")

    with open("D:/GitHub_projects/my_university/labSME/venv/Include/const.py", "w") as f:
        f.writelines(lines)


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
    stop_mode: str = "moment_zero",
    max_unload_steps: int = 500000,
    moment_check_strict: bool = False,
):
    """
    Разгрузка изгибающим моментом (уменьшение M с шагом d_M).

    stop_mode:
      - \"moment_zero\": снимаем внешний момент до M≈0 (как раньше).
      - \"curvature_zero\": останавливаемся, когда «прямая пластинка» по геометрии:
        одинаковый масштаб длин всех крайних волокон (см. is_curvature_zero_by_straightness).
      - \"sig1_out_zero\": останавливаемся, когда напряжение во внешнем волокне слоя 1
        σ₁_out = σ₁+s₁ проходит через ноль (растяжение→сжатие). Это не то же самое, что ε₁_out=0:
        при остаточной пластичности может быть σ≈0 при ε≠0. Параметр delta (укорочение к барабану)
        здесь не используется — он про геометрию стыка, а не про знак σ на волокне.

    В конце: сверка оставшегося счётчика M с моментом по полной формуле из напряжений по формуле (4)
    (`bending_moment_per_width_from_mean_half`, см. диплом Кусакиной). При расхождении
    ищите ошибку в разгрузке/обозначениях; при moment_check_strict=True — ValueError.
    """
    d_M = 1e-6   # приращение момента
    M = bending_moment
    sig1_out_zero_tol = SIG1_OUT_ZERO_TOL_ABS + SIG1_OUT_ZERO_TOL_REL * strenght_yield_1

    # Параметры напряжений с предыдущего шага
    sig1, s1, sig2, s2 = sig1_out / 2, sig1_out / 2, 0, 0

    list_sig1o, list_sig2o, list_sig1in, list_sig2in = [sig1_out], [sig2_out], [sig1_in], [sig2_in]

    list_e1o, list_e2o, list_e1i, list_e2i  = [eps1_out], [eps2_out], [eps1_in], [eps2_in]

    len_o1 = (arc_length / rad) * (h1 + h2 + rad) - delta
    len_o2 = (arc_length / rad) * (rad)
    len_in = (arc_length / rad) * (rad + h1)
    def is_curvature_zero_by_straightness(
        eps1_out_val: float,
        eps1_in_val: float,
        eps2_out_val: float,
        eps2_in_val: float,
    ) -> bool:
        # Проверка прямизны (нулевой кривизны) через равенство относительных
        # удлинений всех крайних волокон.
        L1_out0 = len_o1 + delta
        L1_out = len_o1 + len_o1 * eps1_out_val
        L1_in0 = len_in
        L1_in = len_in + len_in * eps1_in_val

        L2_out0 = len_o2
        L2_out = len_o2 + len_o2 * eps2_out_val

        L2_in0 = (arc_length / rad) * (rad + h2)
        L2_in = L2_in0 + L2_in0 * eps2_in_val

        s_out1 = L1_out / L1_out0
        s_in1 = L1_in / L1_in0
        s_out2 = L2_out / L2_out0
        s_in2 = L2_in / L2_in0

        scales = [s_out1, s_in1, s_out2, s_in2]
        s_min = min(scales)
        s_max = max(scales)
        s_mean = sum(scales) / len(scales)
        allowed = STRAIGHT_SCALE_TOL_ABS + STRAIGHT_SCALE_TOL_REL * abs(s_mean)
        return (s_max - s_min) <= allowed

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

        # Внешнее волокно слоя 1: растяжение (σ₁_out>0) → сжатие (σ₁_out<0); нейтральное волокно — σ₁_out≈0.
        # Проверка после полного шага (списки уже обновлены).
        if stop_mode == "sig1_out_zero":
            if sig1_out_old > 0.0 and sig1_out <= 0.0:
                break
            if abs(sig1_out) <= sig1_out_zero_tol:
                break

        # Вариант разгрузки: остановка при достижении нулевой кривизны
        # (прямизны/одинаковых относительных удлинений крайних волокон),
        # даже если остаточный момент ещё не полностью “вынесен” в ноль.
        if stop_mode == "curvature_zero":
            if is_curvature_zero_by_straightness(eps1_out, eps1_in, eps2_out, eps2_in):
                break

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
    # При stop_mode=sig1_out_zero критерий «прямой по длинам» может не выполняться — у плоских
    # сечений слои не обязаны иметь одинаковую длину при σ₁_out≈0.
    if (s_max - s_min) > allowed:
        msg = (
            "Пластинка не стала прямой после unloading (проверка по длинам): "
            f"scales={scales}, s_min={s_min}, s_max={s_max}, allowed={allowed}. "
            f"eps1_out={eps1_out}, eps1_in={eps1_in}, eps2_in={eps2_in}, eps2_out={eps2_out}"
        )
        if stop_mode == "sig1_out_zero":
            print(f"[INFO] unloading (sig1_out_zero): {msg}")
        else:
            raise ValueError(msg)

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
        f"unloading({stop_mode})",
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


# Нагрев пластинки и рассчет df
# eps1_out_0, eps1_in_0 — деформации перед нагревом (после разгрузки), отчёт: ε0 — «начальная деформация»
def heating(
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
    # Старый вариант нагрева больше не используется: вся логика в `heating_constant_curvature()`.
    return heating_constant_curvature(
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
        d_t=d_t,
    )

    '''
    d_t = 0.5
    force = 0
    t = t_start
    D1_old = 1 / loading_young_module_1
    Fi_old = 1

    list_force = [0]
    list_t = [t_start]
    list_sig1 = [sig1]
    list_sig2 = [sig2]
    list_Fi = [1]

    alpha1_old = alpha1_mart

    D2 = 1 / young_module_2

    podat1_load_old = (1 / strengthening_coefficient_1) - (1 / loading_young_module_1)

    # Отчёт (12): dε^ph_h = K·ε0·dΦ; ε0 — деформация перед нагревом (после разгрузки), K = rec_ratio
    eps0_heat_out = rec_ratio * (eps1_out_0 - strenght_yield_1 / unloading_young_module_1)
    eps0_heat_in = rec_ratio * (eps1_in_0 - strenght_yield_1 / unloading_young_module_1)
    with open('modeling.txt', 'w', encoding='utf-8') as outfile:
        while t <= t_finish:

            d_Fi = -d_t / (m_start - m_finish) * Hev(1 - Fi_old) * Hev(m_start - Fi_old * (m_start - m_finish) - t) - d_t / (a_finish - a_start) * Hev(Fi_old) * Hev(t + Fi_old * (a_finish - a_start) - a_finish)
            Fi = Fi_old + d_Fi

            D1 = 1 / aust_young_module_1 * (1 - Fi) + 1 / loading_young_module_1 * Fi
            d_D1 = D1 - D1_old

            alpha1 = alpha1_aust * (1 - Fi) + alpha1_mart * Fi
            d_alpha1 = alpha1 - alpha1_old

            d_sig2 = (h1 / (h2 * D1)) * (sig1 * d_D1 + d_alpha1 * t + alpha1 * d_t + (eps0_heat_out + eps0_heat_in) * d_Fi / 2)
            d_sig1 = -(1 / D1) * (sig1 * d_D1 + d_alpha1 * t + alpha1 * d_t + (eps0_heat_out + eps0_heat_in) * d_Fi / 2)
            d_s1 = (1 / D1) * ((eps0_heat_in - eps0_heat_out) * d_Fi / 2 - podat1_load * d_D1)
            d_s2 = -d_sig2 - alpha2 * d_t / (D2 + podat2 * Hev(abs(sig2 + s2) - strenght_yield_2))

            if Hev(abs(d_sig2 + d_s2)) == 0:
                d_s2 = -d_sig2 - alpha2 * d_t / D2

            if d_sig2 != (-alpha2*d_t)*(1/(D2 + podat2 * Hev(abs(sig2 + s2) - strenght_yield_2) * Hev(abs(d_sig2 + d_s2))) + 1/(D2 + podat2 * Hev(abs(sig2 - s2) - strenght_yield_2) * Hev(abs(d_sig2 - d_s2)))):
                outfile.write(f"{(t-t_start)/d_t}, peredelivay, raznitsa = {d_sig2 - (-alpha2*d_t)*(1/(D2 + podat2 * Hev(abs(sig2 + s2) - strenght_yield_2) * Hev(abs(d_sig2 + d_s2))) + 1/(D2 + podat2 * Hev(abs(sig2 - s2) - strenght_yield_2) * Hev(abs(d_sig2 - d_s2))))} and d_sig2 = {d_sig2}\n")

            # Отчёт (18): dF = (h1²/(6L))·(3dσ1+ds1−3·(h2²/h1²)·dσ2+(h2²/h1²)·ds2). Минус — конвенция (реакция опоры).
            # Для «усилия, развиваемого лентой» по отчёту можно использовать -d_f (или force_sign = -1).
            d_f = -(h1 * h1 / (6 * part_len)) * (3 * d_sig1 + d_s1 - 3 * h2 * h2 * d_sig2 / (h1 * h1) + h2 * h2 * d_s2 / (h1 * h1))
            force += d_f
            list_force.append(force)

            sig2 += d_sig2
            list_sig2.append(sig2)
            sig1 += d_sig1
            list_sig1.append(sig1)
            s1 += d_s1
            s2 += d_s2
            alpha1_old = alpha1
            t += d_t
            list_t.append(t)
            D1_old = D1
            list_Fi.append(Fi)
            Fi_old = Fi

            if Fi <= 0 and d_Fi != 0:
                eps1_out_strain = (sig1 + s1) * D1 + Hev(sig1 + s1 - strenght_yield_1_aust) * (sig1 + s1 - strenght_yield_1_aust) * podat1_load
                eps1_in_strain = (sig1 - s1) * D1 + Hev(sig1 - s1 - strenght_yield_1_aust) * (sig1 - s1 - strenght_yield_1_aust) * podat1_load
                eps2_in_strain = (sig2 + s2) * D2 + Hev(sig2 + s2 - strenght_yield_2) * (sig2 + s2 - strenght_yield_2) * podat2
                eps2_out_strain = (sig2 - s2) * D2 + Hev(sig2 - s2 - strenght_yield_2) * (sig2 - s2 - strenght_yield_2) * podat2

        # while t <= t_finish:

        #     d_Fi = -d_t / (m_start - m_finish) * Hev(1 - Fi_old) * Hev(m_start - Fi_old * (m_start - m_finish) - t) - d_t / (a_finish - a_start) * Hev(Fi_old) * Hev(t + Fi_old * (a_finish - a_start) - a_finish)
        #     Fi = Fi_old + d_Fi

        #     D1 = 1 / aust_young_module_1 * (1 - Fi) + 1 / loading_young_module_1 * Fi
        #     d_D1 = D1 - D1_old

        #     #podat1_load =

        #     alpha1 = alpha1_aust * (1 - Fi) + alpha1_mart * Fi
        #     d_alpha1 = alpha1 - alpha1_old

        #     d_sig2 = (h1 / (h2 * D1)) * (sig1 * d_D1 + d_alpha1 * t + alpha1 * d_t + (eps0_heat_out + eps0_heat_in) * d_Fi / 2)
        #     d_sig1 = -(1 / D1) * (sig1 * d_D1 + d_alpha1 * t + alpha1 * d_t + (eps0_heat_out + eps0_heat_in) * d_Fi / 2)
        #     d_s1 = (1 / D1) * ((eps0_heat_in - eps0_heat_out) * d_Fi / 2 - podat1_load * d_D1)
        #     d_s2 = -d_sig2 - alpha2 * d_t / (D2 + podat2 * Hev(abs(sig2 + s2) - strenght_yield_2))

        #     if Hev(abs(d_sig2 + d_s2)) == 0:
        #         d_s2 = -d_sig2 - alpha2 * d_t / D2

        #     if d_sig2 != (-alpha2*d_t)*(1/(D2 + podat2 * Hev(abs(sig2 + s2) - strenght_yield_2) * Hev(abs(d_sig2 + d_s2))) + 1/(D2 + podat2 * Hev(abs(sig2 - s2) - strenght_yield_2) * Hev(abs(d_sig2 - d_s2)))):
        #         outfile.write(f"{(t-t_start)/d_t}, peredelivay, raznitsa = {d_sig2 - (-alpha2*d_t)*(1/(D2 + podat2 * Hev(abs(sig2 + s2) - strenght_yield_2) * Hev(abs(d_sig2 + d_s2))) + 1/(D2 + podat2 * Hev(abs(sig2 - s2) - strenght_yield_2) * Hev(abs(d_sig2 - d_s2))))} and d_sig2 = {d_sig2}\n")

        #     d_f = (h1 * h1 / (6 * part_len)) * (3 * d_sig1 + d_s1 - 3 * h2 * h2 * d_sig2 / (h1 * h1) + h2 * h2 * d_s2 / (h1 * h1))
        #     force += d_f
        #     list_force.append(force)

        #     sig2 += d_sig2
        #     list_sig2.append(sig2)
        #     sig1 += d_sig1
        #     list_sig1.append(sig1)
        #     s1 += d_s1
        #     s2 += d_s2
        #     alpha1_old = alpha1
        #     t += d_t
        #     list_t.append(t)
        #     D1_old = D1
        #     list_Fi.append(Fi)
        #     Fi_old = Fi

        #     if Fi <= 0 and d_Fi != 0:
        #         eps1_out_strain = (sig1 + s1) * D1 + Hev(sig1 + s1 - strenght_yield_1_aust) * (sig1 + s1 - strenght_yield_1_aust) * podat1_load
        #         eps1_in_strain = (sig1 - s1) * D1 + Hev(sig1 - s1 - strenght_yield_1_aust) * (sig1 - s1 - strenght_yield_1_aust) * podat1_load
        #         eps2_in_strain = (sig2 + s2) * D2 + Hev(sig2 + s2 - strenght_yield_2) * (sig2 + s2 - strenght_yield_2) * podat2
        #         eps2_in_strain = (sig2 - s2) * D2 + Hev(sig2 - s2 - strenght

    # Обновляем пределы текучести
    # if sig1 + s1 > strenght_yield_1_aust:
    #     update_constant('strenght_yield_1_aust', sig1 + s1)
    # if sig1 - s1 > strenght_yield_1_aust:
    #     update_constant('strenght_yield_1_aust', sig1 - s1)
    # if sig2 + s2 > strenght_yield_2:
    #     update_constant('strenght_yield_2', sig2 + s2)
    # if sig2 - s2 > strenght_yield_2:
    #     update_constant('strenght_yield_2', sig2 - s2)



    return (
        sig1,
        s1,
        sig2,
        s2,
        list_force[-1],
        eps1_out_strain,
        eps1_in_strain,
        list_t,
        list_sig1,
        list_sig2,
        list_force,
        Fi,
        list_Fi
    )
    '''


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

    # Фазовый драйвер нагрева (восстановлено по `bimet_stopka.cpp`).
    # Eps1outF = Eps1outMax - Sig1_out_Yield / E1M_U
    # eps0_heat_out = Kr * Eps1outF
    #
    # Аналогично для in-волокон.
    sig1_out_curr = sig1 + s1
    sig1_in_curr = sig1 - s1
    sig1_out_yield = strenght_yield_1 if sig1_out_curr >= 0 else -strenght_yield_1
    sig1_in_yield = strenght_yield_1 if sig1_in_curr >= 0 else -strenght_yield_1

    eps1_outF = eps1_out_max_0 - sig1_out_yield / unloading_young_module_1
    eps1_inF = eps1_in_max_0 - sig1_in_yield / unloading_young_module_1

    # Фазовая деформация при нагреве: весь кристаллический слой сжимается
    # при ЭПФ. Начальная деформация eps0 = delta/l_out задаёт масштаб
    # деформации, накопленной при кристаллизации. При обратном превращении
    # восстанавливается Kr·eps0 РАВНОМЕРНО по всему слою (не только outer fiber).
    eps0_uniform = rec_ratio * (delta / ((arc_length / rad) * (h1 + h2 + rad) - delta))
    eps0_heat_out = eps0_uniform
    eps0_heat_in = eps0_uniform

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

    while t <= t_finish:
        dPhi = compute_dPhi(Fi_old, t, dT)
        Fi = Fi_old + dPhi
        # Численная защита: Φ должна оставаться в [0, 1]
        if Fi < 0.0:
            Fi = 0.0
        elif Fi > 1.0:
            Fi = 1.0

        alpha1 = alpha1_aust * (1 - Fi) + alpha1_mart * Fi
        d_alpha1 = alpha1 - alpha1_old

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

    if jump_events:
        print(f"\n[JUMP] heating: collected {len(jump_events)} events (showing all)")
        for i, ev in enumerate(jump_events, 1):
            print(
                f"[JUMP][heat #{i}] t={ev['t']:.3f} Fi={ev['Fi']:.6f} dPhi={ev['dPhi']:.6e} "
                f"Fprev={ev['Fprev']:.6g} dF={ev['dF']:.6g} F={ev['F']:.6g} thr={ev['thr']:.6g} "
                f"hev={ev['hev']} hev_changed={ev['hev_changed']}"
            )
            print(
                f"           x={tuple(f'{v:.6e}' for v in ev['x'])} d_sig={tuple(f'{v:.6e}' for v in ev['d_sig'])}"
            )
            print(
                f"           phase(out,in)={tuple(f'{v:.6e}' for v in ev['phase'])} "
                f"thermal(1,2)={tuple(f'{v:.6e}' for v in ev['thermal'])} "
                f"C(out1,in1,out2,in2)={tuple(f'{v:.6e}' for v in ev['C'])}"
            )
            print(
                f"           sig_curr={tuple(f'{v:.6e}' for v in ev['sig_curr'])} "
                f"sig_trial={tuple(f'{v:.6e}' for v in ev['sig_trial'])}"
            )

    if turn_events:
        print(f"\n[TURN] heating: collected {len(turn_events)} turn events (near Af)")
        for i, ev in enumerate(turn_events, 1):
            print(
                f"[TURN][heat #{i}] t={ev['t']:.3f} Fi={ev['Fi']:.6f} dPhi={ev['dPhi']:.6e} "
                f"dF_prev={ev['dF_prev']:.6g} dF={ev['dF']:.6g} F={ev['F']:.6g} hev={ev['hev']}"
            )
            print(
                f"           phase(out,in)={tuple(f'{v:.6e}' for v in ev['phase'])} "
                f"thermal(1,2)={tuple(f'{v:.6e}' for v in ev['thermal'])} "
                f"d_sig={tuple(f'{v:.6e}' for v in ev['d_sig'])}"
            )

    print_peak_force_passport(
        "heating",
        list_force,
        list_t,
        list_Fi,
        peak_rows,
        extra_note=f"part_len={part_len}, h1={h1}, h2={h2}",
    )

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
    peak_rows: list[dict] = []

    Fi_old = Fi
    alpha1_old = alpha1_aust * (1 - Fi_old) + alpha1_mart * Fi_old
    list_Fi = [Fi]

    # Фазовая деформация на охлаждении.
    # В Belyaev et al. (2015): dε_ph = (σ*/E_TP + Ω * ε*) dΦ,
    # где ε* — необратимая деформация после нагрева (константа на протяжении охлаждения),
    # σ* — текущие напряжения. Поэтому:
    eps_star_out = float(eps1_out_strain)
    eps_star_in = float(eps1_in_strain)

    # Фиксированные eps0_cool — вычисляются один раз по напряжениям на начало охлаждения
    sig1_out_hot = sig1 + s1
    sig1_in_hot = sig1 - s1
    eps0_cool_out_raw = sig1_out_hot / young_module_TP + lam * eps_star_out
    eps0_cool_in_raw = sig1_in_hot / young_module_TP + lam * eps_star_in
    # Ограничение: при полном цикле (ΔΦ=1) охлаждение не должно перекомпенсировать нагрев.
    # eps0_cool ≤ eps0_heat, иначе F уйдёт в минус (физически лента не тянет опору).
    eps0_uniform = rec_ratio * (delta / ((arc_length / rad) * (h1 + h2 + rad) - delta))
    eps0_cool_out_fixed = min(eps0_cool_out_raw, eps0_uniform)
    eps0_cool_in_fixed = min(eps0_cool_in_raw, eps0_uniform)

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

    while t >= t_finish:
        dPhi = compute_dPhi(Fi_old, t, dT)
        Fi = Fi_old + dPhi
        # Численная защита: Φ должна оставаться в [0, 1]
        if Fi < 0.0:
            Fi = 0.0
        elif Fi > 1.0:
            Fi = 1.0

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

        # (6) Belyaev: фазовый вклад на охлаждении + σ*·d(1/E₁) [формула (7)]
        eps0_cool_out = (sig1_out_curr) / young_module_TP + lam * eps_star_out
        eps0_cool_in = (sig1_in_curr) / young_module_TP + lam * eps_star_in
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
                "eps0_cool_out": eps0_cool_out_fixed,
                "eps0_cool_in": eps0_cool_in_fixed,
            }
        )

    if jump_events:
        print(f"\n[JUMP] cooling: collected {len(jump_events)} events (showing all)")
        for i, ev in enumerate(jump_events, 1):
            print(
                f"[JUMP][cool #{i}] t={ev['t']:.3f} Fi={ev['Fi']:.6f} dPhi={ev['dPhi']:.6e} "
                f"Fprev={ev['Fprev']:.6g} dF={ev['dF']:.6g} F={ev['F']:.6g} thr={ev['thr']:.6g} "
                f"hev={ev['hev']} hev_changed={ev['hev_changed']}"
            )
            print(
                f"           x={tuple(f'{v:.6e}' for v in ev['x'])} d_sig={tuple(f'{v:.6e}' for v in ev['d_sig'])}"
            )
            print(
                f"           phase(out,in)={tuple(f'{v:.6e}' for v in ev['phase'])} "
                f"thermal(1,2)={tuple(f'{v:.6e}' for v in ev['thermal'])} "
                f"C(out1,in1,out2,in2)={tuple(f'{v:.6e}' for v in ev['C'])}"
            )
            print(
                f"           sig_curr={tuple(f'{v:.6e}' for v in ev['sig_curr'])} "
                f"sig_trial={tuple(f'{v:.6e}' for v in ev['sig_trial'])}"
            )

    if plane_warn_count:
        print(f"\n[WARN] cooling: plane-sections check failed {plane_warn_count} times")
    if kin_warn_count:
        print(f"\n[WARN] cooling: kin-constraints (dEps equalities) exceeded tol {kin_warn_count} times")
    if curv_warn_count:
        print(f"\n[WARN] cooling: curvature-preservation error exceeded tol {curv_warn_count} times")
    if neq_warn_count:
        print(f"\n[WARN] cooling: N-equilibrium residual exceeded tol {neq_warn_count} times")

    print_peak_force_passport(
        "cooling",
        list_force,
        list_t,
        list_Fi,
        peak_rows,
        extra_note=f"part_len={part_len}, h1={h1}, h2={h2}",
    )

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
