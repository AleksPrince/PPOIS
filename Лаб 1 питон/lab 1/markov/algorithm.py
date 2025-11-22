

from rule import Rule

class MarkovAlgorithm:
    def __init__(self, rules):
        self.rules = rules

    def run(self, input_text):
        text = input_text
        while True:
            changed = False
            for rule in self.rules:
                new_text, did_change = rule.apply(text)
                if did_change:
                    text = new_text
                    changed = True
                    if not rule.full_replace:
                        return text
                    break
            if not changed:
                break
        return text

