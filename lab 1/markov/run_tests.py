#!/usr/bin/env python3
"""
Запуск тестов для класса Rule
"""

import unittest
import sys
from test_rule import TestRule, TestRuleEdgeCases


def run_all_tests():
    """Запуск всех тестов"""
    print("Запуск всех тестов для класса Rule...")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Добавляем все тесты
    suite.addTests(loader.loadTestsFromTestCase(TestRule))
    suite.addTests(loader.loadTestsFromTestCase(TestRuleEdgeCases))

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Возвращаем код выхода
    return 0 if result.wasSuccessful() else 1


def run_specific_test(test_name):
    """Запуск конкретного теста"""
    print(f"Запуск теста: {test_name}")
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(f"test_rule.{test_name}")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Запуск конкретного теста
        exit_code = run_specific_test(sys.argv[1])
    else:
        # Запуск всех тестов
        exit_code = run_all_tests()

    sys.exit(exit_code)