import numpy
import matplotlib.pyplot as plt
from const import *

podat1_unload = (1 / strengthening_coefficient_1) - (1 / unloading_young_module_1)
podat1_load = (1 / strengthening_coefficient_1) - (1 / loading_young_module_1)
podat2 = (1 / strengthening_coefficient_2) - (1 / young_module_2)


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


def plot_graph(
    y_values, x_values, y_label="Y-Axis", x_label="X-Axis", title="График зависимости"
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
    plt.show()


# Функция для обновления констант в файле
def update_constant(parameter_name, new_value):
    with open('D:\GitHub_projects\my_university\labSME\const.py', "r") as f:
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
def unloading(bending_moment, sig1_out, sig1_in, sig2_in, sig2_out, eps1_out, eps1_in, eps2_out, eps2_in):
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
    while M > 0:
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

        list_e1o.append(eps1_out)
        list_e2o.append(eps2_out)
        list_e1i.append(eps1_in)
        list_e2i.append(eps2_in)

        eps_elastic = (eps1_out - eps2_out) / (2 * (1 + eps2_out))

        # Обновляем пределы текучести
    # if sig1 + s1 > strenght_yield_1:
    #     update_constant('strenght_yield_1', sig1 + s1)
    # if sig1 - s1 > strenght_yield_1:
    #     update_constant('strenght_yield_1', sig1 - s1)
    # if sig2 + s2 > strenght_yield_2:
    #     update_constant("strenght_yield_2", sig2 + s2)
    # if sig2 - s2 > strenght_yield_2:
    #     update_constant("strenght_yield_2", sig2 - s2)
    # plot_graph(list_e1o, [i*0.1 for i in range(len(list_e1o))], y_label="Eps1_out", x_label="Number", title="График зависимости")
    # plot_graph(list_e2o, [i*0.1 for i in range(len(list_e1o))], y_label="Eps2_out", x_label="Number", title="График зависимости")
    plot_graph(list_e1i, list_e2i, y_label="Eps1_in", x_label="Eps2_in", title="Деформации внутренних слоев")
    print(f'Проверка гипотезы плоских сечений: (eps1_out - eps1_in)/(eps2_in - eps2_out) = {(list_e1o[-1] - delta/len_o1 - list_e1i[-1])/(list_e2i[-1] - list_e2o[-1])} и h1/h2 = {h1/h2}')
    # #---------------------------
    # plot_graph(list_sig1o, list_e1o, y_label="sigma1_out", x_label="Eps", title="График зависимости")
    # plot_graph(list_sig2o, list_e2o, y_label="sigma2_out", x_label="Eps", title="График зависимости")
    # plot_graph(list_sig1in, list_e1i, y_label="sigma1_in", x_label="Eps", title="График зависимости")
    # plot_graph(list_sig2in, list_e2i, y_label="sigma2_in", x_label="Eps", title="График зависимости")

    # plot_graph(list_sig1o, [i*0.1 for i in range(len(list_sig1o))], y_label="sig1_out", x_label="Number", title="График зависимости")
    # plot_graph(list_sig2o, [i*0.1 for i in range(len(list_sig2o))], y_label="sig2_out", x_label="Number", title="График зависимости")
    # plot_graph(list_sig1in, [i*0.1 for i in range(len(list_sig1in))], y_label="sig1_in", x_label="Number", title="График зависимости")
    # plot_graph(list_sig2in, [i*0.1 for i in range(len(list_sig2in))], y_label="sig2_in", x_label="Number", title="График зависимости")

    print(f'Оставшийся момент: {M}')
    print(f'Начальная длина внешнего слоя 1: {len_o1 + delta}, получивашаяся длина: {len_o1 + len_o1 * list_e1o[-1]}')
    print(f'Начальная длина внешнего слоя 2: {len_o2}, получивашаяся длина: {len_o2 + len_o2 * list_e2o[-1]}')
    print(f'Начальная длина слоя in: {len_in}, получивашаяся длина: {len_in + len_in * list_e1i[-1]}')
    # Деформации после разгрузки — для этапа нагрева (ε0 в отчёте: «начальная деформация» перед термоциклированием)
    eps1_out_after_unload = list_e1o[-1]
    eps1_in_after_unload = list_e1i[-1]
    return (sig1_out, sig1_in, sig2_in, sig2_out, sig1, s1, sig2, s2, eps1_out_after_unload, eps1_in_after_unload)


# Нагрев пластинки и рассчет df
# eps1_out_0, eps1_in_0 — деформации перед нагревом (после разгрузки), отчёт: ε0 — «начальная деформация»
def heating(eps1_out_0, eps1_in_0, t_start, t_finish, sig1, s1, sig2, s2):

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


# Нагрев с явным учётом неизменной кривизны (подставка под свободный конец).
# Система отчёта (15): dε^out_1 = dε^in_1 = dε^in_2 = dε^out_2 = 0.
# Вариант B: из (C)(D) и (5) получаем dσ2, ds2=0, dσ1; затем ds1 — полусумма из (A)(B).
def heating_constant_curvature(eps1_out_0, eps1_in_0, t_start, t_finish, sig1, s1, sig2, s2):

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
    E2 = young_module_2

    eps0_heat_out = rec_ratio * (eps1_out_0 - strenght_yield_1 / unloading_young_module_1)
    eps0_heat_in = rec_ratio * (eps1_in_0 - strenght_yield_1 / unloading_young_module_1)

    while t <= t_finish:

        d_Fi = -d_t / (m_start - m_finish) * Hev(1 - Fi_old) * Hev(m_start - Fi_old * (m_start - m_finish) - t) - d_t / (a_finish - a_start) * Hev(Fi_old) * Hev(t + Fi_old * (a_finish - a_start) - a_finish)
        Fi = Fi_old + d_Fi

        D1 = 1 / aust_young_module_1 * (1 - Fi) + 1 / loading_young_module_1 * Fi
        d_D1 = D1 - D1_old
        alpha1 = alpha1_aust * (1 - Fi) + alpha1_mart * Fi
        d_alpha1 = alpha1 - alpha1_old

        # (C)(D) отчёт: полное dε в слое 2 = 0 => ds2 = 0, dσ2 = -E2*α2*dT
        d_sig2 = -E2 * alpha2 * d_t
        d_s2 = 0.0

        # (5) равновесие: dσ1 = -(h2/h1)*dσ2
        d_sig1 = -(h2 / h1) * d_sig2

        # (A)(B): (dσ1±ds1)*D1 = -R_out/in; R = K*ε0*dΦ + α1*dT + (dα1)*T
        R_out = eps0_heat_out * d_Fi + alpha1 * d_t + d_alpha1 * t
        R_in = eps0_heat_in * d_Fi + alpha1 * d_t + d_alpha1 * t
        # ds1 — полусумма двух выражений из (A) и (B) для согласованности с обоими волокнами слоя 1
        ds1_from_A = -R_out / D1 - d_sig1
        ds1_from_B = d_sig1 + R_in / D1
        d_s1 = 0.5 * (ds1_from_A + ds1_from_B)

        # (18) отчёт: усилие, развиваемое лентой (без минуса)
        d_f = (h1 * h1 / (6 * part_len)) * (3 * d_sig1 + d_s1 - 3 * h2 * h2 * d_sig2 / (h1 * h1) + h2 * h2 * d_s2 / (h1 * h1))
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

    # Итоговые деформации по напряжению (для охлаждения)
    D1_fin = 1 / aust_young_module_1 * (1 - Fi) + 1 / loading_young_module_1 * Fi
    eps1_out_strain = (sig1 + s1) * D1_fin + Hev(sig1 + s1 - strenght_yield_1_aust) * (sig1 + s1 - strenght_yield_1_aust) * podat1_load
    eps1_in_strain = (sig1 - s1) * D1_fin + Hev(sig1 - s1 - strenght_yield_1_aust) * (sig1 - s1 - strenght_yield_1_aust) * podat1_load

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
        list_Fi,
    )


