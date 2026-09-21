# Supported model families and availability

Catalog checked 2026-09-21. **Support means model-aware connected-tool routing**, not bundled API clients or completed live validation. The built-in tool is the default. Explicit model requests require a connected tool with verified model selection or a fixed-model contract. See [execution instructions](providers.md).

## Version catalog

| Name | Exact model ID | Official reference |
| --- | --- | --- |
| GPT Image 1 | `gpt-image-1` | [Documentation](https://developers.openai.com/api/docs/guides/tools-image-generation) |
| GPT Image 1-mini | `gpt-image-1-mini` | [Documentation](https://developers.openai.com/api/docs/guides/tools-image-generation) |
| GPT Image 1.5 | `gpt-image-1.5` | [Documentation](https://developers.openai.com/api/docs/guides/tools-image-generation) |
| GPT Image 2 | `gpt-image-2` | [Documentation](https://developers.openai.com/api/docs/guides/tools-image-generation) |
| GPT Image 2.5-sunburst | `gpt-image-2.5-sunburst` | [Documentation](https://developers.openai.com/api/docs/guides/tools-image-generation) |
| GPT Image 2.5-flare | `gpt-image-2.5-flare` | [Documentation](https://developers.openai.com/api/docs/guides/tools-image-generation) |
| Nano Banana | `gemini-2.5-flash-image` | [Documentation](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-image) |
| Nano Banana Pro | `gemini-3-pro-image` | [Documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image) |
| Nano Banana 2 | `gemini-3.1-flash-image` | [Documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-image) |
| Nano Banana 2 Lite | `gemini-3.1-flash-lite-image` | [Documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite-image) |
| Seedream 4.0 | `doubao-seedream-4-0-250828` | [Documentation](https://docs.volcengine.com/docs/ark/model-release-announcement?lang=zh) |
| Seedream 4.5 | `doubao-seedream-4-5-251128` | [Documentation](https://docs.volcengine.com/docs/ark/model-release-announcement?lang=zh) |
| Seedream 5.0 | `doubao-seedream-5-0-260128` | [Documentation](https://docs.volcengine.com/docs/ark/model-release-announcement?lang=zh) |
| Seedream 5.0 Lite | `doubao-seedream-5-0-lite-260128` | [Documentation](https://docs.volcengine.com/docs/ark/model-release-announcement?lang=zh) |
| Seedream 5.0 Pro | `doubao-seedream-5-0-pro-260628` | [Documentation](https://docs.volcengine.com/docs/ark/model-release-announcement?lang=zh) |

Nano Banana's original, Pro, 2 and 2 Lite are distinct models. GPT Image 2.5 requires Sunburst or Flare; the resolver returns `choose_version` for an unspecified 2.5. Exact preview/snapshot IDs not in the catalog are not silently rewritten to stable IDs. Provider-specific IDs, including BytePlus vs Volcengine Seedream names, must be verified before adding a mapping. Catalog membership does not guarantee current account access.

## Built-in image_gen

No model selector is exposed in the current built-in schema. Preserve its actual prompt/reference interface; do not invent model, quality, seed, attention or sampling arguments. The [Codex image documentation](https://learn.chatgpt.com/docs/image-generation) describes its managed generation path, but actual model metadata may be absent. Record observed model as null unless returned. An explicit GPT Image 1/2/2.5 request cannot be fulfilled by simply putting a model name in the prompt.

## External tools

Use current discovery to establish model availability, reference limits, editing support and options. API model IDs are catalog identifiers, not claims that this repository contains an API adapter. A model error stops that route; no automatic provider fallback. Provider access and billing are separate from Codex's built-in entitlement.

Seedream sources also include the [official 2026 release record](https://docs.volcengine.com/docs/LakeAIService/FeatureReleaseRecord2026?lang=en) for 5.0/5.0 Lite and the [image-generation reference](https://www.volcengine.com/docs/82379/1541523). Volcengine's release page is partly client-rendered; inventory discovery remains necessary and capability limits are not hard-coded from its snippets.

Jev still sees text, not pixels. None of these routes exposes model attention control through this skill. Reducing rework remains an evaluation hypothesis, not a demonstrated inference speedup.
