# Release Validation Checklist

## Candidate details
- Version:
- Commit:
- Date:
- Validator:

## Pre-release
- [ ] Change list and linked issues reviewed
- [ ] Scope and known limitations documented
- [ ] Dependencies install in a clean environment
- [ ] Full regression suite executed
- [ ] No unexpected test failures
- [ ] Test report and coverage report archived
- [ ] Defects triaged and release blockers resolved

## Patch validation
- [ ] Defect reproduction test added
- [ ] Test fails against the affected revision
- [ ] Fix applied and reproduction test passes
- [ ] Full regression suite passes after fix
- [ ] Diff reviewed for unintended changes

## Decision
- [ ] PASS — evidence supports release
- [ ] FAIL — release blocked pending investigation

Reason/evidence:
[Link to CI run, report artifact, and relevant commit.]

Note: A green suite is evidence of the checks performed, not a guarantee of
safety or correctness in a real vehicle.
