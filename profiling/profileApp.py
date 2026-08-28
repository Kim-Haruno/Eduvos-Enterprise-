import cProfile
import pstats
import sys
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from models.course import Course
from models.learner import Learner
from models.registration import Registration
from registration.registrationEngine import RegistrationEngine

def buildProfileRequests() -> list[Registration]:
	course = Course("C-PROFILE", "Profile Course", 10)
	learners = [
		Learner(f"L{i}", f"Learner {i}", f"learner{i}@example.com")
		for i in range(20)
	]
	return [Registration(f"R{i}", learner, course) for i, learner in enumerate(learners)]

def profileRegistrationEngine() -> str:
	profiler = cProfile.Profile()
	profiler.enable()
	RegistrationEngine(maxWorkers=4).processRequestsConcurrently(buildProfileRequests())
	profiler.disable()
	output = StringIO()
	stats = pstats.Stats(profiler, stream=output).sort_stats("cumulative")
	stats.print_stats(15)
	return output.getvalue()

def main() -> None:
	print("===== CPROFILE REGISTRATION REPORT =====")
	print(profileRegistrationEngine())

if __name__ == "__main__":
	main()
