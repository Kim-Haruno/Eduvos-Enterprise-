from typing import Protocol
class AssessmentStrategy(Protocol):
    def calculate(self, score: float) -> str | float:
        ...
class PercentageStrategy:
    def calculate(self, score: float) -> float:
        return score
class ClassificationStrategy:
    def calculate(self, score: float) -> str:
        return "Pass" if score >= 50 else "Fail"
class AssessmentCalculator:
    def __init__(self, strategy: AssessmentStrategy) -> None:
        self.strategy = strategy
    def calculateResult(self, score: float) -> str | float:
        return self.strategy.calculate(score)
