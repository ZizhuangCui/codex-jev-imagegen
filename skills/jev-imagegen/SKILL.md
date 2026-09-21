---
name: jev-imagegen
description: Use Jev to classify image requests and choose bounded repair actions, then use Codex built-in image_gen or a connected GPT Image, Nano Banana, or Seedream tool to generate or edit images. Apply to Jev-assisted image creation, editing, or comparison against the same workflow without Jev. Does not modify model attention or denoising internals.
---

# Jev + Codex image generation

Deliver actual images through the built-in `image_gen` tool by default, or a verified connected tool for an explicitly selected model. Jev supplies text-based decisions; Codex understands references, compiles prompts, inspects results, and executes tool calls. Model selection and tool availability are checked separately from Jev decisions.

## Capability boundary

- Read the available `imagegen` skill before actual generation. The current tool schema is authoritative: in this environment it supports `prompt`, `referenced_image_paths`, and `num_last_images_to_include`. It has no model selector, attention keep ratios, seeds, quality flags, masks, or sampler callbacks.
- Default to built-in image generation. Do not silently switch to OpenAI API/CLI or ask for an OpenAI API key for this path. Jev requires its own `TYPESAFE_API_KEY`; read the process environment by default. If the user identifies a secret file, load it without printing secrets; never execute an env file as shell code.
- Support GPT Image 1 / 1 mini / 1.5 / 2 / 2.5 Sunburst / 2.5 Flare; Nano Banana / Pro / 2 / 2 Lite; and Seedream 4.0 / 4.5 / 5.0 / 5.0 Lite / 5.0 Pro through **connected-tool routing**. The catalog is not proof that those tools are installed. Read [providers.md](references/providers.md) and use `scripts/route.py` against a fresh observed tool inventory before generation. No external HTTP adapters are bundled.
- Exact model selection requires a tool whose schema or fixed-model contract establishes that model. The built-in tool cannot satisfy an explicit Gen1/2/2.5 selection merely by putting the name in the prompt. Do not label output with an unreported model. Read [capabilities.md](references/capabilities.md) for version IDs and sources. Ambiguous Image 2.5 requires choosing Sunburst or Flare; never silently substitute providers or versions.
- Jev cannot inspect pixels. After generation it can evaluate a factual visual report from Codex or another actual image observer. It does not certify identity preservation.

## Before generation

1. Preserve the exact request and confirmed constraints. Distinguish style references from edit targets. Inspect local inputs with `view_image`. Screenshots supplied as technical references are not image-edit targets.
2. For edits, retain the user-approved canonical image as the identity/reference anchor separately from the latest output. Only an explicit user change can release a confirmed constraint.
3. Prepare compact JSON using [contract.md](references/contract.md): raw request, relevant constraints and image-role descriptions. Do not send image bytes, local paths, credentials, chat dumps, or an already-decided route to Jev.
4. Run `scripts/decide.py --phase plan --input <json> --mode live`. It makes one network attempt, returns advice, and never invokes image generation.
5. If `status` is not `ok`, use Codex's normal interpretation and record `decision_source: codex_fallback` and the reason. Never fabricate Jev answers. If a live Jev comparison is specifically required, mark that arm blocked until credentials/network are available rather than substituting a baseline result.
6. Check even high-confidence advice against explicit user intent and real inputs. `discuss` must not trigger generation; editing needs an actual target. Unknown decisions never clear existing locks. Ask only about ambiguity that materially blocks the task.
7. Compile a short image prompt with the actual request, image roles, required changes, unchanged elements and verbatim text. Do not add invented creative requirements or probability scores.

## Generate, observe, repair

1. Resolve the selected model/tool using [providers.md](references/providers.md). If blocked, stop without switching models. Invoke the resolved tool once per requested asset, following its actual schema and provider skill. For the built-in path: Use `referenced_image_paths` when all needed images have local paths; otherwise use the smallest `num_last_images_to_include` covering them, within the tool limit. Never set both. If required references cannot all be included, ask for the missing images instead of silently omitting them.
2. Wait for completion and save the returned file non-destructively into the user's destination, or `output/jev-imagegen/<unique-run>/`. Never resubmit while the first call's outcome is unknown.
3. Inspect the actual output against the request and anchors. Record `output_id`, `observer`, `inspected`, `findings`, `uncertainties`. Findings name affected areas and requested constraints. Do not invent numeric similarity scores.
4. If the image meets observable requirements, deliver without another Jev call. If a defect exists and a repair decision would help, call `decide.py --phase review` with the visual report. It selects `accept`, `edit`, `regenerate`, or `human_review` using text only.
5. Codex must reject an `accept` recommendation when observed requirements remain unmet. A probability is not a quality certificate. Preserve canonical references during repairs and use the current result as the edit target when appropriate.
6. Default ceiling per asset: one initial image call plus one targeted repair; one plan and at most one review Jev call. A ceiling is not a quota. Stop with the best actual result and remaining issue after the ceiling unless more iterations were authorized. Respect user-specified batch totals and budgets.

## Evidence and comparison

Save the request, locks, requested model, selected tool, reported model metadata (or null), actual tool arguments, decision JSON, visual report, output paths, call counts and elapsed times in the run directory. Never persist a key. Cost is unknown when usage/pricing is unavailable.

For requested A/B tests, compare the same skill and prompt-compiler rules with Codex decisions versus Jev decisions. Match assets, constraints and call budgets. The built-in tool lacks a seed control; repeat and report variation instead of claiming matched seeds. Separate end-to-end time, image-call time, Jev overhead, attempts and defects. Fewer retries do not prove faster model inference; the reference repository's 41.7% figure is not our performance.

Read [research.md](references/research.md) when explaining the reference audit. Do not install or execute that GPU repository to use this skill.

## Helper

Resolve paths relative to this skill's installation directory:

```sh
python3 scripts/decide.py --phase plan --input /absolute/path/request.json --mode request
python3 scripts/decide.py --phase plan --input /absolute/path/request.json --mode live
python3 scripts/test_decide.py
```

`request` validates and prints the outbound request without contacting Jev; it is not a simulated decision. `live` reads `TYPESAFE_API_KEY` and contacts only the official HTTPS endpoint. Missing keys/errors produce an explicit fallback. See the contract for schema, exit codes and unvalidated thresholds.
