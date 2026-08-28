from models.learner import Learner
from models.course import Course
from models.registration import Registration
from models.assessment import Assessment
from models.supportTicket import SupportTicket
from patterns.singleton import AppConfig
import time
from monitoring.bugzot import Bugzot

print("===== LEARNER =====")

learner1 = Learner(
    "L001",
    "McNeil",
    "NS.2022.W4G8D8@vossie.net"
)

learner1.displayInfo()


print("\n===== COURSE =====")

course1 = Course(
    "C001",
    "Python Enterprise Programming",
    3
)

course1.displayInfo()


print("\n===== REGISTRATION =====")

registration1 = Registration(
    "R001",
    learner1,
    course1
)

registration1.approve()
registration1.displayInfo()


print("\n===== ASSESSMENT =====")

assessment1 = Assessment(
    "A001",
    learner1,
    course1,
    75
)

assessment1.displayInfo()


print("\n===== SUPPORT TICKET =====")

ticket1 = SupportTicket(
    "T001",
    learner1,
    "Unable to access course material"
)

ticket1.displayInfo()

print("\n===== VALIDATION TEST =====")

try:
    invalidLearner = Learner(
        "L999",
        "Invalid User",
        "invalid-email"
    )

except ValueError as error:

    Bugzot.logEvent(
        "VALIDATION",
        "Learner validation failed",
        str(error)
    )

    print("Validation successful:", error)


print("\n===== SINGLETON PATTERN =====")

config1 = AppConfig()
config2 = AppConfig()

config1.displayConfig()

print("Same instance:", config1 is config2)

from patterns.factory import SupportTicketFactory


print("\n===== FACTORY PATTERN =====")

technicalTicket = SupportTicketFactory.createTicket(
    "technical",
    "T002",
    learner1,
    "Computer cannot access the learning platform"
)

registrationTicket = SupportTicketFactory.createTicket(
    "registration",
    "T003",
    learner1,
    "Unable to register for a course"
)

assessmentTicket = SupportTicketFactory.createTicket(
    "assessment",
    "T004",
    learner1,
    "Assessment mark is incorrect"
)

technicalTicket.displayInfo()

print()

registrationTicket.displayInfo()

print()

assessmentTicket.displayInfo()

from patterns.strategy import PercentageStrategy, PassFailStrategy, AssessmentCalculator


print("\n===== STRATEGY PATTERN =====")

percentageCalculator = AssessmentCalculator(
    PercentageStrategy()
)

passFailCalculator = AssessmentCalculator(
    PassFailStrategy()
)

mark = 75

percentageResult = percentageCalculator.calculateResult(mark)
passFailResult = passFailCalculator.calculateResult(mark)

print("Original Mark:", mark)
print("Percentage Strategy:", percentageResult)
print("Pass/Fail Strategy:", passFailResult)

from registration.registrationEngine import RegistrationEngine


print("\n===== REGISTRATION ENGINE =====")

learner2 = Learner(
    "L002",
    "Kulani",
    "EDUV9358610@vossie.net"
)

learner3 = Learner(
    "L003",
    "KIMBERLY",
    "EDUV4826881@vossie.net"
)

learner4 = Learner(
    "L004",
    "Saad",
    "EDUV5048165@vossie.net"
)

learner5 = Learner(
    "L005",
    "Adila",
    "EDUV7023307@vossie.net"
)

learner6 = Learner(
    "L006",
    " Zenande",
    "NS.2022.J4Q6Z9@vossie.net"
)

course2 = Course(
    "C002",
    "Python Enterprise Programming",
    3
)

requests = [
    Registration("R002", learner1, course2),
    Registration("R003", learner2, course2),
    Registration("R004", learner3, course2),
    Registration("R005", learner1, course2),
    Registration("R006", learner4, course2),
    Registration("R007", learner5, course2),
    Registration("R008", learner6, course2),
    Registration("R009", learner2, course2),
    Registration("R010", learner3, course2),
    Registration("R011", learner4, course2)
]

engine = RegistrationEngine()

results = engine.processRequests(requests)

engine.displaySummary(results)

print("\n===== CONCURRENT PROCESSING =====")

concurrentCourse = Course(
    "C003",
    "Concurrent Python Course",
    3
)

concurrentRequests = [
    Registration("CR001", learner1, concurrentCourse),
    Registration("CR002", learner2, concurrentCourse),
    Registration("CR003", learner3, concurrentCourse),
    Registration("CR004", learner4, concurrentCourse),
    Registration("CR005", learner5, concurrentCourse),
    Registration("CR006", learner6, concurrentCourse)
]

concurrentEngine = RegistrationEngine()

startTime = time.time()

concurrentResults = concurrentEngine.processRequestsConcurrently(
    concurrentRequests
)

endTime = time.time()

for result in concurrentResults:
    print(
        f"{result['registrationID']} | "
        f"{result['learner']} | "
        f"{result['status']} | "
        f"{result['result']}"
    )

print("\nConcurrent processing time:",
      round(endTime - startTime, 3), "seconds")

Bugzot.displayEvents()
Bugzot.performanceReport()