import tkinter as tk
import random
from tkinter import filedialog
import time
import timeit
import matplotlib.pyplot as plt
import os

class FileGenerationWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Генерация файла")
        self.parent = parent

        # Создаем элементы управления для выбора названия файла и типа последовательности
        self.file_name_label = tk.Label(self, text="Название файла:")
        self.file_name_entry = tk.Entry(self)
        self.sequence_type_label = tk.Label(self, text="Тип последовательности:")
        self.sequence_type_var = tk.StringVar(self)
        self.sequence_type_var.set("Упорядоченная по возрастанию")
        self.sequence_type_menu = tk.OptionMenu(self, self.sequence_type_var,
                                                "Упорядоченная по возрастанию",
                                                "Упорядоченная по убыванию",
                                                "Случайная")
        self.digits_label = tk.Label(self, text="Количество разрядов для чисел:")
        self.digits_entry = tk.Entry(self)
        self.elements_label = tk.Label(self, text="Количество элементов:")
        self.elements_entry = tk.Entry(self)
        self.generate_button = tk.Button(self, text="Сгенерировать", command=self.generate_file)

        # Позиционируем элементы на форме
        self.file_name_label.pack()
        self.file_name_entry.pack()
        self.sequence_type_label.pack()
        self.sequence_type_menu.pack()
        self.digits_label.pack()
        self.digits_entry.pack()
        self.elements_label.pack()
        self.elements_entry.pack()
        self.generate_button.pack()

    def generate_file(self):
        # Получаем значения из элементов управления
        file_name = self.file_name_entry.get()
        sequence_type = self.sequence_type_var.get()
        digits = int(self.digits_entry.get())
        elements = int(self.elements_entry.get())

        # Генерируем последовательность чисел в соответствии с выбранным типом
        if sequence_type == "Упорядоченная по возрастанию":
            sequence = generate_ordered_sequence(digits, elements, "Упорядоченная по возрастанию")
        elif sequence_type == "Упорядоченная по убыванию":
            sequence = generate_ordered_sequence(digits, elements, "Упорядоченная по убыванию")
        elif sequence_type == "Случайная":
            sequence = [random.randint(10 ** (digits - 1), 10 ** digits - 1) for _ in range(elements)]

        # Формируем полный путь к файлу в текущей директории проекта
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, file_name + ".txt")

        try:
            with open(file_path, 'w') as file:
                for number in sequence:
                    file.write(str(number) + " ")

            # Выводим сообщение о успешной генерации файла
            print("Файл успешно сгенерирован:", file_path)

        except FileNotFoundError:
            print("Ошибка при сохранении файла.")


def generate_ordered_sequence(digits, elements, order):
    sequence = []
    current_number = 10 ** digits - 1 if order == "Упорядоченная по убыванию" else 10 ** (digits - 1)
    step = -1 if order == "Упорядоченная по убыванию" else 1

    for _ in range(elements):
        sequence.append(current_number)
        current_number += step

    return sequence


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
        self.generate_button = tk.Button(self, text="Генерация", command=self.open_generation_window)

        # Позиционируем элементы на форме
        self.open_button.pack()
        self.generate_button.pack()
        self.exit_button.pack()

        # Создаем гистограммы
        self.fig = None
        self.axs = None

    def open_file(self):
        file_paths = filedialog.askopenfilenames()

        if not file_paths:
            return

        try:
            swaps = []
            comparisons = []
            times = []

            max_swaps = 0
            max_comparisons = 0
            max_time = 0.0

            for file_path in file_paths:
                with open(file_path, 'r') as file:
                    sequence = []
                    for line in file:
                        numbers = line.strip().split()
                        sequence.extend(map(int, numbers))

                    sorted_sequence_1, time_1, comparisons_1, swaps_1 = self.patience_sort(sequence)
                    sorted_sequence_2, time_2, comparisons_2, swaps_2 = self.radix_sort(sequence)

                    swaps.append((swaps_1, swaps_2))
                    comparisons.append((comparisons_1, comparisons_2))
                    times.append((float(time_1), float(time_2)))

                    # Обновляем максимальные значения
                    max_swaps = max(max_swaps, swaps_1, swaps_2)
                    max_comparisons = max(max_comparisons, comparisons_1, comparisons_2)
                    max_time = max(max_time, float(time_1), float(time_2))

            self.create_histograms(len(file_paths), max_swaps, max_comparisons, max_time)
            self.update_histograms(file_paths, swaps, comparisons, times)
            self.show_histograms()

        except FileNotFoundError:
            print("Файл(ы) не найден(ы).")

    def create_histograms(self, num_files, max_swaps, max_comparisons, max_time):
        self.fig, self.axs = plt.subplots(3, num_files, figsize=(8 * num_files, 6))

        for i in range(num_files):
            ax_swaps = self.axs[0, i]
            ax_comparisons = self.axs[1, i]
            ax_time = self.axs[2, i]

            ax_swaps.set_xlabel("Файл " + str(i + 1))
            ax_comparisons.set_xlabel("Файл " + str(i + 1))
            ax_time.set_xlabel("Файл " + str(i + 1))

            ax_swaps.set_ylabel("Количество перестановок")
            ax_comparisons.set_ylabel("Количество сравнений")
            ax_time.set_ylabel("Время (сек)")

            ax_swaps.set_ylim(0, max_swaps)
            ax_comparisons.set_ylim(0, max_comparisons)
            ax_time.set_ylim(0, max_time)

    def update_histograms(self, file_paths, swaps, comparisons, times):
        num_files = len(file_paths)

        for i in range(num_files):
            file_name = os.path.basename(file_paths[i])
            ax_swaps = self.axs[0, i]
            ax_comparisons = self.axs[1, i]
            ax_time = self.axs[2, i]

            # Разбиваем данные по категориям
            swaps_1, swaps_2 = swaps[i]
            comparisons_1, comparisons_2 = comparisons[i]
            time_1, time_2 = times[i]

            # Строим гистограммы для каждой категории
            ax_swaps.bar([1, 2], [swaps_1, swaps_2], color=['blue', 'green'])
            ax_comparisons.bar([1, 2], [comparisons_1, comparisons_2], color=['blue', 'green'])
            ax_time.bar([1, 2], [time_1, time_2], color=['blue', 'green'])

            # Добавляем подписи к диаграммам
            ax_swaps.set_title("Перестановки (" + file_name + ")")
            ax_comparisons.set_title("Сравнения (" + file_name + ")")
            ax_time.set_title("Время (" + file_name + ")")

    def show_histograms(self):
        plt.tight_layout()
        plt.show()

    def open_generation_window(self):
        generation_window = FileGenerationWindow(self)

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

    def show_about(self):
        # Окно "О программе"
        about_window = tk.Toplevel(self)
        about_window.title("О программе")

        # Добавляем текст описания программы
        about_label = tk.Label(about_window, text="Это приложение сортирует введенную последовательность цифр "
                                                  "с использованием терпеливой и поразрядной сортировок.")
        about_label.pack()

        # Добавляем информацию о программе
        info_label = tk.Label(about_window, text="Разработчик: Волчков Николай")
        info_label.pack()

        version_label = tk.Label(about_window, text="Версия программы: 1.5")
        version_label.pack()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
