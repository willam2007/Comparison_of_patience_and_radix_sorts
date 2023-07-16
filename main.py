import tkinter as tk
import random
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

    def plot_graph(self, sequence, sorted_sequence_1, sorted_sequence_2, comparisons_1, comparisons_2, swaps_1, swaps_2,
                   sequence_type):
        # Создаем списки для количества сравнений и перестановок
        comparisons = [comparisons_1, comparisons_2]
        swaps = [swaps_1, swaps_2]

        # Создаем графическую диаграмму
        labels = ['Терпеливая сортировка', 'Поразрядная сортировка']
        comparisons_values = comparisons
        swaps_values = swaps

        # Создаем фигуру и подграфики
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

        # Диаграмма для количества сравнений
        ax1.bar(labels, comparisons_values)
        ax1.set_ylabel('Количество сравнений')
        ax1.set_title('Сравнения по типу последовательности: ' + sequence_type)

        # Диаграмма для количества перестановок
        ax2.bar(labels, swaps_values)
        ax2.set_ylabel('Количество перестановок')

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
