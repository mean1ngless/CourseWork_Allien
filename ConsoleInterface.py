import os
import json
import time
from datetime import datetime

import numpy as np

from ProblemGenerator import ProblemGenerator
from Distributions.GreedyDistribution import GreedyDistribution
from Distributions.GeneticDistribution import GeneticDistribution
from Expirements.TerminationConditionExperiment import TerminationConditionExperiment
from Expirements.MutationProbabilityExperiment import MutationProbabilityExperiment
from Expirements.ProblemSizeExperiment import ProblemSizeExperiment


class ConsoleInterface:
    def __init__(self):
        self.current_problem = None
        self.problems = {}

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_menu(self):
        self.clear_screen()
        print("=== Меню ===")
        print("1. Робота з індивідуальною задачею")
        print("2. Експериментальне дослідження алгоритмів")
        print("3. Вихід")

        choice = input("Оберіть пункт меню: ")
        return choice

    def individual_problem_menu(self):
        while True:
            self.clear_screen()
            print("=== Робота з індивідуальною задачею ===")
            print("1. Ввести дані вручну")
            print("2. Згенерувати випадкову задачу")
            print("3. Завантажити з файлу")
            print("4. Зберегти у файл")
            print("5. Редагувати поточну задачу")
            print("6. Розв'язати поточну задачу")
            print("7. Повернутися до головного меню")

            choice = input("Оберіть пункт меню: ")

            if choice == '1':
                self.manual_input()
            elif choice == '2':
                self.generate_problem()
            elif choice == '3':
                self.load_from_file()
            elif choice == '4':
                self.save_to_file()
            elif choice == '5':
                self.edit_problem()
            elif choice == '6':
                self.solve_current_problem()
            elif choice == '7':
                return
            else:
                print("Невірний вибір. Спробуйте ще раз.")
                input("Натисніть Enter для продовження...")

    def manual_input(self):
        self.clear_screen()
        print("=== Введення даних задачі ===")

        try:
            n = int(input("Кількість предметів: "))
            m = int(input("Кількість рук: "))

            print("\nВведіть параметри предметів:")
            items = []
            for i in range(n):
                print(f"\nПредмет {i + 1}:")
                weight = float(input("Вага: "))
                volume = float(input("Об'єм: "))
                items.append({'weight': weight, 'volume': volume})

            self.current_problem = {
                'n': n,
                'm': m,
                'items': items
            }

            # Зберігаємо в історію
            problem_id = f"manual_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.problems[problem_id] = self.current_problem.copy()

            print("\nЗадачу успішно створено!")
            input("Натисніть Enter для продовження...")
        except ValueError:
            print("Помилка введення даних!")
            input("Натисніть Enter для продовження...")

    def generate_problem(self):
        self.clear_screen()
        print("=== Генерація випадкової задачі ===")

        try:
            n = int(input("Кількість предметів: "))
            m = int(input("Кількість рук: "))
            Va = float(input("Мінімальний об'єм предмета: "))
            Vb = float(input("Максимальний об'єм предмета: "))
            Wa = float(input("Мінімальна вага предмета: "))
            Wb = float(input("Максимальна вага предмета: "))

            generator = ProblemGenerator(n, Va, Vb, Wa, Wb)
            items = generator.generate_as_dicts()

            self.current_problem = {
                'n': n,
                'm': m,
                'items': items,
                'params': {'Va': Va, 'Vb': Vb, 'Wa': Wa, 'Wb': Wb}
            }

            # Зберігаємо в історію
            problem_id = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.problems[problem_id] = self.current_problem.copy()

            print("\nЗадачу успішно згенеровано!")
            input("Натисніть Enter для продовження...")
        except ValueError:
            print("Помилка введення даних!")
            input("Натисніть Enter для продовження...")

    def load_from_file(self):
        self.clear_screen()
        print("=== Завантаження з файлу ===")

        filename = input("Введіть ім'я файлу (без розширення): ") + ".json"

        try:
            with open(filename, 'r') as f:
                data = json.load(f)

                if 'current' in data:
                    self.current_problem = data['current']
                if 'problems' in data:
                    self.problems.update(data['problems'])

                print("\nДані успішно завантажено!")
                input("Натисніть Enter для продовження...")
        except FileNotFoundError:
            print("Файл не знайдено!")
            input("Натисніть Enter для продовження...")
        except json.JSONDecodeError:
            print("Помилка читання файлу!")
            input("Натисніть Enter для продовження...")

    def save_to_file(self):
        self.clear_screen()
        print("=== Збереження у файл ===")

        if not self.current_problem:
            print("Немає поточної задачі для збереження!")
            input("Натисніть Enter для продовження...")
            return

        filename = input("Введіть ім'я файлу (без розширення): ") + ".json"

        data = {
            'current': self.current_problem,
            'problems': self.problems
        }

        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)

            print("\nДані успішно збережено!")
            input("Натисніть Enter для продовження...")
        except:
            print("Помилка при збереженні файлу!")
            input("Натисніть Enter для продовження...")

    def edit_problem(self):
        self.clear_screen()
        print("=== Редагування задачі ===")

        if not self.current_problem:
            print("Немає поточної задачі для редагування!")
            input("Натисніть Enter для продовження...")
            return

        print("\nПоточні параметри задачі:")
        print(f"Кількість предметів: {self.current_problem['n']}")
        print(f"Кількість рук: {self.current_problem['m']}")

        print("\nСписок предметів:")
        for i, item in enumerate(self.current_problem['items'], 1):
            print(f"{i}. Вага: {item['weight']:.2f}, Об'єм: {item['volume']:.2f}")

        print("\n1. Редагувати предмет")
        print("2. Додати предмет")
        print("3. Видалити предмет")
        print("4. Змінити кількість рук")
        print("5. Повернутися назад")

        choice = input("Оберіть дію: ")

        if choice == '1':
            self.edit_item()
        elif choice == '2':
            self.add_item()
        elif choice == '3':
            self.remove_item()
        elif choice == '4':
            self.change_hands()
        elif choice == '5':
            return
        else:
            print("Невірний вибір!")
            input("Натисніть Enter для продовження...")

    def edit_item(self):
        try:
            item_num = int(input("Введіть номер предмета для редагування: ")) - 1
            if item_num < 0 or item_num >= len(self.current_problem['items']):
                raise ValueError

            item = self.current_problem['items'][item_num]
            print(f"\nПоточні значення: Вага: {item['weight']:.2f}, Об'єм: {item['volume']:.2f}")

            item['weight'] = float(input("Нова вага: "))
            item['volume'] = float(input("Новий об'єм: "))

            print("Предмет успішно змінено!")
            input("Натисніть Enter для продовження...")
        except (ValueError, IndexError):
            print("Невірний номер предмета!")
            input("Натисніть Enter для продовження...")

    def add_item(self):
        try:
            weight = float(input("Вага нового предмета: "))
            volume = float(input("Об'єм нового предмета: "))

            self.current_problem['items'].append({'weight': weight, 'volume': volume})
            self.current_problem['n'] += 1

            print("Предмет успішно додано!")
            input("Натисніть Enter для продовження...")
        except ValueError:
            print("Помилка введення даних!")
            input("Натисніть Enter для продовження...")

    def remove_item(self):
        try:
            item_num = int(input("Введіть номер предмета для видалення: ")) - 1
            if item_num < 0 or item_num >= len(self.current_problem['items']):
                raise ValueError

            del self.current_problem['items'][item_num]
            self.current_problem['n'] -= 1

            print("Предмет успішно видалено!")
            input("Натисніть Enter для продовження...")
        except (ValueError, IndexError):
            print("Невірний номер предмета!")
            input("Натисніть Enter для продовження...")

    def change_hands(self):
        try:
            m = int(input("Нова кількість рук: "))
            if m < 1:
                raise ValueError

            self.current_problem['m'] = m
            print("Кількість рук успішно змінено!")
            input("Натисніть Enter для продовження...")
        except ValueError:
            print("Невірна кількість рук!")
            input("Натисніть Enter для продовження...")

    def solve_current_problem(self):
        self.clear_screen()
        print("=== Розв'язання поточної задачі ===")

        if not self.current_problem:
            print("Немає поточної задачі для розв'язання!")
            input("Натисніть Enter для продовження...")
            return

        items = self.current_problem['items']
        m = self.current_problem['m']

        print("\nРозв'язання жадібним алгоритмом:")
        start_time = time.time()
        greedy = GreedyDistribution(items, m)
        greedy_solution, gr_wdiff, gr_vdiff = greedy.distribute()
        greedy_time = time.time() - start_time

        print(f"Різниця ваг: {gr_wdiff:.2f}")
        print(f"Різниця об'ємів: {gr_vdiff:.2f}")
        print(f"Час виконання: {greedy_time:.4f} сек")
        print("\nРозподіл по руках (жадібний алгоритм):")
        for i, hand in enumerate(greedy_solution):
            print(f"  Рука {i + 1}: {[item for item in hand]}")

        print("\nРозв'язання генетичним алгоритмом:")
        start_time = time.time()
        genetic = GeneticDistribution(items, m, Np=50, Ng=100, Mp=0.1, Er=0.2)
        genetic_solution, ge_wdiff, ge_vdiff = genetic.evolve()
        genetic_time = time.time() - start_time

        print(f"Різниця ваг: {ge_wdiff:.2f}")
        print(f"Різниця об'ємів: {ge_vdiff:.2f}")
        print(f"Час виконання: {genetic_time:.4f} сек")
        print("\nРозподіл по руках (генетичний алгоритм):")
        for i, hand in enumerate(genetic_solution):
            print(f"  Рука {i + 1}: {[int(item) for item in hand]}")

        print("\nПорівняння результатів:")
        print(f"Покращення по вазі: {gr_wdiff / ge_wdiff:.2f}x")
        print(f"Покращення по об'єму: {gr_vdiff / ge_vdiff:.2f}x")
        print(f"Відношення часу: {genetic_time / greedy_time:.2f}x")

        input("\nНатисніть Enter для продовження...")

    def experimental_research_menu(self):
        while True:
            self.clear_screen()
            print("=== Експериментальне дослідження ===")
            print("1. Дослідження умови завершення (Ng/Np)")
            print("2. Дослідження ймовірності мутації")
            print("3. Дослідження впливу розміру задачі")
            print("4. Повернутися до головного меню")
            choice = input("Оберіть пункт меню: ")
            if choice == '1':
                self.termination_condition_experiment()
            elif choice == '2':
                self.mutation_experiment()
            elif choice == '3':
                self.problem_size_experiment()
            elif choice == '4':
                return
            else:
                print("Невірний вибір. Спробуйте ще раз.")
                input("Натисніть Enter для продовження...")

    def termination_condition_experiment(self):
        self.clear_screen()
        print("=== Експеримент: Умова завершення генетичного алгоритму ===")
        try:
            n = int(input("Кількість предметів: "))
            m = int(input("Кількість рук: "))
            Va = float(input("Мінімальний об'єм: "))
            Vb = float(input("Максимальний об'єм: "))
            Wa = float(input("Мінімальна вага: "))
            Wb = float(input("Максимальна вага: "))
            Mp = float(input("Ймовірність мутації: "))
            Er = float(input("Частка еліти: "))
            print("\nПараметри експерименту:")
            A_input = input("Список значень параметрів A: ")
            B_input = input("Список значень параметрів B: ")
            A = [int(x.strip()) for x in A_input.split(',')]
            B = [int(x.strip()) for x in B_input.split(',')]

            print("\nЗапуск експерименту...")
            experiment = TerminationConditionExperiment(n, m, Va, Vb, Wa, Wb, Mp, Er, A, B)
            result = experiment.run_and_analyze()

            analysis = result['detailed_results']
            optimal = analysis[np.argmin([x['total_diff'] for x in analysis])]

            print("\nРезультати експерименту:")
            print(f"Оптимальна комбінація: A={optimal['a']}, B={optimal['b']}")
            print(f"Рекомендована кількість ітерацій: {optimal['iterations']}")
            print("\nДетальні результати:")
            for res in analysis:
                print(
                    f"A={res['a']:4} | "
                    f"B={res['b']:4} | "
                    f"Різниця об'ємів: {res['avg_volume_diff']:.2f} | "
                    f"Різниця ваг: {res['avg_weight_diff']:.2f} | "
                    f"Сумарний добуток: {res['total_diff']:.2f}"
                )
            input("\nНатисніть Enter для продовження...")

        except Exception as e:
            print(f"\nПомилка: {e}")
            input("Натисніть Enter для повернення...")

    def mutation_experiment(self):
        self.clear_screen()
        print("=== Дослідження ймовірності мутації ===")

        try:
            n = int(input("Кількість предметів: "))
            m = int(input("Кількість рук: "))
            Va = float(input("Мінімальний об'єм: "))
            Vb = float(input("Максимальний об'єм: "))
            Wa = float(input("Мінімальна вага: "))
            Wb = float(input("Максимальна вага: "))
            Ng = int(input("Кількість поколінь: "))
            Np = int(input("Розмір популяції: "))
            Er = float(input("Частка еліти: "))

            mutations = input("Список ймовірностей мутації (через кому): ")
            mutation_list = [float(x.strip()) for x in mutations.split(',')]

            print("\nЗапуск експерименту...")
            experiment = MutationProbabilityExperiment(n, m, Va, Vb, Wa, Wb, Ng, Np, Er, mutation_list)
            Rv, Rw, analysis = experiment.run_full_experiment()

            print("\nРезультати експерименту:")
            print(f"Оптимальна ймовірність мутації: {analysis['optimal_mutation_prob']}")

            print("\nДетальні результати:")
            for res in analysis['detailed_results']:
                print(f"Ймовірність мутації: {res['mutation_prob']:.2f} | "
                      f"Різниця об'ємів: {res['avg_volume_diff']:.2f} | "
                      f"Різниця ваг: {res['avg_weight_diff']:.2f} | "
                      f"Сумарна різниця: {res['total_diff']:.2f}")

            input("\nНатисніть Enter для продовження...")
        except ValueError as e:
            print(f"Помилка введення даних: {e}")
            input("Натисніть Enter для продовження...")

    def problem_size_experiment(self):
        self.clear_screen()
        print("=== Дослідження впливу розміру задачі ===")

        try:
            m = int(input("Кількість рук: "))
            Va = float(input("Мінімальний об'єм: "))
            Vb = float(input("Максимальний об'єм: "))
            Wa = float(input("Мінімальна вага: "))
            Wb = float(input("Максимальна вага: "))
            Ng = int(input("Кількість поколінь (для GA): "))
            Np = int(input("Розмір популяції (для GA): "))
            Mp = float(input("Ймовірність мутації (для GA): "))
            Er = float(input("Частка еліти (для GA): "))

            sizes = input("Список кількостей предметів (через кому): ")
            size_list = [int(x.strip()) for x in sizes.split(',')]

            print("\nЗапуск експерименту...")
            experiment = ProblemSizeExperiment(size_list, m, Va, Vb, Wa, Wb, Ng, Np, Mp, Er)
            results, analysis = experiment.run_full_experiment()

            print("\nРезультати експерименту:")
            for n in size_list:
                print(f"\nКількість предметів: {n}")
                print("Жадібний алгоритм:")
                print(f"  Різниця об'ємів: {analysis[n]['greedy']['avg_volume_diff']:.2f}")
                print(f"  Різниця ваг: {analysis[n]['greedy']['avg_weight_diff']:.2f}")
                print(f"  Час: {analysis[n]['greedy']['avg_time']:.4f} сек")
                print("Генетичний алгоритм:")
                print(f"  Різниця об'ємів: {analysis[n]['genetic']['avg_volume_diff']:.2f}")
                print(f"  Різниця ваг: {analysis[n]['genetic']['avg_weight_diff']:.2f}")
                print(f"  Час: {analysis[n]['genetic']['avg_time']:.4f} сек")
                print(f"  Покращення якості: {analysis[n]['improvement_ratio']:.2f}x")

            input("\nНатисніть Enter для продовження...")
        except ValueError as e:
            print(f"Помилка введення даних: {e}")
            input("Натисніть Enter для продовження...")

    def run(self):
        while True:
            choice = self.show_menu()

            if choice == '1':
                self.individual_problem_menu()
            elif choice == '2':
                self.experimental_research_menu()
            elif choice == '3':
                print("Вихід з програми...")
                break
            else:
                print("Невірний вибір. Спробуйте ще раз.")
                input("Натисніть Enter для продовження...")