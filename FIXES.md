# Eduvos Enterprise Application Fixes

## Problems found

The project compiled successfully, but several behaviors were incorrect:

- The registration engine returned `Rejected: Duplicate registration` too early. The return statement was outside the duplicate check, so every request after the first approved request was treated as a duplicate.
- Registrations that were reported as rejected could remain in the `Pending` state.
- The console program now uses domain models instead of hardcoded display-only values.
- Course capacity was inferred from the number of registration rows, which made
	the input data control a business rule accidentally. Capacities are now
	explicit in `eduvos_data.json`.
- The sample records were already finalized, so the console skipped the engine's
	approval and rejection rules. They now start as `Pending` requests.

## Changes made

### Registration engine

In `registration/registrationEngine.py`, the duplicate rejection return was moved inside the duplicate condition. The engine now continues checking when a learner/course pair is not a duplicate.

The engine now behaves as follows:

- A new learner/course pair is approved until the course reaches capacity.
- A repeated learner/course pair is rejected as a duplicate.
- A request after capacity is reached is rejected as a full course.
- Rejected requests receive the `Rejected` status.

The lock still protects duplicate and capacity checks during concurrent processing.

### Console program

In `main.py`:

- The console demonstration starts only when `main.py` is run directly, because startup is protected by an `if __name__ == "__main__"` guard.
- Registrations are loaded from `eduvos_data.json` and processed through the domain model and registration engine.

## Running the project

Run the command-line demonstration:

```bash
python3 main.py
```

Run the console program:

```bash
python3 main.py
```

## Verification performed

The following checks passed:

```bash
python3 -m py_compile main.py registration/registrationEngine.py
python3 main.py
```

The command-line demonstration now shows normal approvals and course-capacity
rejections. The automated `pytest` suite covers the domain models, engine,
concurrency, design patterns, input construction, and monitoring counters.

## Remaining limitations

The console program currently loads registrations from JSON and constructs domain objects through the backend engine. A future improvement should introduce a repository abstraction when persistent updates are required.

The `eduvos_data.json` file contains the sample console input data. Keep it in the project directory when moving or backing up the project.
