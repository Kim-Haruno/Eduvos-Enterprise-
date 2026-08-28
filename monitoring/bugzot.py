from datetime import datetime
import threading
import time
from typing import Any


class Bugzot:

    events: list[dict[str, Any]] = []
    performanceSamples: list[float] = []
    transactionCounts = {
        "registrations": 0,
        "successes": 0,
        "failures": 0,
    }
    lock = threading.Lock()

    @classmethod
    def logEvent(
        cls,
        eventType: str,
        message: str,
        details: str = "",
        level: str = "INFO",
    ) -> None:
        event = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "level": level.upper(),
            "event_type": eventType,
            "message": message,
            "details": details,
        }
        with cls.lock:
            cls.events.append(event)
            if eventType in {"REGISTRATION", "DUPLICATE", "CAPACITY", "VALIDATION"}:
                cls.transactionCounts["registrations"] += 1
            if eventType == "REGISTRATION":
                cls.transactionCounts["successes"] += 1
            elif eventType in {"DUPLICATE", "CAPACITY", "VALIDATION"}:
                cls.transactionCounts["failures"] += 1

    @classmethod
    def getEvents(cls) -> list[dict[str, Any]]:
        with cls.lock:
            return [event.copy() for event in cls.events]

    @classmethod
    def startTimer(cls) -> float:
        return time.perf_counter()

    @classmethod
    def recordPerformance(cls, operation: str, startTime: float) -> float:
        elapsed = time.perf_counter() - startTime
        with cls.lock:
            cls.performanceSamples.append(elapsed)
        cls.logEvent(
            "PERFORMANCE",
            operation,
            f"Processing time: {elapsed:.6f} seconds",
            level="INFO",
        )
        return elapsed

    @classmethod
    def getPerformanceReport(cls) -> dict[str, float | int]:
        with cls.lock:
            samples = list(cls.performanceSamples)
            counts = dict(cls.transactionCounts)
        totalTime = sum(samples)
        return {
            **counts,
            "sample_count": len(samples),
            "average_time": totalTime / len(samples) if samples else 0.0,
            "min_time": min(samples) if samples else 0.0,
            "max_time": max(samples) if samples else 0.0,
            "throughput": len(samples) / totalTime if totalTime else 0.0,
        }

    @classmethod
    def displayEvents(cls) -> None:
        print("\n===== BUGZOT EVENT LOG =====")
        events = cls.getEvents()
        if not events:
            print("No events recorded.")
            return
        for event in events:
            print(
                f"{event['timestamp']} | {event['level']} | "
                f"{event['event_type']} | {event['message']} | {event['details']}"
            )

    @classmethod
    def displayPerformanceReport(cls) -> None:
        report = cls.getPerformanceReport()
        print("\n===== BUGZOT PERFORMANCE REPORT =====")
        print(f"Transactions: {report['registrations']}")
        print(f"Successful: {report['successes']}")
        print(f"Failures: {report['failures']}")
        print(f"Samples: {report['sample_count']}")
        print(f"Average time: {report['average_time']:.6f} seconds")
        print(f"Minimum time: {report['min_time']:.6f} seconds")
        print(f"Maximum time: {report['max_time']:.6f} seconds")
        print(f"Throughput: {report['throughput']:.2f} operations/second")

    @classmethod
    def clearEvents(cls) -> None:
        with cls.lock:
            cls.events.clear()
            cls.performanceSamples.clear()
            for key in cls.transactionCounts:
                cls.transactionCounts[key] = 0

