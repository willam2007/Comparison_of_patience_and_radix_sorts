import tkinter as tk
from tkinter import filedialog
import random
import time
import timeit
import matplotlib.pyplot as plt
import os
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Сортировка последовательности")

        # Создаем главное меню
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        # Создаем подменю "О программе"
        self.about_menu = tk.Menu(self.menu, tearoff=False)
        self.about_menu.add_command(label="О программе", command=self.show_about)
        self.menu.add_cascade(label="Меню", menu=self.about_menu)

        # Создаем кнопки и поле для выбора файла
        self.open_button = tk.Button(self, text="Открыть файл", command=self.open_file)
        self.exit_button = tk.Button(self, text="Выход", command=self.quit)
        self.file_path_label = tk.Label(self, text="Путь к файлу:")
        self.file_path_entry = tk.Entry(self)

        # Позиционируем элементы на форме
        self.file_path_label.pack()
        self.file_path_entry.pack()
        self.open_button.pack()
        self.exit_button.pack()

    def open_file(self):
        file_path = filedialog.askopenfilename()

        try:
            with open(file_path, 'r') as file:
                sequence = []
                for line in file:
                    numbers = line.strip().split()
                    sequence.extend(map(int, numbers))

            sorted_sequence_1, time_1, comparisons_1, swaps_1 = self.patience_sort(sequence)
            sorted_sequence_2, time_2, comparisons_2, swaps_2 = self.radix_sort(sequence)

            # Выводим результаты и время выполнения
            self.plot_graph(sequence, sorted_sequence_1, sorted_sequence_2, time_1, time_2, comparisons_1,
                            comparisons_2, swaps_1, swaps_2, file_path)

        except FileNotFoundError:
            print("Файл не найден.")

    def patience_sort(self, sequence):
        sequence = list(map(int, sequence))

        piles = []
        comparisons = 0  # Количество сравнений
        swaps = 0  # Количество перестановок

        start_time = timeit.default_timer()

        for num in sequence:
            found_pile = False
            for pile in piles:
                comparisons += 1  # Увеличиваем количество сравнений
                if num >= pile[-1]:
                    pile.append(num)
                    found_pile = True
                    break

            if not found_pile:
                new_pile = [num]
                piles.append(new_pile)

            swaps += 1  # Увеличиваем количество перестановок

        sorted_piles = sorted(piles, key=lambda pile: pile[0])

        sorted_sequence = []
        while sorted_piles:
            min_pile_idx = 0
            for i in range(1, len(sorted_piles)):
                comparisons += 1  # Увеличиваем количество сравнений
                if sorted_piles[i][0] < sorted_piles[min_pile_idx][0]:
                    min_pile_idx = i

            min_num = sorted_piles[min_pile_idx].pop(0)
            sorted_sequence.append(min_num)
            if len(sorted_piles[min_pile_idx]) == 0:
                sorted_piles.pop(min_pile_idx)

            swaps += 1  # Увеличиваем количество перестановок

        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time
        elapsed_time_str = "{:.9f}".format(elapsed_time)

        return sorted_sequence, elapsed_time_str, comparisons, swaps

    def radix_sort(self, sequence):
        sequence = list(map(int, sequence))
        comparisons = 0  # Количество сравнений
        swaps = 0  # Количество перестановок

        start_time = timeit.default_timer()

        max_digits = len(str(max(sequence)))

        for digit_idx in range(max_digits):
            buckets = [[] for _ in range(10)]

            for num in sequence:
                digit = (num // 10 ** digit_idx) % 10
                buckets[digit].append(num)

            sequence = [num for bucket in buckets for num in bucket]

            comparisons += len(sequence) - 1  # Увеличиваем количество сравнений
            swaps += len(sequence)  # Увеличиваем количество перестановок

        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time
        elapsed_time_str = "{:.9f}".format(elapsed_time)

        sorted_sequence = sequence
        return sorted_sequence, elapsed_time_str, comparisons, swaps

    def plot_graph(self, sequence, sorted_sequence_1, sorted_sequence_2, time_1, time_2, comparisons_1, comparisons_2,
                   swaps_1, swaps_2, file_path):
        # Создаем списки для количества сравнений и перестановок
        comparisons = [comparisons_1, comparisons_2]
        swaps = [swaps_1, swaps_2]

        # Извлекаем только имя файла из полного пути
        file_name = os.path.basename(file_path)

        # Создаем фигуру и подграфики
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

        # Диаграмма для количества сравнений
        labels = ['Терпеливая сортировка', 'Поразрядная сортировка']
        comparisons_values = [comparisons_1, comparisons_2]
        ax1.bar(labels, comparisons_values)
        ax1.set_ylabel('Количество сравнений')
        ax1.set_title('Сравнения для файла: ' + file_name)

        # Диаграмма для количества перестановок
        ax2.bar(labels, swaps)
        ax2.set_ylabel('Количество перестановок')

        # Добавляем время работы сортировок
        ax2.text(0, -20, time_1 + ' сек', ha='center', fontsize=12, fontweight='bold')
        ax2.text(1, -20, time_2 + ' сек', ha='center', fontsize=12, fontweight='bold')

        # Размещение диаграмм на форме
        plt.tight_layout()
        plt.show()

    def show_about(self):
        # Окно "О программе"
        about_window = tk.Toplevel(self)
        about_window.title("О программе")

        # Добавляем текст описания программы
        about_label = tk.Label(about_window, text="Это приложение сортирует введенную последовательность цифр "
                                                  "с использованием терпеливой и поразрядной сортировок.")
        about_label.pack()

        # Добавляем информацию о программе
        info_label = tk.Label(about_window, text="Разработчик: Ваше имя")
        info_label.pack()

        version_label = tk.Label(about_window, text="Версия программы: 1.0")
        version_label.pack()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
