class PercentageStrategy:
    def calculate(self, mark):
        return mark


class PassFailStrategy:
    def calculate(self, mark):
        if mark >= 50:
            return "Pass"
        else:
            return "Fail"


class AssessmentCalculator:
    def __init__(self, strategy):
        self.strategy = strategy

    def calculateResult(self, mark):
        return self.strategy.calculate(mark)