import tkinter as tk
import random
import time
import timeit
import matplotlib.pyplot as plt

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

        # Создаем кнопки и поле для выбора типа последовательности
        self.generate_button = tk.Button(self, text="Генерация последовательности", command=self.generate_sequence)
        self.exit_button = tk.Button(self, text="Выход", command=self.quit)
        self.num_count_label = tk.Label(self, text="Количество чисел:")
        self.num_count_entry = tk.Entry(self)
        self.sequence_type_label = tk.Label(self, text="Тип:")
        self.sequence_type_var = tk.StringVar()
        self.sequence_type_var.set("Случайная")
        self.sequence_type_menu = tk.OptionMenu(self, self.sequence_type_var, "Случайная", "Повторяющаяся", "Упорядоченная")

        # Позиционируем элементы на форме
        self.num_count_label.pack()
        self.num_count_entry.pack()
        self.sequence_type_label.pack()
        self.sequence_type_menu.pack()
        self.generate_button.pack()
        self.exit_button.pack()

        # Создаем метки и текстовые поля для вывода результатов и времени выполнения
        self.result_label_1 = tk.Label(self, text="Терпеливая сортировка:")
        self.result_label_1.pack()
        self.result_text_1 = tk.Text(self, width=30, height=5)
        self.result_text_1.pack()

        self.result_label_2 = tk.Label(self, text="Поразрядная сортировка:")
        self.result_label_2.pack()
        self.result_text_2 = tk.Text(self, width=30, height=5)
        self.result_text_2.pack()

        self.time_label_1 = tk.Label(self, text="Время выполнения терпеливой сортировки:")
        self.time_label_1.pack()
        self.time_text_1 = tk.Text(self, width=30, height=1)
        self.time_text_1.pack()

        self.time_label_2 = tk.Label(self, text="Время выполнения поразрядной сортировки:")
        self.time_label_2.pack()
        self.time_text_2 = tk.Text(self, width=30, height=1)
        self.time_text_2.pack()

    def generate_sequence(self):
        num_count = int(self.num_count_entry.get())
        sequence_type = self.sequence_type_var.get()  # Получаем выбранный тип последовательности

        if sequence_type == "Случайная":
            sequence = self.generate_random_sequence(num_count)
        elif sequence_type == "Повторяющаяся":
            sequence = self.generate_repeating_sequence(num_count)
        elif sequence_type == "Упорядоченная":
            sequence = self.generate_ordered_sequence(num_count)

        # Отсортируем последовательность двумя методами
        sorted_sequence_1, time_1, comparisons_1, swaps_1 = self.patience_sort(sequence)
        sorted_sequence_2, time_2, comparisons_2, swaps_2 = self.radix_sort(sequence)

        # Выводим результаты и время выполнения
        self.result_text_1.delete('1.0', tk.END)
        self.result_text_1.insert(tk.END, str(sorted_sequence_1))

        self.result_text_2.delete('1.0', tk.END)
        self.result_text_2.insert(tk.END, str(sorted_sequence_2))

        self.time_text_1.delete('1.0', tk.END)
        self.time_text_1.insert(tk.END, str(time_1))

        self.time_text_2.delete('1.0', tk.END)
        self.time_text_2.insert(tk.END, str(time_2))

        self.plot_graph(sequence, sorted_sequence_1, sorted_sequence_2, comparisons_1, comparisons_2, swaps_1, swaps_2,
                        sequence_type)

    def generate_random_sequence(self, num_count):
        sequence = [random.randint(1, 100) for _ in range(num_count)]
        return sequence

    def generate_repeating_sequence(self, num_count):
        num = random.randint(1, 100)
        sequence = [num] * num_count
        return sequence

    def generate_ordered_sequence(self, num_count):
        sequence = list(range(1, num_count + 1))
        return sequence

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
