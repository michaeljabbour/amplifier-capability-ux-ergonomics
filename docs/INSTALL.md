# Install UX Ergonomics

## Portable method

Requires Git and Python 3.11+. From a terminal:

```sh
git clone https://github.com/michaeljabbour/amplifier-capability-ux-ergonomics.git
cd amplifier-capability-ux-ergonomics
python3 scripts/capability.py doctor
python3 scripts/capability.py install --dest ~/.agents/skills
```

The destination is the parent of the `ux-ergonomics` folder. Select your host’s supported skills location. Refresh skill discovery, or point your agent at the complete installed folder and ask it to read `SKILL.md`.

Try this first:

```text
Use UX Ergonomics to review this fictional batch-import failure flow. The analyst loses entered mappings after an error. Separate observation, inference and recommendation; propose recovery behavior and keyboard/task checks without claiming a measured improvement.
```

## Install behavior and optional execution

Run `python3 scripts/capability.py doctor`, then `python3 scripts/capability.py install --dest <your-host-skills-parent>`. The destination must be the parent of the installed `ux-ergonomics` folder. The command refuses conflicting content; inspect it before choosing `--replace`, which retains a dated backup. Repeating an identical install is idempotent. Remove only that installed folder to uninstall; no global service is installed.

The portable method requires no engine, provider credential, Memory service, or background process. Native runtime instructions are retained in [the native guide](NATIVE-README.md), with their original dependencies and limitations. Check the actual host/version/permissions before execution. A method doctor result is not runtime health or model quality evidence.

The previous native document is preserved in [NATIVE-INSTALL.md](NATIVE-INSTALL.md), including its historical evidence and limits.