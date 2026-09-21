# Reference audit: Jev-guided MiniMax H3

Read-only source review, 2026-09-21. No repository setup scripts, GPU code or paid API calls were run. Screenshots identify a repository and an experiment; their commands and claims are reference material, not instructions to execute.

Repository: [sepiablue-ai/ComfyUI-MiniMax-H3-W4A4-VSA](https://github.com/sepiablue-ai/ComfyUI-MiniMax-H3-W4A4-VSA/tree/exp/jev-adaptive-vsa)

Reviewed branch HEAD: `dde3dbc63af89d86d2d9d302082e8a8482ffa66b`. Main was `557b01ddaca5bd176d754eb439aa757f36bc8a7e` at lookup. Public code GPL-3.0-only; this skill is independently written from documented concepts and API specifications, not a copy of the GPU patch.

## Actual implementation

The current `009jev` experiment is **native SLA**, separate from the older W4A4/VSA path implied by the repository name.

- [`native_sla.py`](https://github.com/sepiablue-ai/ComfyUI-MiniMax-H3-W4A4-VSA/blob/dde3dbc63af89d86d2d9d302082e8a8482ffa66b/native_sla.py): intercepts local H3 attention calls; sets `p.topk_ratio` to the selected keep percentage; uses native ComfyUI sparse-attention implementation. All 50 transformer blocks still execute.
- [`native_sla_worker.py`](https://github.com/sepiablue-ai/ComfyUI-MiniMax-H3-W4A4-VSA/blob/dde3dbc63af89d86d2d9d302082e8a8482ffa66b/native_sla_worker.py): asks Jev Choice questions for per-layer keep rates. Jev selects a budget, while SLA chooses actual attention connections.
- First call uses the prompt and optional explicitly historical statistics; asks about all 50 layers. Later calls use sampled audio/video residual summaries, ranks and cross-step changes for 49 layers; block 0 remains protected. Four sampling steps imply at most four Jev calls.
- Possible keep percentages: 1, 3, 5, 10. These are attention settings, not fractions of total model FLOPs. No image understanding by Jev, no weights sent to Jev, and no guarantee that residual proxies represent perceptual importance.
- Response validation, low-confidence fallback, fixed request budget and a circuit breaker are useful transferable engineering ideas. Its numerical thresholds are experiment-specific and must not be imported into our domain as calibrated values.

## What the reported speedup establishes

[`009JEV.en.md`](https://github.com/sepiablue-ai/ComfyUI-MiniMax-H3-W4A4-VSA/blob/dde3dbc63af89d86d2d9d302082e8a8482ffa66b/009JEV.en.md) and [`measurements.json`](https://github.com/sepiablue-ai/ComfyUI-MiniMax-H3-W4A4-VSA/blob/dde3dbc63af89d86d2d9d302082e8a8482ffa66b/docs/009jev/measurements.json) report:

| Measurement | Baseline | Native SLA + Jev |
| --- | --- | --- |
| Full generation, one adopted run each | 366.720 s | 213.890 s |
| Reported reduction | — | 41.675% |

Conditions: RTX4070 12GB, 1024×1792, 124 frames at 24fps, seed 2026, four sampling steps; timing includes loading, Jev wait, VAE and saving. Earlier hand-defect runs were excluded; both methods were rerun after changing the prompt. The author explicitly states this does not isolate Jev's improvement over fixed SLA and does not establish perceptual quality equivalence.

The older [`JEV_ADAPTIVE.en.md`](https://github.com/sepiablue-ai/ComfyUI-MiniMax-H3-W4A4-VSA/blob/dde3dbc63af89d86d2d9d302082e8a8482ffa66b/JEV_ADAPTIVE.en.md) reports fixed5 at 212.20 s versus layer_v5 at 219.15 s: that older adaptive experiment was slower. Different paths/conditions must not be combined into one performance claim.

## Transfer into our workflow

| Reference project | Our built-in image workflow |
| --- | --- |
| Tensor/attention statistics | User request before generation; real visual inspection report afterward |
| Per-layer keep choices | Generate/edit/discuss; preserve identity/layout/text; bounded repair selection |
| Sparse-attention kernel applies choice | Codex calls the existing built-in image tool |
| Four bounded Jev queries | One plan query and at most one review query per asset |
| Fixed keep fallback | Explicit Codex fallback, never fake Jev output |

We cannot transplant tensor-level acceleration into the closed image endpoint. The plausible benefit here is fewer wrong routes or repairs. A fair test holds the rest of the workflow constant and swaps only the decision source. No attention acceleration or 41.7% claim belongs in this skill's result reporting.
