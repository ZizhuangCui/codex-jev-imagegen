# Multi-model tool routing

This is a Codex skill, not a provider SDK. `route.py` checks a requested model against an inventory of **currently observed tools**. It never authenticates, uploads images, calls APIs or executes commands. Codex invokes the selected tool using its actual schema. No external HTTP adapters are bundled.

## Agent procedure

1. Preserve explicit model choice outside Jev state. Jev chooses task/repair intent, not providers. With no model choice, use `builtin`.
2. Discover available tools and read the relevant provider skill and tool documentation. Use a fresh private run-directory inventory. Never infer a callable tool, account access or free service from the model catalog. Provider CLIs must follow their installed skill's discovery and execution flow.
3. Record actual tool names, exact supported model IDs, operations, reference capacity and evidence from discovery. `image_gen` is the normalized built-in name. Unknown capabilities must not be asserted. Use a separate inventory per selected model when a tool's limits vary by model. Inventories are agent-supplied assertions, not independent availability checks; rediscover after every session change.
4. Run `route.py` with the chosen model, operation and required reference count. For edits, also verify an actual edit target, not just style references. `handoff` means only that the supplied inventory matches. `blocked` stops generation without a model fallback. Resolve `choose_version` or `choose_tool` with the user's preference.
5. Map the prompt and every required reference to the selected tool's documented schema. Set its model selector to the exact resolved ID, or verify the tool is fixed to that model. If a provider uses another identifier, verify an explicit mapping from that provider's documentation; never guess. Authentication and billing follow the provider's setup. Never put credentials in inventories. Preserve model/tool during repairs unless the user changes them.
6. Built-in generation follows the `imagegen` skill and never receives a model argument. For all paths, inspect returned images, retain anchors and enforce call budgets. Record requested model, selected tool and observed model (null if metadata omits it). Text-only output or a job ID is not a completed image. Poll an asynchronous job; do not resubmit an unknown outcome.

## Inventory schema

```json
{
  "tools": [
    {
      "name": "image_gen",
      "models": [],
      "operations": ["generate", "edit"],
      "max_references": 5,
      "evidence": "Illustration only: replace with current tool discovery evidence"
    }
  ]
}
```

This illustrates the contract, not availability. An external entry uses a real tool name and exact catalog IDs confirmed by discovery. All required references must fit. Built-in capacity here conservatively uses the recent-image limit; local-path capacity must be checked in the actual tool contract.

```sh
python3 scripts/route.py --list
python3 scripts/route.py --model 'Nano Banana Pro' --inventory /absolute/path/discovered-tools.json
python3 scripts/route.py --model 'Seedream 5.0 Pro' --operation edit --reference-count 2 --inventory /absolute/path/discovered-tools.json
```

Exit 0: catalog or handoff; 2: malformed input; 3: blocked. These commands generate no images. Without an inventory, nothing is assumed available.

## Portability

Share the natural-language request, reference roles, invariants and verbatim text across providers. Keep dimensions, quality and format in tool-specific options; only use options that the selected model/tool actually supports. Do not treat OpenAI quality values, Gemini image sizes or Seedream batch options as interchangeable. Do not promise common seeds, masks, layers, transparency or reference limits.

Keep provider/model fixed in Jev-vs-Codex A/B tests; provider comparisons are a separate experiment.
