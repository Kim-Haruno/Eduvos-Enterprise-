from datetime import datetime
import time


class Bugzot:

    _events = []

    @classmethod
    def logEvent(cls, event_type, message, details=""):
        event = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event_type": event_type,
            "message": message,
            "details": details
        }

        cls._events.append(event)

    @classmethod
    def getEvents(cls):
        return cls._events

    @classmethod
    def displayEvents(cls):
        print("\n===== BUGZOT EVENT LOG =====")

        if not cls._events:
            print("No events recorded.")
            return

        for event in cls._events:
            print(
                f"{event['timestamp']} | "
                f"{event['event_type']} | "
                f"{event['message']} | "
                f"{event['details']}"
            )

    @classmethod
    def clearEvents(cls):
        cls._events.clear()

    @classmethod
    def startTimer(cls):
        return time.perf_counter()

    @classmethod
    def recordPerformance(cls, operation, startTime):
        elapsed = time.perf_counter() - startTime

        cls.logEvent(
            "PERFORMANCE",
            operation,
            f"Processing time: {elapsed:.6f} seconds"
        )

        return elapsed

    @classmethod
    def performanceReport(cls):
        performanceEvents = [
            event for event in cls._events
            if event["event_type"] == "PERFORMANCE"
        ]

        print("\n===== BUGZOT PERFORMANCE REPORT =====")

        print(
            "Performance Events:",
            len(performanceEvents)
        )

        if not performanceEvents:
            print("No performance data recorded.")
            return

        for event in performanceEvents:
            print(
                f"{event['timestamp']} | "
                f"{event['message']} | "
                f"{event['details']}"
            )