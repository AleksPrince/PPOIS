import unittest


class Rule:
    def __init__(self, pattern, replacement, full_replace=False):
        self.pattern = pattern
        self.replacement = replacement
        self.full_replace = full_replace

    def apply(self, text):
        if not self.pattern:
            return text, False

        if self.full_replace:
            # Заменить все вхождения (включая перекрывающиеся)
            if len(self.pattern) == 0:
                return text, False

            result = []
            i = 0
            changed = False
            n = len(self.pattern)

            while i < len(text):
                # Проверяем, есть ли паттерн на текущей позиции
                if i <= len(text) - n and text[i:i + n] == self.pattern:
                    result.append(self.replacement)
                    i += n  # Перескакиваем через весь паттерн
                    changed = True
                else:
                    result.append(text[i])
                    i += 1

            return ''.join(result), changed
        else:
            # Заменить только первое вхождение
            index = text.find(self.pattern)
            if index == -1:
                return text, False
            result = text[:index] + self.replacement + text[index + len(self.pattern):]
            return result, True


class TestRule30Tests(unittest.TestCase):

    def test_01_empty_pattern(self):
        """Пустой паттерн - без изменений"""
        rule = Rule("", "replacement")
        result, changed = rule.apply("some text")
        self.assertEqual(result, "some text")
        self.assertFalse(changed)

    def test_02_pattern_not_found(self):
        """Паттерн не найден - без изменений"""
        rule = Rule("xyz", "123")
        result, changed = rule.apply("some text")
        self.assertEqual(result, "some text")
        self.assertFalse(changed)

    def test_03_single_replacement_first(self):
        """Замена первого вхождения"""
        rule = Rule("test", "PASS")
        result, changed = rule.apply("this is test test string")
        self.assertEqual(result, "this is PASS test string")
        self.assertTrue(changed)

    def test_04_single_replacement_only(self):
        """Замена единственного вхождения"""
        rule = Rule("hello", "world")
        result, changed = rule.apply("say hello")
        self.assertEqual(result, "say world")
        self.assertTrue(changed)

    def test_05_pattern_at_beginning(self):
        """Паттерн в начале строки"""
        rule = Rule("start", "BEGIN")
        result, changed = rule.apply("start of text")
        self.assertEqual(result, "BEGIN of text")
        self.assertTrue(changed)

    def test_06_pattern_at_end(self):
        """Паттерн в конце строки"""
        rule = Rule("end", "FINISH")
        result, changed = rule.apply("text with end")
        self.assertEqual(result, "text with FINISH")
        self.assertTrue(changed)

    def test_07_empty_text(self):
        """Пустой входной текст"""
        rule = Rule("pattern", "replacement")
        result, changed = rule.apply("")
        self.assertEqual(result, "")
        self.assertFalse(changed)

    def test_08_pattern_equals_text(self):
        """Паттерн равен всему тексту"""
        rule = Rule("full", "REPLACED")
        result, changed = rule.apply("full")
        self.assertEqual(result, "REPLACED")
        self.assertTrue(changed)

    def test_09_full_replace_single(self):
        """Полная замена одного вхождения"""
        rule = Rule("test", "PASS", full_replace=True)
        result, changed = rule.apply("this is test")
        self.assertEqual(result, "this is PASS")
        self.assertTrue(changed)

    def test_10_full_replace_multiple(self):
        """Полная замена нескольких вхождений"""
        rule = Rule("ab", "XY", full_replace=True)
        result, changed = rule.apply("ab cd ab ef ab")
        self.assertEqual(result, "XY cd XY ef XY")
        self.assertTrue(changed)

    def test_11_full_replace_no_overlap(self):
        """Полная замена без перекрытий"""
        rule = Rule("a", "X", full_replace=True)
        result, changed = rule.apply("abcabc")
        self.assertEqual(result, "XbcXbc")
        self.assertTrue(changed)

    def test_12_full_replace_all_chars(self):
        """Замена всех символов"""
        rule = Rule("a", "X", full_replace=True)
        result, changed = rule.apply("aaaa")
        self.assertEqual(result, "XXXX")
        self.assertTrue(changed)

    def test_13_full_replace_empty_replacement(self):
        """Замена на пустую строку"""
        rule = Rule("test", "", full_replace=True)
        result, changed = rule.apply("this is test text test")
        self.assertEqual(result, "this is  text ")
        self.assertTrue(changed)

    def test_14_full_replace_no_change(self):
        """Полная замена без изменений"""
        rule = Rule("missing", "found", full_replace=True)
        result, changed = rule.apply("text without pattern")
        self.assertEqual(result, "text without pattern")
        self.assertFalse(changed)

    def test_15_full_replace_overlap_aaa(self):
        """Перекрывающиеся паттерны 'aaa'"""
        rule = Rule("aaa", "X", full_replace=True)
        result, changed = rule.apply("aaaaaa")
        self.assertEqual(result, "XX")
        self.assertTrue(changed)

    def test_16_full_replace_overlap_aba(self):
        """Перекрывающиеся паттерны 'aba'"""
        rule = Rule("aba", "X", full_replace=True)
        result, changed = rule.apply("abababa")
        self.assertEqual(result, "XbX")
        self.assertTrue(changed)

    def test_17_full_replace_overlap_111(self):
        """Перекрывающиеся паттерны '111'"""
        rule = Rule("111", "X", full_replace=True)
        result, changed = rule.apply("111111")
        self.assertEqual(result, "XX")
        self.assertTrue(changed)

    def test_18_full_replace_overlap_aa(self):
        """Перекрывающиеся паттерны 'aa'"""
        rule = Rule("aa", "X", full_replace=True)
        result, changed = rule.apply("aaaa")
        self.assertEqual(result, "XX")
        self.assertTrue(changed)

    def test_19_single_char_pattern(self):
        """Паттерн из одного символа"""
        rule = Rule("1", "один", full_replace=True)
        result, changed = rule.apply("123141")
        self.assertEqual(result, "один23один4один")
        self.assertTrue(changed)

    def test_20_single_char_full_replace(self):
        """Полная замена одного символа"""
        rule = Rule("a", "A", full_replace=True)
        result, changed = rule.apply("banana")
        self.assertEqual(result, "bAnAnA")
        self.assertTrue(changed)

    def test_21_replacement_longer(self):
        """Замена длиннее паттерна"""
        rule = Rule("a", "long_replacement")
        result, changed = rule.apply("abc")
        self.assertEqual(result, "long_replacementbc")
        self.assertTrue(changed)

    def test_22_replacement_shorter(self):
        """Замена короче паттерна"""
        rule = Rule("longpattern", "short")
        result, changed = rule.apply("longpattern text")
        self.assertEqual(result, "short text")
        self.assertTrue(changed)

    def test_23_replacement_same_length(self):
        """Замена той же длины"""
        rule = Rule("abc", "XYZ")
        result, changed = rule.apply("abcdef")
        self.assertEqual(result, "XYZdef")
        self.assertTrue(changed)

    # ЗАМЕНЕННЫЕ ТЕСТЫ (не сильно поднимают покрытие)
    def test_24_similar_patterns_1(self):
        """Похожий паттерн - почти совпадение"""
        rule = Rule("test", "PASS")
        result, changed = rule.apply("this is testo text")
        # "testo" содержит "test", поэтому замена происходит
        self.assertEqual(result, "this is PASSo text")
        self.assertTrue(changed)

    def test_25_similar_patterns_2(self):
        """Паттерн с дополнительным символом"""
        rule = Rule("hello", "world")
        result, changed = rule.apply("say helloworld")
        # "helloworld" содержит "hello", поэтому замена происходит
        self.assertEqual(result, "say worldworld")
        self.assertTrue(changed)

    def test_26_partial_match(self):
        """Частичное совпадение паттерна"""
        rule = Rule("abcde", "12345")
        result, changed = rule.apply("text with abcd fg")
        # "abcd" не равно "abcde", поэтому замена не происходит
        self.assertEqual(result, "text with abcd fg")
        self.assertFalse(changed)

    def test_27_case_sensitivity(self):
        """Чувствительность к регистру"""
        rule = Rule("Test", "PASS")
        result, changed = rule.apply("this is test text")
        # "test" != "Test" (разный регистр), поэтому замена не происходит
        self.assertEqual(result, "this is test text")
        self.assertFalse(changed)

    def test_28_whitespace_variation(self):
        """Вариация пробелов в паттерне"""
        rule = Rule("hello world", "test")
        result, changed = rule.apply("hello  world")
        # "hello  world" (2 пробела) != "hello world" (1 пробел)
        self.assertEqual(result, "hello  world")
        self.assertFalse(changed)

    def test_29_pattern_larger_than_text(self):
        """Паттерн больше текста"""
        rule = Rule("verylongpattern", "short")
        result, changed = rule.apply("short")
        self.assertEqual(result, "short")
        self.assertFalse(changed)

    def test_30_complex_scenario(self):
        """Сложный сценарий"""
        rule = Rule("cat", "dog", full_replace=True)
        result, changed = rule.apply("The cat caught a caterpillar")
        self.assertEqual(result, "The dog caught a dogerpillar")
        self.assertTrue(changed)



if __name__ == '__main__':


    print("=" * 50)
    print("Запуск тестов...")
    print("=" * 50)

    # Запуск тестов
    unittest.main(verbosity=2)


    def show_coverage():
        """Показать покрытие если установлен coverage"""
        try:
            import coverage
            cov = coverage.Coverage()
            cov.start()

            # Запускаем тесты
            unittest.main(module='test_rule', verbosity=2, exit=False)

            cov.stop()
            cov.save()
            print("\n" + "=" * 50)
            print("ОТЧЕТ О ПОКРЫТИИ:")
            print("=" * 50)
            cov.report()
        except ImportError:
            # Если coverage не установлен, просто запускаем тесты
            unittest.main(verbosity=2)


    if __name__ == '__main__':

        print("=" * 50)
        print("Запуск тестов...")
        print("=" * 50)

        show_coverage()