import numpy
import pandas as pd
import matplotlib.pyplot as plt
def plot_graph(
    y_values, x_values, y_label="Y-Axis", x_label="X-Axis", title="График зависимости"):
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
    plt.plot(x_values, y_values, marker="", linestyle="-")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(f"{title} {y_label} от {x_label}")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
df = pd.read_excel("C:/Users/79125/Desktop/laba1.xlsx", header=0)
#print(df.columns)
plot_graph(df['7faza'], df['2tem/K'],'Faza', 'Temp')
plot_graph(df['3e33/pct'], df['2tem/K'],'Eps', 'Temp')
