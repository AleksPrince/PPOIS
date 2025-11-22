from rule import Rule
from algorithm import MarkovAlgorithm

def get_user_rules():
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
    return rules

def run_console():
    print("\n=== Алгоритм Маркова ===")
    rules = get_user_rules()
    print()
    text = input("Введите строку: ").strip()
    algo = MarkovAlgorithm(rules)
    result = algo.run(text)
    print("Результат:", result)
