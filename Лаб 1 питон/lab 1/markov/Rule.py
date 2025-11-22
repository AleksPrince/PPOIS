class Rule:
    def __init__(self, pattern, replacement, full_replace=False):
        self.pattern = pattern
        self.replacement = replacement
        self.full_replace = full_replace

    def apply(self, text):
        if not self.pattern:
            return text, False
        if self.full_replace:
            return self._apply_full(text)
        else:
            return self._apply_first(text)

    def _apply_full(self, text):
        """Замена всех вхождений."""
        result = []
        i = 0
        changed = False
        n = len(self.pattern)

        while i < len(text):
            if i <= len(text) - n and text[i:i + n] == self.pattern:
                result.append(self.replacement)
                i += n
                changed = True
            else:
                result.append(text[i])
                i += 1
        return ''.join(result), changed

    def _apply_first(self, text):
        """Замена только первого вхождения."""
        index = text.find(self.pattern)
        if index == -1:
            return text, False
        result = text[:index] + self.replacement + text[index + len(self.pattern):]
        return result, True
