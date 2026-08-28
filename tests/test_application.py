import pytest

from main import buildRequests
from models.assessment import Assessment
from models.course import Course
from models.learner import Learner
from models.registration import Registration
from models.support_ticket import SupportTicket
from monitoring.bugzot import Bugzot
from patterns.factory import AcademicTicket, SupportTicketFactory
from patterns.singleton import AppConfig
from patterns.strategy import AssessmentCalculator, ClassificationStrategy, PercentageStrategy
from registration.registrationEngine import RegistrationEngine


@pytest.fixture(autouse=True)
def clear_monitoring() -> None:
    Bugzot.clearEvents()


def make_learner(number: int = 1) -> Learner:
    return Learner(f"L{number}", f"Learner {number}", f"learner{number}@example.com")


def test_domain_relationships_and_defaults() -> None:
    learner = make_learner()
    course = Course("C1", "Python", 2)
    registration = Registration("R1", learner, course)
    assessment = Assessment("A1", learner, course, 75)
    ticket = SupportTicket("T1", learner, "Access issue")

    assert registration in learner.registrations
    assert registration in course.registrations
    assert registration.status == "Pending"
    assert assessment.result == "Pass"
    assert ticket.status == "Open"


@pytest.mark.parametrize("email", ["invalid", "a@", "@example.com", "a b@example.com"])
def test_invalid_email_is_rejected(email: str) -> None:
    with pytest.raises(ValueError):
        Learner("L1", "Learner", email)


def test_invalid_fields_are_rejected() -> None:
    with pytest.raises(ValueError):
        Course("C1", "Python", 0)
    with pytest.raises(ValueError):
        Assessment("A1", make_learner(), Course("C1", "Python", 1), 101)
    with pytest.raises(ValueError):
        Registration("R1", make_learner(), Course("C1", "Python", 1), "Unknown")


def test_registration_engine_rejects_duplicate_and_capacity() -> None:
    course = Course("C1", "Python", 1)
    first = Registration("R1", make_learner(1), course)
    duplicate = Registration("R2", first.learner, course)
    full = Registration("R3", make_learner(3), course)
    results = RegistrationEngine().processRequests([first, duplicate, full])

    assert [result["status"] for result in results] == ["Approved", "Rejected", "Rejected"]
    assert len(course.registeredLearners) == 1
    assert {event["event_type"] for event in Bugzot.getEvents()} >= {
        "REGISTRATION",
        "DUPLICATE",
        "CAPACITY",
    }


def test_concurrent_processing_preserves_capacity() -> None:
    course = Course("C1", "Python", 3)
    requests = [
        Registration(f"R{i}", make_learner(i), course)
        for i in range(1, 11)
    ]
    results = RegistrationEngine(maxWorkers=4).processRequestsConcurrently(requests)

    assert sum(result["status"] == "Approved" for result in results) == 3
    assert len(course.registeredLearners) == 3


def test_build_requests_uses_explicit_course_capacities() -> None:
    data = {
        "course_capacities": {"Python": 1},
        "registrations": [["R1", "Learner", "Python", "Pending"]],
    }

    learners, courses, requests = buildRequests(data)

    assert len(learners) == 1
    assert courses[0].capacity == 1
    assert requests[0].status == "Pending"


def test_monitoring_report_counts_registration_outcomes() -> None:
    course = Course("C1", "Python", 1)
    requests = [
        Registration("R1", make_learner(1), course),
        Registration("R2", make_learner(2), course),
    ]

    RegistrationEngine().processRequests(requests)
    report = Bugzot.getPerformanceReport()

    assert report["registrations"] == 2
    assert report["successes"] == 1
    assert report["failures"] == 1
    assert report["sample_count"] == 2


def test_assessment_strategies() -> None:
    assert AssessmentCalculator(PercentageStrategy()).calculateResult(72.5) == 72.5
    assert AssessmentCalculator(ClassificationStrategy()).calculateResult(49) == "Fail"
    assert AssessmentCalculator(ClassificationStrategy()).calculateResult(50) == "Pass"


def test_factory_and_singleton_patterns() -> None:
    ticket = SupportTicketFactory.createTicket("academic", "T1", make_learner(), "Help")
    assert isinstance(ticket, AcademicTicket)
    assert AppConfig() is AppConfig()