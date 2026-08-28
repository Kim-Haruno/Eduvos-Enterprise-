import json
from pathlib import Path
from typing import Any, cast

from models.assessment import Assessment
from models.course import Course
from models.learner import Learner
from models.registration import Registration
from monitoring.bugzot import Bugzot
from patterns.factory import SupportTicketFactory
from patterns.singleton import AppConfig
from patterns.strategy import AssessmentCalculator, ClassificationStrategy, PercentageStrategy
from registration.registrationEngine import RegistrationEngine


def loadData(filePath: Path) -> dict[str, Any]:
    with filePath.open(encoding="utf-8") as dataFile:
        data = json.load(dataFile)
    if not isinstance(data, dict):
        raise ValueError("Application data must be a JSON object.")
    return cast(dict[str, Any], data)


def buildRequests(data: dict[str, Any]) -> tuple[list[Learner], list[Course], list[Registration]]:
    learnersByName: dict[str, Learner] = {}
    coursesByName: dict[str, Course] = {}
    requests: list[Registration] = []
    rows = data.get("registrations", [])
    if not isinstance(rows, list):
        raise ValueError("The registrations value must be a list.")
    capacities = data.get("course_capacities", {})
    if not isinstance(capacities, dict):
        raise ValueError("The course_capacities value must be an object.")
    rows = cast(list[Any], rows)
    capacities = cast(dict[str, int], capacities)

    for row in rows:
        if not isinstance(row, list) or len(cast(list[Any], row)) != 4:
            raise ValueError("Each registration must contain four values.")
        row = cast(list[Any], row)
        registrationID, learnerName, courseName, status = row
        learner = learnersByName.get(learnerName)
        if learner is None:
            learner = Learner(
                f"L{len(learnersByName) + 1:03d}",
                learnerName,
                f"{str(learnerName).lower().replace(' ', '.')}@eduvos.example",
            )
            learnersByName[learnerName] = learner
        course = coursesByName.get(courseName)
        if course is None:
            capacity = capacities.get(courseName, len(rows))
            course = Course(f"C{len(coursesByName) + 1:03d}", courseName, capacity)
            coursesByName[courseName] = course
        requests.append(Registration(registrationID, learner, course, status))
    return list(learnersByName.values()), list(coursesByName.values()), requests


def demonstratePatterns(learner: Learner, course: Course) -> None:
    print(f"Singleton shares instance: {AppConfig() is AppConfig()}")
    ticket = SupportTicketFactory.createTicket("technical", "T001", learner, "Unable to access course material")
    print(f"Factory created: {ticket}")
    assessment = Assessment("A001", learner, course, 75)
    percentage = AssessmentCalculator(PercentageStrategy()).calculateResult(assessment.score)
    classification = AssessmentCalculator(ClassificationStrategy()).calculateResult(assessment.score)
    print(f"Strategy results: {percentage}% ({classification})")


def runConsoleDemo(filePath: Path) -> None:
    Bugzot.clearEvents()
    data = loadData(filePath)
    learners, courses, requests = buildRequests(data)
    print("===== EDUVOS ENTERPRISE CONSOLE =====")
    print(f"Loaded {len(learners)} learners and {len(courses)} courses from {filePath.name}")
    if learners and courses:
        demonstratePatterns(learners[0], courses[0])
    engine = RegistrationEngine()
    results = engine.processRequestsConcurrently(requests)
    engine.displaySummary(results)
    Bugzot.displayEvents()
    Bugzot.displayPerformanceReport()


def main() -> None:
    runConsoleDemo(Path(__file__).with_name("eduvos_data.json"))


if __name__ == "__main__":
    main()
