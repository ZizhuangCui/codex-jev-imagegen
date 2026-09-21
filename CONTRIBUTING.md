# Contributing

Small, evidence-backed improvements are welcome. Start with an issue for a new provider adapter or a change to decision semantics; a focused bug fix can go directly to a pull request.

## Local checks

```sh
python3 -B skills/jev-imagegen/scripts/test_decide.py
python3 -B -m unittest discover -s tests -v
```

No dependency installation or live API key is needed. Add a focused behavior check when changing validation, transport, fallback, or installation behavior.

## Useful contributions

- Labeled, permission-cleared image requests, especially Chinese and mixed-language edits.
- Failure cases involving ambiguous intent, identity locks, or exact text.
- Evidence about a provider's actual API capabilities, with official documentation links.
- Reproducible A/B evaluations using the same image backend and call budget.

## Preserve the contract

Do not silently change the selected model, remove confirmed constraints, generate without user intent, or label a fallback as a Jev result. Missing evidence must remain unknown. Keep reference interpretation and image inspection separate from Jev's text-only decisions.

Do not commit API keys, raw private prompts, account screenshots, personal filesystem paths, image assets without publication rights, or billed outputs from a user session. Label synthetic fixtures and mocked responses clearly. Ask the maintainer before adding dependencies or paid CI work.

If you report performance, include all runs, call counts, model/backend identifiers, failure cases and quality checks. A single successful image is not an accuracy benchmark. See [the evaluation plan](docs/EVALUATION.md).

Contributions are provided under the repository's MIT license. Do not copy GPL implementation code from the reference experiment into this project.
