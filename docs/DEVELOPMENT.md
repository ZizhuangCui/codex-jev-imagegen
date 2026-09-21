# Development and releases / 开发与版本流程

## Current status

- **v0.1.0**: experimental Jev helper and built-in image workflow.
- **v0.2.0**: experimental multi-model connected-tool routing.
- Both are prereleases. Offline CI is evidence about code behavior, not model accuracy or live provider availability.

[Releases](https://github.com/ZizhuangCui/codex-jev-imagegen/releases) · [Milestones](https://github.com/ZizhuangCui/codex-jev-imagegen/milestones) · [Open issues](https://github.com/ZizhuangCui/codex-jev-imagegen/issues)

## Milestone plan / 里程碑

| Target | Outcome and completion gate | Issues |
| --- | --- | --- |
| v0.3.0 | 真实链路验证：Jev、内置生成/编辑、至少一个外部工具均有可复现证据；逐型号标明验证状态。 | #1, #2, #3 |
| v0.4.0 | 受控评测：双语数据集、固定测试划分、同后端 A/B、置信度评估；接受负面结果。 | #4, #5 |
| v1.0.0 | 稳定工作流：安全升级与回滚、公开契约、证据和发布门槛全部完成。 | #6, #7 |

These are scope targets, not promised dates. A milestone completes only when its acceptance gates are met. A blocked credential or missing provider is recorded on the relevant issue, never hidden by a mock run. Standalone API clients are outside the current plan; propose a separate issue if connected tools cannot meet a real requirement.

## Issue and PR lifecycle / 开发过程

1. **Triage**: state the user-visible problem, scope, acceptance criteria, evidence and dependencies. Assign one milestone and a priority. `p0` blocks that milestone; `p1` is planned work. `needs-verification` means required evidence is still missing.
2. **Ready**: dependencies and access requirements are understood. Do not request secrets in issues. Assign an owner only after they accept the work.
3. **In progress**: branch from current `main` as `codex/<issue-number>-<short-description>`. Link the branch/PR to the issue and report concrete blockers there. Avoid unrelated cleanup.
4. **Review**: open a focused PR with the problem, changed behavior, meaningful verification and remaining limitations. Use `Closes #N` only when all issue criteria will be met on merge; otherwise use `Refs #N`.
5. **Done**: merge only after checks and review; close the issue with evidence. For live-verification tasks, green mocked tests alone are insufficient. Remove `needs-verification` only when the required evidence exists.
6. **Release**: publish a version when its documented gate is met, not on every documentation commit. Preserve old tags and release assets.

Issue/PR state is the source of truth; roadmap checkboxes are summaries, not a competing tracker. Use dependencies to sequence work: #1 → #2; #1 + #2 + #4 → #5; #3 is also required if evaluation uses an external route; #1–#6 → #7. Dataset preparation (#4) and safe upgrade work (#6) can proceed independently.

## Version policy / 版本规则

Use `vMAJOR.MINOR.PATCH` tags. Before 1.0, minor releases may change the experimental contract, but must document migrations; patch releases preserve it. After 1.0, incompatible contract changes require a major version, compatible features a minor version, and compatible fixes a patch. Keep prerelease flags until the stable gate passes. A registered model addition never implies live verification.

Maintain [CHANGELOG.md](../CHANGELOG.md): add changes under Unreleased, then move them into the version section when publishing. Source-only documentation changes need no immediate tag. The release archive must contain the skill from the exact tagged commit and must exclude credentials, caches, private runs and local paths.

## Release checklist

- [ ] Milestone/issue acceptance criteria checked against actual evidence; open blockers resolved or scope explicitly revised.
- [ ] Both offline test commands from CONTRIBUTING pass on supported Python versions in GitHub CI.
- [ ] Live evidence linked where required; account access, limitations and untested routes remain explicit.
- [ ] README, support matrix, changelog, migration notes and skill metadata agree.
- [ ] No credentials, private prompts, unlicensed assets or personal paths in the commit/archive.
- [ ] Update `docs/AGENT_LOG.md` before push; record concrete changes, checks and limitations.
- [ ] Tag the reviewed commit, build its archive, publish notes with the correct prerelease/stable status.
- [ ] Verify remote tag, release asset and installability; record the release URL in the release issue.

These are maintainer workflow rules. They are not enforced repository branch protection. Paid live checks remain manual and are not part of public PR CI.
