# Uncensored / Open-Weight LLMs for 12GB VRAM (RTX 4070)

> Research Date: 2026-05-20
> Target: RTX 4070 (12GB VRAM)
> Focus: Truly uncensored models — Dolphin series, NousResearch, Abliterated variants

---

## VRAM Requirements by Model Size & Quantization

GGUF quantization levels and approximate VRAM needed for inference (4k context, ~20% overhead):

| Model Size | Q4_K_M (4-bit) | Q5_K_M (5-bit) | Q6_K (6-bit) | Q8_0 (8-bit) | FP16 |
|---|---|---|---|---|---|
| 1.5B (Phi-2)  | ~1.2 GB | ~1.5 GB | ~1.7 GB | ~2.2 GB | ~3.5 GB |
| 3B            | ~2.5 GB | ~3.0 GB | ~3.5 GB | ~4.5 GB | ~7.0 GB |
| 7B            | ~5.0 GB | ~6.0 GB | ~7.0 GB | ~9.0 GB | ~14 GB |
| 8B            | ~5.5 GB | ~6.5 GB | ~7.5 GB | ~10 GB | ~16 GB |
| 13B           | ~8.5 GB | ~10 GB  | ~11.5 GB| ~15 GB  | ~26 GB |
| 20B           | ~12 GB  | ~14 GB  | ~16 GB  | ~21 GB  | ~40 GB |
| 34B           | ~19 GB  | ~22 GB  | ~26 GB  | ~33 GB  | ~68 GB |

**For 12GB VRAM (RTX 4070), viable options:**
- **7B/8B models**: Q4_K_M through Q8_0 all fit comfortably
- **13B models**: Q4_K_M only (~8.5 GB, some headroom for context)
- **20B models**: Q4_K_M barely fits (~12 GB with minimal context)
- **34B models**: Q2_K or Q3_K might fit with heavy quantization, but quality degrades

---

## Uncensored Model Categories

### "Truly" Uncensored
These models were trained without refusal mechanisms — they answer any question directly:

- **Dolphin series** (cognitivecomputations / Eric Hartford) — trained on uncensored multi-turn conversations. Removes alignment/refusal entirely.
- **Abliterated models** — base models (Llama 3, Mistral, Qwen, etc.) modified via FailSpy's [abliterator](https://github.com/failspy/abliterator) tool, which removes the "refusal direction" from residual stream activations. The model retains its intelligence but can no longer refuse.
- **Bagel series** (jondurbin) — fine-tuned on diverse datasets including "uncensored" portions; doesn't hard-code refusals.

### "Lightly Censored" / "Refusal-Trained" (NOT truly uncensored)
These models will refuse certain categories of requests:

- **Nous Hermes series** — fine-tuned for instruction following but retains some base model guardrails
- **Meta Llama 3 / 3.1 Instruct** — heavily refusal-trained; requires abliteration to uncensor
- **Mistral / Mixtral Instruct** — some refusal baked in; abliterated variants exist
- **Qwen 2.5 / 3 Instruct** — refusal-trained; abliterated variants exist
- **DeepSeek** — refusal-trained; not recommended for uncensored use

---

## Recommended Models for 12GB VRAM

### Tier 1: Best Performance (7B-8B, all quants fit)

