# Evaluation plan

Status: no live model evaluation has been completed. Offline tests verify software behavior only.

## Isolate the decision source

Compare A: the same skill with Codex decisions, versus B: the same skill with Jev decisions. Keep the image backend, reference assets, user request, prompt-compilation rules and call budgets constant. Evaluate Seedream separately once its adapter exists; changing the generator and decision source simultaneously cannot isolate Jev's contribution.

Use permission-cleared tasks spanning new images, identity-preserving edits, layout-preserving edits, exact text, mixed changes, missing references and discussion-only requests. Include Chinese, English and mixed-language requests. Split by conversation into a tuning set and a held-out set.

## Report per run

- Decision source, Jev model/version and question version.
- Actual image backend, or `unreported` when unavailable.
- Task type, input/reference roles and confirmed constraints.
- Jev elapsed time, image-call time and end-to-end time separately.
- Number of Jev and image calls; all fallbacks and failures.
- Which requirements were satisfied, violated or not assessable.
- Actual token usage; cost only when usage and applicable pricing are known.

Do not publish private prompts or images. A public report can use aggregate results and permission-cleared examples.

## Interpret results

Interleave arms and repeat tasks because the built-in image tool has no seed control. Report the number of runs and variability, not just the best image. Use independent or blinded human assessment where practical. Identity similarity, literal text and layout preservation require separate judgments.

Tune thresholds on the tuning set, then freeze them for the held-out set. Report both correctness among accepted decisions and the fraction of requests accepted. Calibrated-looking confidence is not proof of calibrated correctness in this domain.

The feature is useful when it reduces rework or total task cost/time without an unacceptable quality loss. Better end-to-end time does not demonstrate faster image-model inference. No result should inherit the reference project's 41.7% claim.
