# Decision contract

Python 3 standard library only. No OpenAI API calls. Examples are illustrative, not measured Jev results.

## Plan input

```json
{
  "user_request": "人物长相不变，改成雨夜街景，镜头拉远。",
  "confirmed_constraints": ["保留人物身份"],
  "reference_images": [
    {"id": "approved-character", "role": "edit_target", "description": "用户批准的人物原图，已由 Codex 查看"}
  ]
}
```

Required: nonempty `user_request`. Optional arrays default to empty. Image roles: `edit_target`, `identity_anchor`, `style_reference`, `supporting_image`. Metadata must reflect actual available images. Paths stay with Codex; Jev receives IDs/descriptions only.

Questions: `intent` = generate/edit/discuss/unknown; `preserve_identity`, `preserve_layout`, `exact_text` = yes/no/unknown. These describe requirements, not successful fulfillment. The script never clears constraints. Original mixed-edit requests remain in the image prompt.

## Review input

Add `visual_report` to the same input:

```json
{
  "output_id": "result-01",
  "observer": "codex",
  "inspected": true,
  "findings": ["背景已改为雨夜，但要求保留的眼镜消失"],
  "uncertainties": ["光照不同，无法确定面部细节是否完全一致"]
}
```

The report must follow actual inspection. `inspected: false` returns fallback without a network call. Never convert missing evidence into a pass. Jev selects `next_action`: accept/edit/regenerate/human_review, using text only. It cannot override observed defects or authorize extra calls.

## Execution

- `--mode request` (default): validated outbound body, no decisions, no network.
- `--mode live`: one HTTPS request, 8-second socket timeout, no retries, no redirects. Does not generate images.
- Fixed model `jev-1.13.0`. Response model is logged; revalidate before upgrading.
- `--min-confidence` defaults to 0.8: an **unvalidated starting value**, not an 80% accuracy promise. Calibrate per question with labeled Chinese requests before automatic routing. The initial helper falls back if any required decision is unknown or below the floor.
- Declared fields only; serialized input at most 24,000 characters. Shorten irrelevant context instead of dropping constraints.
- `status: ok` means schema/threshold checks passed, not semantic correctness. Codex still verifies user intent, locks and available inputs.
- Responses preserve `model`, `answers`, `usage`, `elapsed_ms`, `decision_source`. Validate option sets, finite probabilities and totals. `confidence` is not the same as chosen-option probability.
- `status: fallback` includes a reason. Missing key/error paths do not invent answers; low-confidence or missing-target paths may retain validated answers for diagnosis only. Exception bodies and auth headers are never echoed.
- Exit 0 = prepared request or valid recommendation; 2 = invalid input; 3 = fallback.

Official: [API](https://docs.typesafe.ai/api), [Confidence](https://docs.typesafe.ai/confidence), [Models](https://docs.typesafe.ai/models).
