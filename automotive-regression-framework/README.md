# Automotive Regression Testing Framework

A portfolio project demonstrating Python-based automated testing and release
quality assurance for a **simulated** automotive monitoring controller.

> Educational project only. This is not a real-time execution platform, a
> production vehicle controller, or safety-certified software.

## Demonstrated skills
- Python OOP, type hints, input validation
- pytest unit, boundary-value, parameterized and regression tests
- Git-based development and CI checks
- JUnit XML and code coverage reports
- Azure Pipelines YAML
- Test planning, defect reporting, and release validation

## Architecture
`test inputs -> VehicleController.evaluate() -> NORMAL/WARNING or validation error`
`Git push / pull request -> CI -> pytest -> JUnit + coverage artifacts`

## Quick start
Python 3.12 or newer is recommended.

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest
```

Run with reports:

```bash
mkdir -p reports
pytest --junitxml=reports/junit-results.xml \
  --cov=vehicle_testing --cov-report=term-missing \
  --cov-report=xml:reports/coverage.xml
```

## Test design
See [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md). The suite covers safe operation,
inclusive threshold boundaries, warning conditions, invalid values, non-finite
numbers, and recovery to safe conditions.

## CI
- GitHub Actions: `.github/workflows/tests.yml`
- Azure Pipelines: `azure-pipelines.yml`

To use Azure Pipelines, push this repository to a GitHub repository, create an
Azure DevOps project, choose **Pipelines → New pipeline → GitHub**, authorize
the repository, and select the existing `azure-pipelines.yml`. Hosted agent
availability depends on your Azure DevOps organization.

## Portfolio evidence to add before publishing
- [ ] Green CI run screenshot/link
- [ ] One intentionally failing test run and explanation
- [ ] Completed example bug report with real reproduction evidence
- [ ] Completed release checklist for a tagged version
- [ ] Actual test count and measured coverage (do not invent metrics)

## Limitations and next steps
This project does not measure hard real-time deadlines or interact with hardware.
Potential extensions: deterministic simulated time steps, fault injection,
test-data files, property-based testing, mutation testing, and a hardware-in-the-
loop adapter interface.
