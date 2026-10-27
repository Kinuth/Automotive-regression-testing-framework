# Architecture Overview — Automotive Regression Testing Framework

This document describes the software design, execution flow, automated testing architecture, and continuous integration pipeline for the Automotive Regression Testing Framework.

---

## 1. System Architecture

The framework consists of a domain-modeled vehicle monitoring controller and a multi-tiered automated verification suite.

```mermaid
flowchart TD
    subgraph SUT["System Under Test: vehicle_testing"]
        CFG["ControllerConfig\n(min/max speed, min/max temp)"]
        VC["VehicleController"]
        VAL["Validation Engine\n• Type check\n• Finiteness check\n• Domain bounds"]
        EVAL["Threshold Evaluator\n• Inclusive upper bounds\n• Warning trigger"]
        STATE["ControllerState\n(NORMAL / WARNING)"]
        
        CFG --> VC
        VC --> VAL
        VAL -->|Valid Readings| EVAL
        VAL -->|Invalid Readings| ERR["Raise TypeError / ValueError"]
        EVAL --> STATE
    end

    subgraph Inputs["Sensor Signal Inputs"]
        SPD["speed_kmh (float)"]
        TMP["temperature_c (float)"]
        SPD --> VC
        TMP --> VC
    end
```

### Component Details
1. **`ControllerState`**:
   - Enumeration of legal operational monitoring states: `NORMAL` (`"normal"`) and `WARNING` (`"warning"`).
2. **`ControllerConfig`**:
   - Immutable frozen dataclass encapsulating physical sensor constraints and operational thresholds.
   - Self-validating in `__post_init__`: guarantees finite numbers, rejects boolean types, and enforces `min_speed_kmh >= 0.0`, `min_speed_kmh < max_speed_kmh`, and `min_temperature_c < max_temperature_c`.
3. **`VehicleController`**:
   - Encapsulates domain logic.
   - `_require_finite_number(name, value)`: Strictly validates numeric type (explicitly rejecting Python `bool`) and ensures non-NaN, non-infinite values.
   - `evaluate(speed_kmh, temperature_c)`: Deterministically compares inputs against configured boundaries. Upper limits are inclusive safe bounds.

---

## 2. Evaluation Data Flow

```mermaid
sequenceDiagram
    autonumber
    actor Caller as Test Suite / Diagnostic Caller
    participant VC as VehicleController
    participant VAL as Validation Engine
    participant CFG as ControllerConfig

    Caller->>VC: evaluate(speed_kmh, temperature_c)
    VC->>VAL: _require_finite_number("speed_kmh", speed_kmh)
    alt Non-numeric or bool or NaN/Inf
        VAL-->>Caller: raise TypeError / ValueError
    end

    VC->>VAL: _require_finite_number("temperature_c", temperature_c)
    alt Non-numeric or bool or NaN/Inf
        VAL-->>Caller: raise TypeError / ValueError
    end

    VC->>CFG: Check lower limits (min_speed_kmh, min_temperature_c)
    alt Reading below minimum valid domain
        VC-->>Caller: raise ValueError
    end

    VC->>CFG: Compare upper limits (max_speed_kmh, max_temperature_c)
    alt speed_kmh > max_speed_kmh OR temperature_c > max_temperature_c
        VC-->>Caller: ControllerState.WARNING
    else Within safe limits
        VC-->>Caller: ControllerState.NORMAL
    end
```

---

## 3. Automated Testing Architecture

The verification suite is structured to guarantee full requirement coverage, boundary protection, and regression immunity:

```mermaid
graph LR
    subgraph TestSuite["Automated Regression Suite (pytest)"]
        T1["Functional Tests\n(REQ-001, REQ-002)"]
        T2["Boundary-Value Analysis\n(REQ-001, REQ-002, REQ-003)"]
        T3["Negative & Type Tests\n(REQ-003, REQ-004)"]
        T4["Warning Independence\n(REQ-005)"]
        T5["Configuration Validation\n(REQ-006, REQ-007)"]
        T6["Regression Tests\n(REG-001 / BUG-001, REG-002)"]
    end

    subgraph Artifacts["Test & Quality Artifacts"]
        JUNIT["reports/junit-results.xml"]
        COV["reports/coverage.xml"]
        STDOUT["Console Summary & Missing Lines"]
    end

    TestSuite --> JUNIT
    TestSuite --> COV
    TestSuite --> STDOUT
```

---

## 4. Continuous Integration Pipeline Workflow

```mermaid
flowchart TD
    subgraph GitHubActions["GitHub Actions Workflow (.github/workflows/tests.yml)"]
        TRIGGER["Trigger: Push or PR to main"]
        CHECKOUT["1. Check out repository source"]
        PYTHON["2. Set up Python matrix (3.12, 3.13)"]
        INSTALL["3. Install package & dependencies (.venv)"]
        RUN["4. Run pytest with branch coverage & JUnit XML"]
        UPLOAD["5. Upload test artifacts (reports/)"]

        TRIGGER --> CHECKOUT --> PYTHON --> INSTALL --> RUN --> UPLOAD
    end
```

Both GitHub Actions and Azure DevOps execute this test and report-generation sequence, providing automated verification across supported Python environments.
