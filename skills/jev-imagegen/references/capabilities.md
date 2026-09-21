# Built-in image_gen and model families

Verified 2026-09-21. Capability design only; model-specific API adapters are not implemented or authorized by selecting this skill.

## Current executable path

User explicitly selected **Codex built-in image_gen**, not an independent OpenAI API application. The skill passes a prompt and actual references through the tool schema. There is no model selector, `quality`, `steps`, `seed`, attention ratio, or intermediate latent access in the current tool. Do not invent those fields or try to set them through prose.

Official [Codex image documentation](https://learn.chatgpt.com/docs/image-generation) currently describes built-in generation as using `gpt-image-2`. The runtime tool itself does not expose a choice or guarantee a model identity in every result. Record the model as unreported unless returned; distinguish documentation from observed metadata. Calling this skill's first release “v1” does not mean the model is `gpt-image-1`.

## Preserve the requested family coverage

| Family | Official API ID | Design treatment |
| --- | --- | --- |
| Gen1 | `gpt-image-1` | Base task contract: text-to-image, reference/edit inputs, explicit invariants. Keep this simple generation/edit loop as the conceptual starting point. No Gen1-specific API call in this release. |
| Gen2 | `gpt-image-2` | Same task contract; API supports additional size controls. Built-in selection stays platform-managed. |
| Gen2.5 | `gpt-image-2.5-sunburst`, `gpt-image-2.5-flare` | Official docs position Sunburst for precise editing and Flare for fast everyday generation. These are distinct model IDs, not an assumed `gpt-image-2.5` alias. |
| Seedream 5.0 Pro | `doubao-seedream-5-0-pro-260628` (Volcengine Ark release listing) | External image provider, not a Codex built-in model. Reuse text generation/edit intent, references and invariants; adapter and live access remain pending. |

The reusable information is `user_request`, reference roles, preserve/change requirements, exact text and visual findings. Keep provider parameters outside this business state. If future tools expose explicit selectors, add only the verified mappings then, without rewriting decision questions. Today, do not silently upgrade models or route between these families.

If the user later requests an independent API app: first resolve credentials and permitted model, then follow current official API docs and model availability. Preserve user-specified Gen1 even if newer models exist; explain access/deprecation issues if encountered rather than silently substituting.

Primary sources:

- [GPT Image 1](https://developers.openai.com/api/docs/models/gpt-image-1)
- [GPT Image 2](https://developers.openai.com/api/docs/models/gpt-image-2)
- [GPT Image 2.5 Sunburst](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst)
- [GPT Image 2.5 Flare](https://developers.openai.com/api/docs/models/gpt-image-2.5-flare)
- [Image-generation tool](https://developers.openai.com/api/docs/guides/tools-image-generation)

## Seedream 5.0 Pro extension

Added at the user's request. The official Volcengine release listing identifies this model and describes text-to-image, single/multiple-reference generation and interactive editing. Treat location/marker editing as provider-specific capabilities; do not assume they share the built-in image_gen schema.

Design path: the same Jev plan → Codex prompt/reference preparation → **external Seedream adapter** → actual image inspection → optional Jev repair recommendation. The adapter is not implemented in this release. Keep `provider`/model settings in the execution layer rather than sending unsupported fields to `decide.py`.

Before implementation, resolve the actual service (Volcengine Ark, BytePlus, or the user's existing provider), account access, exact model ID, image upload contract and billing. Do not assume credentials/model names or parameters are interchangeable across services. Seedream usage requires that provider's access and billing, not Codex's built-in image entitlement. Preserve an explicit Seedream selection even when unavailable; never silently substitute another model.

Verification limit: the official release listing was searchable, but the tutorial body was not exposed by the documentation fetcher. Reference-image count, exact sizes, layer export, seed support, endpoint payload and prices are not hard-coded here until verified for the chosen provider. Third-party model listings are not treated as ByteDance's official API contract.

- [Volcengine official model releases](https://docs.volcengine.com/docs/ark/model-release-announcement?lang=zh)
- [BytePlus Seedream 5.0 Pro tutorial](https://docs.byteplus.com/en/docs/ModelArk/2582774)
- [BytePlus interactive editing guide](https://docs.byteplus.com/en/docs/ModelArk/2582775)

The currently implemented built-in interface exposes no per-layer attention control; no such control has been verified for Seedream. “Improve end-to-end completion by reducing wrong routes or rework” remains a hypothesis to measure, distinct from inference acceleration.