| Model | Parameters | Source | Quantization | VRAM | Notes |
|---|---|---|---|---|---|
| **Dolphin 2.9.2 Llama 3.1 8B** | 8B | [cognitivecomputations](https://huggingface.co/cognitivecomputations) | GGUF Q4_K_M (~5.5 GB) | ~5.5 GB | Latest Dolphin on Llama 3.1 base. Truly uncensored, not just refusal-ablated. High quality. |
| **Dolphin 2.9.1 Llama 3 8B** | 8B | [cognitivecomputations](https://huggingface.co/cognitivecomputations) | GGUF Q4_K_M (~5.5 GB) | ~5.5 GB | Predecessor to 2.9.2; solid uncensored model. |
| **Dolphin 2.8 Mistral 7B v02** | 7B | [cognitivecomputations](https://huggingface.co/cognitivecomputations) | GGUF Q4_K_M (~5 GB) | ~5 GB | Mistral 7B v0.2 base, well-tested uncensored model. |
| **Dolphin 2.6 Mistral 7B** | 7B | [cognitivecomputations](https://huggingface.co/cognitivecomputations) | GGUF Q4_K_M (~5 GB) | ~5 GB | Older but very stable; widely used. |
| **Dolphin 3.0 Llama 3.1 8B** | 8B | [cognitivecomputations](https://huggingface.co/cognitivecomputations) | GGUF Q4_K_M (~5.5 GB) | ~5.5 GB | Latest Dolphin generation; improves on 2.9.x. |
| **Abliterated Llama 3.1 8B Instruct** | 8B | Community (FailSpy method) | GGUF Q4_K_M (~5.5 GB) | ~5.5 GB | Base Llama 3.1 Instruct with refusal ablated. Quality preserved. |
| **Abliterated Mistral 7B v0.3** | 7B | Community (FailSpy method) | GGUF Q4_K_M (~5 GB) | ~5 GB | Mistral 7B v0.3 instruct with refusal removed. |
| **Nous Hermes 2 Mistral 7B DPO** | 7B | [NousResearch](https://huggingface.co/NousResearch) | GGUF Q4_K_M (~5 GB) | ~5 GB | Good instruction following, lighter refusals. Apache 2.0. |
| **Nous Hermes 2 Yi 34B** | 34B | [NousResearch](https://huggingface.co/NousResearch) | GGUF Q2_K (~13 GB) | ~13 GB | Too large for 12 GB even at Q2_K. Skip for RTX 4070. |
| **NeuralMarcoro14 7B** | 7B | Community | GGUF Q4_K_M (~5 GB) | ~5 GB | Merge-based model, often recommended for uncensored roleplay. |

### Tier 2: High Quality (13B, Q4_K_M only)

| Model | Parameters | Source | Quantization | VRAM | Notes |
|---|---|---|---|---|---|
| **Dolphin 2.2.1 Mistral 7B** | 7B | cognitivecomputations | GGUF Q5_K_M (~6 GB) | ~6 GB | Excellent uncensored general-purpose model. |
| **Abliterated Llama 2 13B** | 13B | Community | GGUF Q4_K_M (~8.5 GB) | ~8.5 GB | Older but larger; fits with headroom. |
| **Bagel 13B DPO** | 13B | [jondurbin](https://huggingface.co/jondurbin) | GGUF Q4_K_M (~8.5 GB) | ~8.5 GB | Trained on diverse data; minimal refusals. |
| **Pygmalion 2 13B** | 13B | PygmalionAI | GGUF Q4_K_M (~8.5 GB) | ~8.5 GB | Roleplay-focused; very uncensored. |

### Tier 3: Creative / Specialized (7B)

| Model | Parameters | Source | Notes |
|---|---|---|---|
| **Dolphin Phi-2** | 2.7B | cognitivecomputations | Tiny, fast, surprisingly capable for its size. Fits Q8_0 (~3 GB). |
| **Miqu 70B** | 70B | [miqudev](https://huggingface.co/miqudev) | Leaked Mistral-medium; too large for 12 GB (needs at least 24 GB at Q4). |
| **Tulu 2 DPO 7B / 13B** | 7B/13B | Allen AI | Open-source fine-tune; lighter guardrails than base. |
| **Euryale 1.3 70B** | 70B | Community | Roleplay merge; too large for 12 GB. |

---

## How to Find GGUF Quantized Versions on Hugging Face

Most uncensored models are available as GGUF quants via community members like:

- **TheBloke** (classic, massive GGUF library — most major models)
- **MaziyarPanahi** (frequent GGUF conversions for newer models)
- **Bartowski** (many GGUF quants including abliterated variants)
- **Lewdiculous** (roleplay/uncensored GGUF quants)

Search pattern: `huggingface.co/<user>/<model-name>-GGUF`

### Key Hugging Face Links

| Model | GGUF Source |
|---|---|
| Dolphin 2.9.2 Llama 3.1 8B | `huggingface.co/cognitivecomputations/dolphin-2.9.2-llama-3.1-8b` |
| Dolphin 2.9.1 Llama 3 8B | `huggingface.co/cognitivecomputations/dolphin-2.9.1-llama-3-8b` |
| Dolphin 2.8 Mistral 7B | `huggingface.co/cognitivecomputations/dolphin-2.8-mistral-7b` |
| Dolphin 2.6 Mistral 7B | `huggingface.co/cognitivecomputations/dolphin-2.6-mistral-7b` |
| Nous Hermes 2 Mixtral | `huggingface.co/NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO` |
| Nous Hermes 2 SOLAR 10.7B | `huggingface.co/NousResearch/Nous-Hermes-2-SOLAR-10.7B` |
| FailSpy abliterator tool | `github.com/failspy/abliterator` |
| Abliterated models | Search `huggingface.co/models?search=abliterated` |

---

## Quantization Guidance for RTX 4070

### Recommended Strategy
1. **8B models (e.g., Dolphin 3.0 / 2.9.2)**: Use Q5_K_M or Q6_K for best quality. Fits easily with 4k-8k context.
2. **7B models**: Q8_0 fits with room for ~8k context. Best quality.
3. **13B models**: Q4_K_M is the maximum that fits. Quality is good but expect ~10-15% quality loss vs Q8_0.
4. **20B+ models**: Do not recommend for 12 GB. Even Q4_K_M barely loads with no context room.

### Backend Recommendations
| Backend | Best for | Notes |
|---|---|---|
| **llama.cpp** (GGUF) | All models | Best VRAM efficiency with K-quants. CUDA offloading works great. |
| **ExLlamaV2** (EXL2) | 7B-13B | Higher tokens/sec on 12 GB. Good for roleplay/chat. |
| **AutoGPTQ** / **AWQ** | 7B-8B | Less efficient than GGUF for 12 GB; skip unless you need specific model format. |

---

## Actual Uncensorship Status

| Model | Truly Uncensored? | Notes |
|---|---|---|
| Dolphin 2.6, 2.8, 2.9, 3.0 | **YES** | Trained on unfiltered datasets; no refusal mechanism |
| Abliterated Llama 3 / Mistral / Qwen | **YES** | Refusal direction surgically removed via ablation |
| Bagel DPO | **Mostly YES** | Minimal refusal training |
| Nous Hermes 2 | **NO** | Retains base model refusals, though light |
| Base Llama 3 / Mistral / Qwen Instruct | **NO** | Heavily refusal-trained; needs abliteration |
| DeepSeek V3 / R1 | **NO** | Refusal baked in |
| Command R / R+ | **NO** | Enterprise safety filters |

---

## Top 6 Recommendations for RTX 4070 (12GB)

1. **Dolphin 3.0 Llama 3.1 8B** (GGUF Q5_K_M) — Best overall uncensored model for 12 GB
2. **Dolphin 2.9.2 Llama 3.1 8B** (GGUF Q5_K_M) — Excellent alternative; more battle-tested
3. **Abliterated Llama 3.1 8B Instruct** (GGUF Q5_K_M) — Best quality if you want base Llama without refusals
4. **Dolphin 2.8 Mistral 7B** (GGUF Q8_0) — Maximum quality at 7B scale
5. **Abliterated Mistral 7B v0.3** (GGUF Q8_0) — Best Mistral-based uncensored option
6. **Dolphin Phi-2** (GGUF Q8_0) — Fastest option for simple uncensored requests

---

## Sources

- https://github.com/failspy/abliterator — Abliteration tool and methodology
- https://huggingface.co/cognitivecomputations — Dolphin model series
- https://huggingface.co/NousResearch — Nous Hermes model series
- https://huggingface.co/jondurbin — Bagel model series
- https://github.com/ggerganov/llama.cpp — GGUF quantization and inference
- https://llm-tracker.info — LLM model and hardware tracking
