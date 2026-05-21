# Uncensored LLM Performance on RTX 4070 Class Hardware (12GB VRAM)

**Research Date:** May 2026
**Sources:** llmhardware.io, hardware-corner.net, llmrun.dev, gigachadllc.com, practicalwebtools.com, localllm.in, watsonout.com, github.com/ggml-org/llama.cpp

---

## 1. RTX 4070 Hardware Specifications

| Spec | Value |
|------|-------|
| VRAM | 12 GB GDDR6X |
| Memory Bandwidth | 504 GB/s |
| Architecture | Ada Lovelace |
| CUDA Cores | 5,888 |
| Tensor Cores | 4th Gen (FP16/INT8/INT4) |
| TDP | 200W |
| Memory Bus | 192-bit |
| Compute Capability | 8.9 (full CUDA support) |

*Source: [llmhardware.io/guides/rtx-4070-llm-guide](https://llmhardware.io/guides/rtx-4070-llm-guide)*

The RTX 4070's 504 GB/s bandwidth is 1.75x the RTX 4060 Ti 16GB (288 GB/s), making it significantly faster per token on models that fit. The trade-off is 12 GB VRAM vs 16 GB.

---

## 2. Inference Speed Benchmarks (Tokens/Second)

### Measured on RTX 4070 (Ollama / llama.cpp / CUDA)

| Model | Quantization | VRAM Used | Tokens/sec | Source |
|-------|-------------|-----------|------------|--------|
| TinyLlama 1.1B | Q4_K_M | ~1.0 GB | ~324 t/s | llmrun.dev |
| Llama 3.2 3B | Q4_K_M | ~2.0 GB | ~166 t/s | llmrun.dev |
| Qwen3 4B | Q4_K_M | ~2.9 GB | ~113 t/s | llmrun.dev |
| Phi-4 Mini 3.8B | Q4_K_M | ~2.9 GB | ~115 t/s | llmrun.dev |
| Llama 3.1 8B | Q4_K_M | ~5.3 GB | 62-68 t/s | llmrun.dev, practicalwebtools.com |
| Llama 3.1 8B | Q8_0 | ~8.5 GB | ~35 t/s | llmhardware.io |
| Qwen3 8B | Q4_K_M | ~5.5 GB | ~59 t/s | llmrun.dev |
| Qwen3 8B | Q8_0 | ~8.6 GB | ~35 t/s | llmhardware.io |
| Gemma 3 12B | Q4_K_M | ~7.4 GB | ~41 t/s | llmrun.dev |
| Mistral 7B v0.3 | Q4_K_M | ~4.9 GB | ~67 t/s | llmrun.dev |
| Gemma 2 9B | Q4_K_M | ~6.1 GB | ~54 t/s | llmrun.dev |
| Qwen3 14B | Q4_K_M | ~9.0 GB | 30-33 t/s | hardware-corner.net, llmhardware.io |
| Phi-4 14B | Q4_K_M | ~8.8 GB | ~30 t/s | llmrun.dev, llmhardware.io |
| DeepSeek R1 Distill 14B | Q4_K_M | ~9.0 GB | ~28 t/s | llmhardware.io |

### Detailed Context Scaling (Hardware Corner Benchmarks - Q4_K quant)

**Qwen3 8B:**
| Context | Prompt Processing | Token Generation |
|---------|------------------|-----------------|
| 4K | 3,564 t/s | 71.2 t/s |
| 16K | 2,064 t/s | 52.1 t/s |
| 32K | 1,117 t/s | 38.1 t/s |

**Qwen3 14B:**
| Context | Prompt Processing | Token Generation |
|---------|------------------|-----------------|
| 4K | 2,100 t/s | 42.5 t/s |
| 16K | 1,356 t/s | 32.7 t/s |

*Source: [hardware-corner.net/gpu-llm-benchmarks/rtx-4070/](https://www.hardware-corner.net/gpu-llm-benchmarks/rtx-4070/)*

### Additional Benchmarks (GigaChad LLC - TensorRT)

| Model | Runtime | Tokens/sec |
|-------|---------|------------|
| LLaMA-2 7B | TensorRT int4 (AWQ) | 85 t/s |
| Mistral 7B | TensorRT int8 | 52 t/s |
| LLaMA-2 7B | PyTorch FP16 (torch.compile) | 40 t/s |
| LLaMA-2 13B | TensorRT int4 | 28 t/s |
| GPT-J 6B | PyTorch FP16 | 48 t/s |
| BERT base (seq=128) | FP16 | 3,200 t/s |

*Source: [gigachadllc.com/geforce-rtx-4070-ai-benchmarks-breakdown/](https://gigachadllc.com/geforce-rtx-4070-ai-benchmarks-breakdown/)*

---

## 3. Best Inference Engines for Consumer GPUs

### Ollama (Recommended for most users)
- **Ease of Use:** Extremely easy. One-click install, GPU auto-detected.
- **Model Management:** Pull models with `ollama run <model>`.
- **Performance:** Good; uses llama.cpp backend under the hood with CUDA acceleration.
- **Best for:** Users who want simplest setup, quick experimentation.
- **Install:** [ollama.com](https://ollama.com)

### llama.cpp (Best performance/flexibility)
- **Ease of Use:** Moderate. Requires compilation or binary download.
- **Performance:** Excellent. Full CUDA support via `-DGGML_CUDA=ON`. Supports all quantization formats. Most optimized for consumer GPUs.
- **Features:** KV cache quantization, Flash Attention, concurrent serving (`llama-server`), CPU offloading.
- **Best for:** Power users, maximum performance, server deployments.
- **Install:** Build from [github.com/ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)

### LM Studio (GUI-based)
- **Ease of Use:** Very easy. GUI for downloading and running GGUF models.
- **Performance:** Good; uses llama.cpp backend.
- **Best for:** Users who prefer GUI over terminal, model exploration.
- **Install:** [lmstudio.ai](https://lmstudio.ai)

### text-generation-webui (Oobabooga)
- **Ease of Use:** Moderate. Browser-based UI with many features.
- **Performance:** Good. Supports multiple backends (llama.cpp, ExLlama, AutoGPTQ).
- **Best for:** Users who want many options (chat, instruct, notebook modes), API endpoints.
- **Install:** [github.com/oobabooga/text-generation-webui](https://github.com/oobabooga/text-generation-webui)

### vLLM (Production serving)
- **Ease of Use:** Moderate. Requires Python setup.
- **Performance:** Excellent for batching/multi-user. PagedAttention for efficient KV cache.
- **Best for:** API servers, multi-user deployments, production workloads.
- **Note:** Requires more setup; best for advanced users serving multiple concurrent requests.

### TensorRT-LLM (Maximum speed)
- **Ease of Use:** Complex. Requires model conversion/compilation.
- **Performance:** Highest throughput. Up to 85 t/s on 7B models (int4 AWQ).
- **Best for:** Users wanting absolute maximum performance willing to invest setup time.
- **Note:** Compilation step for each model; less flexible than llama.cpp.

**Recommendation for RTX 4070:** Start with **Ollama** for simplicity. Switch to **llama.cpp** directly for better control and performance. Use **LM Studio** if you prefer GUI.

*Sources: [llmhardware.io/guides/rtx-4070-llm-guide](https://llmhardware.io/guides/rtx-4070-llm-guide), [gigachadllc.com](https://gigachadllc.com/geforce-rtx-4070-ai-benchmarks-breakdown/)*

---

## 4. Context Window Sizes with 12GB VRAM

### VRAM Requirements by Model and Context (Q4_K_M quantization)

| Model | Weights VRAM | 4K Ctx Total | 16K Ctx Total | 32K Ctx Total | 64K Ctx Total |
|-------|-------------|-------------|--------------|--------------|--------------|
| 7-8B (e.g., Qwen3 8B) | ~5.8 GB | ~6.0 GB | ~6.5 GB | ~6.8 GB | ~7.8 GB |
| 12-14B (e.g., Qwen3 14B) | ~9.0 GB | ~9.3 GB | ~9.8 GB | ~10.5 GB | ~11.8 GB* |
| 20-22B (e.g., Mistral Small) | ~13.5 GB | Does not fit | Does not fit | Does not fit | Does not fit |

*Estimates include ~0.75 GB backend baseline overhead.
*14B at 64K context pushes ~11.8 GB — critically close to the 12 GB ceiling, may cause OOM with display overhead.*

### What Fits at Different Context Lengths:

| Context Length | Models that Fit (Q4_K_M) |
|---------------|------------------------|
| 4K-32K | 7B, 8B, 12B, 14B models all fit comfortably |
| 64K | 14B models are borderline (~11.8 GB); 7-8B models fit fine |
| 128K | 7-8B only (Qwen3 8B at 128K = ~10.5 GB) |
| 256K+ | Not feasible on 12 GB without aggressive quantization or CPU offloading |

### KV Cache Quantization Impact

Using `--cache-type-k q8_0 --cache-type-v q8_0` in llama.cpp can cut KV cache VRAM usage by ~50%, enabling longer contexts on the same hardware. This adds minimal quality degradation on modern models (especially Qwen 3.x series).

*Source: [localllm.in/blog/llamacpp-vram-requirements-for-local-llms](https://localllm.in/blog/llamacpp-vram-requirements-for-local-llms)*

---

## 5. Best Uncensored Models for RTX 4070 (Quality-to-Speed Ratio)

### For Conversation / General Chat

| Model | Size | Quant | VRAM | Speed | Quality Rating | Notes |
|-------|------|-------|------|-------|---------------|-------|
| Qwen3 14B (abliterated) | 14B | Q4_K_M | ~9.0 GB | ~30 t/s | Excellent | Best overall 12GB model in 2026 |
| Mistral Small 3.1 (abliterated) | 24B | Q3_K_M | ~10 GB* | ~20 t/s | Very Good | Punches above weight class; borderline fit |
| Phi-4 14B | 14B | Q4_K_M | ~8.8 GB | ~30 t/s | Excellent | Great for chat + reasoning |
| Llama 3.1 8B (abliterated) | 8B | Q4_K_M | ~5.3 GB | ~62 t/s | Good | Fast and widely supported |
| Qwen3 8B | 8B | Q8_0 | ~8.6 GB | ~35 t/s | Very Good | Near-lossless quality at 8B scale |

*Source: [watsonout.com](https://www.watsonout.com/editorials/the-sovereign-stack-best-uncensored-llms-for-local-inference-dec-2025/), [llmhardware.io/guides/best-llm-for-12gb-vram](https://llmhardware.io/guides/best-llm-for-12gb-vram)*

### For Coding

| Model | Size | Quant | VRAM | Speed | Notes |
|-------|------|-------|------|-------|-------|
| Phi-4 14B | 14B | Q4_K_M | ~8.8 GB | ~30 t/s | Best coding model for 12GB; optimized for reasoning chains |
| Qwen3 14B | 14B | Q4_K_M | ~9.0 GB | ~30 t/s | Excellent for code; supports thinking mode |
| DeepSeek R1 Distill 14B | 14B | Q4_K_M | ~9.0 GB | ~28 t/s | Strong reasoning for complex coding tasks |
| Qwen3 8B | 8B | Q8_0 | ~8.6 GB | ~35 t/s | Near-lossless quality, faster than 14B |

### For Creative Writing / Roleplay

| Model | Size | Quant | VRAM | Speed | Notes |
|-------|------|-------|------|-------|-------|
| Midnight Miqu 1.5 | 70B | Q3_K_M (offloaded) | ~40 GB* | ~5 t/s | Needs offloading; best prose quality but slow |
| Qwen3 14B (abliterated) | 14B | Q4_K_M | ~9.0 GB | ~30 t/s | Best balance for writing on 12GB |
| Mistral Small 3.1 (abliterated) | 24B | Q3_K_M | ~10 GB* | ~20 t/s | Good writing quality, borderline fit on 12GB |

*\*Requires partial CPU offloading or very aggressive quantization on 12 GB*

### "Abliterated" Uncensored Models

The current best approach for uncensored models is **abliteration** (surgically removing refusal neurons) rather than old-style fine-tuning on edgy data. Key developers: `failspy`, `mradermacher`. The result is the full intelligence of the base model without safety refusals.

*Source: [watsonout.com - The Sovereign Stack](https://www.watsonout.com/editorials/the-sovereign-stack-best-uncensored-llms-for-local-inference-dec-2025/)*

---

## 6. GPU-Only vs. GPU + CPU Offloading Performance

### Key Finding

**GPU-only inference is dramatically faster.** The RTX 4070's 504 GB/s VRAM bandwidth vs. system RAM's ~25-50 GB/s (DDR5) means offloading to CPU causes a 10-20x speed penalty.

### Performance Impact of Offloading

| Scenario | 7B Model Speed | 14B Model Speed | Notes |
|----------|---------------|----------------|-------|
| Full GPU (fits in VRAM) | 60-68 t/s | 30-33 t/s | RTX 4070 native |
| 50% GPU / 50% CPU offload | ~5-10 t/s | ~3-5 t/s | PCIe bottleneck |
| Full CPU (no GPU) | ~2-5 t/s | ~1-3 t/s | Usually uses RAM + CPU |
| Full GPU + Flash Attention | 65-72 t/s | 32-35 t/s | Best case with optimizations |

### When Offloading Makes Sense

- **Large models (30B+):** Only way to run them on 12 GB. Expect 2-5 t/s.
- **Batch processing:** For non-interactive tasks where speed doesn't matter.
- **Testing/tinkering:** To see if a model's quality justifies hardware upgrade.

### Recommended Strategy for RTX 4070

1. **Always prefer models that fully fit in VRAM.** At Q4_K_M, models up to 14B fit with headroom.
2. **If model doesn't fit:** Lower quantization (Q3_K_M, Q2_K) before resorting to offloading.
3. **Only use offloading as last resort** for models that won't fit even at Q2_K.
4. **KV cache quantization** (`--cache-type-k q8_0`) can help fit larger contexts without offloading.

### Comparison: RTX 4070 vs Other GPUs at Same Price Tier

| GPU | VRAM | Bandwidth | 8B Q4 Speed | 14B Q4 Speed | Fits Qwen3 14B Q8? |
|-----|------|-----------|------------|-------------|-------------------|
| RTX 4070 | 12 GB | 504 GB/s | ~62 t/s | ~30 t/s | No |
| RTX 4060 Ti 16GB | 16 GB | 288 GB/s | ~35 t/s | ~18 t/s | Yes |
| Intel Arc B580 | 12 GB | 456 GB/s | ~40 t/s | ~20 t/s | No |
| RTX 4070 Super | 12 GB | 504 GB/s | ~65 t/s | ~32 t/s | No |
| RTX 5070 | 12 GB | ~896 GB/s | ~100+ t/s | ~50+ t/s | No |

*Source: [llmhardware.io/guides/rtx-4070-llm-guide](https://llmhardware.io/guides/rtx-4070-llm-guide)*

---

## 7. Recommendations Summary

### Best Models for RTX 4070 12GB

| Use Case | Model | Quant | Why |
|----------|-------|-------|-----|
| **Best Overall** | Qwen3 14B Q4_K_M | Q4_K_M | ~30 t/s, fits in 9 GB, excellent quality |
| **Best for Coding** | Phi-4 14B Q4_K_M | Q4_K_M | ~30 t/s, optimized for reasoning/code |
| **Best Speed** | Llama 3.1 8B Q4_K_M | Q4_K_M | ~62 t/s, feels instantaneous |
| **Best Quality/Speed** | Qwen3 8B Q8_0 | Q8_0 | ~35 t/s, near-lossless precision |
| **Best Fast Chat** | Gemma 3 12B Q4_K_M | Q4_K_M | ~41 t/s, uses only 7.4 GB |
| **Best Reasoning** | DeepSeek R1 Distill 14B Q4_K_M | Q4_K_M | ~28 t/s, step-by-step reasoning |

### Inference Engine Recommendation

| Engine | Recommended For |
|--------|----------------|
| Ollama | Beginners, quick setup, everyday use |
| llama.cpp | Power users, maximum performance, server mode |
| LM Studio | GUI lovers, model exploration |
| TensorRT-LLM | Maximum speed (85 t/s on 7B int4) |

### "Uncensored" Model Sources

Use abliterated versions of Qwen3, Llama 3.1/3.3, Mistral Small 3.1 from:
- Hugging Face: search for "abliterated" + model name, look for `mradermacher` or `failspy` builds
- Ollama: community tags for abliterated variants

---

## Sources

1. **LLMHardware.io** - RTX 4070 LLM Guide & 12GB VRAM best models guide
   https://llmhardware.io/guides/rtx-4070-llm-guide
   https://llmhardware.io/guides/best-llm-for-12gb-vram

2. **Hardware Corner** - RTX 4070 LLM Benchmarks with context scaling data
   https://www.hardware-corner.net/gpu-llm-benchmarks/rtx-4070/

3. **llmrun.dev** - Best AI Models for RTX 4070 with VRAM/speed estimates
   https://llmrun.dev/gpu/rtx-4070

4. **GigaChad LLC** - RTX 4070 AI Benchmarks Breakdown (TensorRT data)
   https://gigachadllc.com/geforce-rtx-4070-ai-benchmarks-breakdown/

5. **Practical Web Tools** - Local LLM Benchmarks 2025 (47 hardware-model combos)
   https://practicalwebtools.com/blog/local-llm-benchmarks-consumer-hardware-guide-2025

6. **LocalLLM.in** - llama.cpp VRAM Requirements Guide (32K/64K context)
   https://localllm.in/blog/llamacpp-vram-requirements-for-local-llms

7. **Watsonout** - The Sovereign Stack: Best Uncensored LLMs for Local Inference
   https://www.watsonout.com/editorials/the-sovereign-stack-best-uncensored-llms-for-local-inference-dec-2025/

8. **GitHub (llama.cpp)** - Performance discussions on Apple Silicon (methodology reference)
   https://github.com/ggml-org/llama.cpp/discussions/4167
