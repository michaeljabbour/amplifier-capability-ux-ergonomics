# UX Ergonomics

Make the next step easier to understand and do.

Watch the [68-second film](https://michaeljabbour.github.io/amplifier-capability-ux-ergonomics/#film): forty mapped fields lost to one failed import, and the route the skill takes to fix the stop where people quit. The example in it is fictional.

An evidence-led UX skill for workflows and human-agent interactions. Trace the real task, find where people can lose their way and turn findings into changes you can verify.

[Explore the site](https://michaeljabbour.github.io/amplifier-capability-ux-ergonomics/) · [Read the method](skills/ux-ergonomics/SKILL.md) · [Install guide](docs/INSTALL.md)

## What you get

- **Find the task behind the screen.** Map decisions, interruptions, errors, recovery and completion instead of beginning with a visual redesign.
- **Make authority understandable.** Show who decides, who acts, what can be stopped and what evidence confirms completion.
- **Give recommendations a fair test.** Separate observation from inference and specify what would pass or fail each consequential change.

## Install and try it

Requires Git and Python 3.11+. Run these commands from a terminal:

```sh
git clone https://github.com/michaeljabbour/amplifier-capability-ux-ergonomics.git
cd amplifier-capability-ux-ergonomics
python3 scripts/capability.py doctor
python3 scripts/capability.py install --dest ~/.agents/skills
```

The installer copies `skills/ux-ergonomics` as a complete folder into your chosen skills parent. Use the discovery path supported by your agent. It starts no service and configures no provider. Restart or refresh skill discovery in your host, then ask:

```text
Use UX Ergonomics to review this fictional batch-import failure flow. The analyst loses entered mappings after an error. Separate observation, inference and recommendation; propose recovery behavior and keyboard/task checks without claiming a measured improvement.
```

If your agent does not discover installed skills, point it directly at the complete folder and ask it to read `SKILL.md`. Reading the method needs no Python runtime. [Installation details](docs/INSTALL.md) cover conflict handling and optional native execution.

## How the work proceeds

1. **Frame and inspect.** Name the actor and task, gather relevant evidence and walk both normal and failure states.
2. **Recommend a concrete change.** Choose the lenses that fit: cognition, accessibility, authority, recovery and visual craft.
3. **Verify at the right level.** Check keyboard and runtime behavior, then use affected-user tasks where the claim needs them.

## Example output

Fictional worked example. It illustrates the intended output; it is not a measured result or a real customer story.

```text
Fictional finding: failed import discards mappings
Observation: inputs disappear after the error
Consequence: task must restart from scratch
Change: preserve mappings; explain retry and cancellation
Acceptance: keyboard user can inspect and retry without re-entry
Evidence gap: affected-user task observation pending
```

## What is checked

Native bundle structure, references and portable installation are checked. No usability study or accessibility-conformance claim is established by those structural checks; each product needs validation on its actual tasks and surfaces. See [validation](docs/VALIDATION.md) for the exact checks and limits.

## Retained implementation and references

[Migration map](docs/MIGRATION.md) records the original source paths and current roles. Primary Git history, native engines, tests, examples, and evaluation assets remain in this checkout. [Native guide](docs/NATIVE-README.md) preserves the original project documentation; old install URLs and runtime claims there are historical and need current verification. [Validation](docs/VALIDATION.md) records actual checks and limits.

[Retained visual references and native adapters](docs/OPTIONAL-CRAFT-ADAPTERS.md) maps the older Taste bundle's creative arsenal, dials, agents and recipes to their actual retained home. The credited references included here are a partial extraction; the native bundle and the authored Taste × Elegance method retain distinct roles.

## Build the site

```sh
python3 scripts/capability.py build
python3 scripts/capability.py check
```

The static site includes a ZIP built from the canonical method, references and license. Runtime and provider setup remain separate from installing the portable method.

## Repository migration

This repository was renamed from `amplifier-skill-ux-ergonomics` to `amplifier-capability-ux-ergonomics`. Existing installed method names, bundle aliases and native interfaces stay the same. See the [migration guide](https://michaeljabbour.github.io/migration/) and [repository map](https://michaeljabbour.github.io/migration/mapping.json) for source URL updates.
