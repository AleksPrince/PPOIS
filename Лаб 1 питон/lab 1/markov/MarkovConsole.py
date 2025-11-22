from Rule import Rule
from MarkovAlgorithm import MarkovAlgorithm

class MarkovConsole:


    def __init__(self):
        self.rules = []

    def get_user_rules(self):

        rules = []
        print("Введите правила подстановки (пустой шаблон — завершение ввода):")
        while True:
            pattern = input("Шаблон: ").strip()
            if pattern == "":
                break
            replacement = input("Замена: ").strip()
            mode = input("Режим замены (0 — только первое, 1 — все перекрывающиеся): ").strip()
            full_replace = mode == "1"
            rules.append(Rule(pattern, replacement, full_replace))
        self.rules = rules
        return rules

    def run(self):

        print("\n=== Алгоритм Маркова ===")
        rules = self.get_user_rules()
        print()
        text = input("Введите строку: ").strip()
        algo = MarkovAlgorithm(rules)
        result = algo.run(text)
        print("Результат:", result)


if __name__ == "__main__":
    console = MarkovConsole()
    console.run()