# Охлаждение и рассчет силы
def cooling(
t_start, t_finish, force_start, eps1_out_strain, eps1_in_strain, sig1, s1, sig2, s2, Fi):

    d_t = 0.0005
    force = force_start
    t = t_start
    list_force = [force_start]
    list_t = [t_start]
    list_sig1 = [sig1]
    list_sig2 = [sig2]

    D2 = 1 / young_module_2
    Fi_old = Fi  # инициализация перед циклом (исправление: в цикле использовался неинициализированный Fi_old)
    D1_old = 1 / aust_young_module_1 * (1 - Fi) + 1 / loading_young_module_1 * Fi
    alpha1_old = alpha1_aust * (1 - Fi) + alpha1_mart * Fi

    eps0_cool_out = lam * eps1_out_strain + (sig1 + s1) / young_module_TP
    eps0_cool_in = lam * eps1_in_strain + (sig1 - s1) / young_module_TP

    while t >= t_finish:

        d_Fi = -d_t / (m_start - m_finish) * Hev(1 - Fi_old) * Hev(m_start - Fi_old * (m_start - m_finish) - t) - d_t / (a_finish - a_start) * Hev(Fi_old) * Hev(t + Fi_old * (a_finish - a_start) - a_finish)
        Fi = Fi_old + d_Fi

        D1 = 1 / aust_young_module_1 * (1 - Fi) + 1 / loading_young_module_1 * Fi
        d_D1 = D1 - D1_old

        alpha1 = alpha1_aust * (1 - Fi) + alpha1_mart * Fi
        d_alpha1 = alpha1 - alpha1_old

        d_sig2 = (h1 / (h2 * D1)) * (sig1 * d_D1 + d_alpha1 * t + alpha1 * d_t + (eps0_cool_out + eps0_cool_in) * d_Fi / 2)
        d_sig1 = -(1 / D1) * (sig1 * d_D1 + d_alpha1 * t + alpha1 * d_t + (eps0_cool_out + eps0_cool_in) * d_Fi / 2)
        d_s1 = (1 / D1) * ((eps0_cool_in - eps0_cool_out) * d_Fi / 2 - podat1_load * d_D1)
        d_s2 = -d_sig2 - alpha2 * d_t / (D2 + podat2 * Hev(abs(sig2 + s2) - strenght_yield_2) * Hev(0))

        d_f = (h1 * h1 / (6 * part_len)) * (3 * d_sig1 + d_s1 - 3 * h2 * h2 * d_sig2 / (h1 * h1) + h2 * h2 * d_s2 / (h1 * h1))
        force -= d_f
        list_force.append(force)

        sig2 += d_sig2
        list_sig2.append(sig2)
        sig1 += d_sig1
        list_sig1.append(sig1)
        s1 += d_s1
        s2 += d_s2
        alpha1_old = alpha1
        t -= d_t  # при охлаждении температура уменьшается
        list_t.append(t)
        D1_old = D1
        Fi_old = Fi

    # if sig2 + s2 > strenght_yield_2:
    #     update_constant('strenght_yield_2', sig2 + s2)
    # if sig2 - s2 > strenght_yield_2:
    #     update_constant('strenght_yield_2', sig2 - s2)

    # Считаем деформацию от напряжений по закону Гука
    D1 = 1 / aust_young_module_1 * (1 - Fi) + 1 / loading_young_module_1 * Fi
    eps1_out_strain = (sig1 + s1) * D1 + Hev(sig1 + s1 - strenght_yield_1_aust) * (sig1 + s1 - strenght_yield_1_aust) * podat1_load
    eps1_in_strain = (sig1 - s1) * D1 + Hev(sig1 - s1 - strenght_yield_1_aust) * (sig1 - s1 - strenght_yield_1_aust) * podat1_load
    eps2_in_strain = (sig2 + s2) * D2 + Hev(sig2 + s2 - strenght_yield_2) * (sig2 + s2 - strenght_yield_2) * podat2
    eps2_out_strain = (sig2 - s2) * D2 + Hev(sig2 - s2 - strenght_yield_2) * (sig2 - s2 - strenght_yield_2) * podat2

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
    )
