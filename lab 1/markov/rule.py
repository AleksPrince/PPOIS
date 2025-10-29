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