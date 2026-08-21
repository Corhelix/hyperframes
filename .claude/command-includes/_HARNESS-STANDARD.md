# _HARNESS-STANDARD — verification scripts are artefacts, not scratch

<!-- Include, not a command. v0.1 2026-08-21. A COMMON EXPECTATION, like _VERIFICATION-STANDARD.md:
     no department owns "write a probe that proves it". Referenced by /goal-build, /build,
     /review, /audit-cto. Reference implementation, read it before writing a new probe:
     CLEAN/capital-works-experience/harness/ (14 scripts, logs and captures under harness/out/). -->

A run that verifies by hand leaves nothing behind. A run that writes a probe leaves something the next run, the next feature and the next person can execute. So every check that can be a script becomes one, the script is committed, and the next run reuses it rather than rewriting it.

**Reuse before writing.** Read the harness directory first. Most verification needs are one of a dozen recurring shapes, and the second version of a probe is nearly always worse than the first, because the first was written while the problem was fresh.

## Where things live

```
harness/                     the probes, committed, one file per thing proved
harness/fixtures/            sample inputs so probes can self-test without a full run
harness/out/<area>/          logs and captures each run writes; evidence, not source
```

Evidence written by a probe follows the naming law in `_GOAL-BUILD-TEMPLATES.md`. Source is committed; `out/` is not, unless a specific capture is cited as evidence for an acceptance check.

## The contract every probe obeys

**Header first.** Three things, before any code: what it proves and which acceptance check it answers, exactly how to run it, and what its exit codes mean. A probe whose purpose has to be inferred from its body is a probe nobody will reuse.

**Exit codes are a three-way contract.** `0` pass. `1` fail, naming what failed. `2` misconfigured — missing env, no credentials, unreachable service. The third is not decoration: without it a broken probe reads as a passing product, which is the most dangerous outcome verification can produce. Check configuration and exit `2` before touching the system under test.

**Probes must not be vacuous.** A check passes trivially far more often than people expect. "The signed-out client sees zero rows" is satisfied by a table that is simply empty. So seed the condition that makes a pass meaningful, then assert, then clean up. State the seeding in the header so the next reader can see the probe has teeth.

**Assert the negative, both ways.** Proving a boundary holds means showing the forbidden action was refused *and* that the thing it targeted survived. An unauthorised delete that appears blocked but silently succeeded looks identical to a pass from one side.

**The pass message is evidence.** Print the numbers observed, not the word PASS: *"1 row seeded by operator; anon read 0 rows; anon delete blocked; row cleaned up"*. A bare PASS asserts; a counted PASS proves, and it is what gets pasted into the ledger.

**Clean up, and say so.** A probe leaves the system as it found it, and its output states what it created and removed. Anything it could not clean up is named, because an unnoticed leftover becomes the next run's phantom defect.

**Secrets come from the environment and are never printed.** Source them, use them, never echo them, never write them to `out/`.

**Fixtures make the harness self-testable.** A generator that builds a known-good sample lets every probe be exercised without a full model run, which is how you find out the probe is broken rather than the product.

## The recurring probe types

These are the shapes that keep reappearing. Name a new probe after the one it resembles.

| Type | Proves | Lens |
|---|---|---|
| Environment / account setup | the run has a usable identity to test as | prerequisite |
| Server start with secrets | the thing under test is actually running | prerequisite |
| Journey walk in a real browser | a person can complete the job end to end, with a capture per step | 3 |
| Surface and state capture | every reachable state renders correctly at each viewport | 2 |
| Artefact validation | the emitted file, export or payload is self-contained and well-formed | 2 |
| Data truth probe | what the store actually holds after the action, as the user's own scope sees it | 2 |
| Isolation probe | one account's data is invisible and untouchable to another | adversarial |
| Gate / lock probe | a state that should refuse writes actually refuses them | adversarial |
| Link and navigation walk | nothing dead-ends, every route resolves to the page it claims | 2 |
| Performance and accessibility audit | the stated budget and standard are met, per page | 2 |
| Fixture generator | the harness itself can be tested without the product | meta |

## When a probe cannot exist

Some checks are irreducibly human: does this read well, is this the right decision, does the tone fit. Those stay walkthrough steps in `ACCEPTANCE.md` with their evidence captured by hand. The test is whether a machine could decide it, not whether writing the script would be convenient.
