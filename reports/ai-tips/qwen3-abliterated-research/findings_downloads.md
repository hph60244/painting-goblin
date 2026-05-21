# Qwen3 14B Abliterated Q4_K_M GGUF - Download Research Findings

## Summary

Multiple sources for downloading "Qwen3 14B abliterated q4_k_m gguf" models were found. The model is an **abliterated (uncensored)** version of the Qwen3-14B Instruct model, with refusal behavior reduced by ~80% while preserving coherence (KL divergence 0.98). The abliteration process uses the Heretic library.

---

## Primary Download Sources

### 1. bartowski/huihui-ai_Qwen3-14B-abliterated-GGUF (Hugging Face) - **RECOMMENDED**

- **URL**: https://huggingface.co/bartowski/huihui-ai_Qwen3-14B-abliterated-GGUF
- **Creator**: bartowski (hosting huihui-ai's model)
- **License**: Apache-2.0
- **Downloads**: 6,097+
- **Release Date**: May 6, 2025
- **Quantization Method**: llama.cpp imatrix using release b5284
- **Direct Q4_K_M download**: https://huggingface.co/bartowski/huihui-ai_Qwen3-14B-abliterated-GGUF/resolve/main/huihui-ai_Qwen3-14B-abliterated-Q4_K_M.gguf

**Quantization variants available (comprehensive list):**
| Variant | File Size | Notes |
|---------|-----------|-------|
| bf16 | 29.54 GB | Full BF16 weights |
| Q8_0 | 15.70 GB | Near-lossless |
| Q6_K_L | 12.50 GB | Very high quality, recommended |
| Q6_K | 12.12 GB | Very high quality, recommended |
| Q5_K_L | 10.99 GB | High quality, recommended |
| Q5_K_M | 10.51 GB | High quality, recommended |
| Q5_K_S | 10.26 GB | High quality, recommended |
| Q4_K_L | 9.58 GB | Good quality, recommended |
| Q4_1 | 9.39 GB | Legacy format |
| **Q4_K_M** | **9.00 GB** | **Good quality, default size, recommended** |
| Q3_K_XL | 8.58 GB | Lower quality |
| Q4_K_S | 8.57 GB | Slightly lower quality |
| Q4_0 | 8.54 GB | Legacy format |
| IQ4_NL | 8.54 GB | Similar to IQ4_XS |
| IQ4_XS | 8.11 GB | Decent quality |
| Q3_K_L | 7.90 GB | Lower quality |
| Q3_K_M | 7.32 GB | Low quality |
| IQ3_M | 6.88 GB | Medium-low quality |
| Q3_K_S | 6.66 GB | Low quality |
| Q2_K_L | 6.51 GB | Very low quality |
| IQ3_XS | 6.38 GB | Lower quality |
| IQ3_XXS | 5.94 GB | Lower quality |
| Q2_K | 5.75 GB | Very low quality |
| IQ2_M | 5.32 GB | Relatively low quality |
| IQ2_S | 4.96 GB | Low quality |
| IQ2_XS | 4.69 GB | Low quality |

**Download command:**
```bash
huggingface-cli download bartowski/huihui-ai_Qwen3-14B-abliterated-GGUF --include "huihui-ai_Qwen3-14B-abliterated-Q4_K_M.gguf" --local-dir ./
```

---

### 2. richardyoung/Qwen3-14B-abliterated-GGUF (Hugging Face)

- **URL**: https://huggingface.co/richardyoung/Qwen3-14B-abliterated-GGUF
- **Creator**: richardyoung
- **Also available on Ollama**: `richardyoung/qwen3-14b-abliterated`
- **Ollama URL**: https://ollama.com/richardyoung/qwen3-14b-abliterated
- **Ollama Downloads**: 7,627+
- **Quantizations**: Q4_K_M (9.0 GB, recommended), Q5_K_M (11 GB), IQ3_M (6.9 GB), IQ4_XS (8.2 GB), Q8_0 (16 GB)

**Quick start (Ollama):**
```bash
ollama run richardyoung/qwen3-14b-abliterated
ollama run richardyoung/qwen3-14b-abliterated:Q4_K_M
```

---

### 3. Mungert/Qwen3-14B-abliterated-GGUF (Hugging Face)

- **URL**: https://huggingface.co/Mungert/Qwen3-14B-abliterated-GGUF
- **Creator**: Mungert
- **Details**: Generated using llama.cpp at commit 19e899c. Includes ultra-low-bit quantization with IQ-DynamicGate (1-2 bit).

---

### 4. huihui-ai/Qwen3-14B-abliterated-GGUF (Hugging Face - Original)

- **URL**: https://huggingface.co/huihui-ai/Qwen3-14B-abliterated-GGUF
- **Creator**: huihui-ai (developed by bartowski)
- **Note**: This is the source model - the bartowski upload above is a mirror with the same files.

---

## Community Discussions

### Reddit - r/LocalLLaMA

Several discussions mention Qwen3 14B abliterated models:

1. **"Fun with Doom: trolley problem"** (5 months ago)
   - https://old.reddit.com/r/LocalLLaMA/comments/1pmjow2/
   - References "Qwen3 Abliterated (huihui-ai)" in a trolley problem test

2. **"Help me squeeze every drop out of my AMD Ryzen AI Max+ 395"** (1 month ago)
   - https://old.reddit.com/r/LocalLLaMA/comments/1snzbsj/
   - User uses `mradermacher/Huihui-Qwen3-30B-A3B-Instruct-2507-abliterated-GGUF`

3. **"Seeking best LLM models for Agentic Unity development"** (3 months ago)
   - https://old.reddit.com/r/LocalLLaMA/comments/1qqibnr/
   - Discussion includes Qwen3-14B and abliterated variants

4. **"My experience with 14B LLMs on phones"** (10 months ago)
   - https://old.reddit.com/r/LocalLLaMA/comments/1lpzvtx/
   - User tested abliterated Qwen3 14B at Q4_K_M on Snapdragon 8 Elite phones

---

## Related Models from Known GGUF Uploaders

### mradermacher
- Known for GGUF conversions of many models
- Has uploaded: `mradermacher/Huihui-Qwen3-30B-A3B-Instruct-2507-abliterated-GGUF`
- HF profile: https://huggingface.co/mradermacher

### bartowski
- Major GGUF uploader; uploaded huihui-ai's abliterated Qwen3 14B
- HF profile: https://huggingface.co/bartowski

### FailSpy
- Known for abliterated model GGUF conversions
- Likely repo: https://huggingface.co/FailSpy/abliterated-Qwen3-14B-GGUF

---

## Recommendations

| Use Case | Recommended Source | Variant |
|----------|-------------------|---------|
| Best all-around quality/size | bartowski/huihui-ai | Q4_K_M (9.0 GB) |
| Easiest setup (one command) | Ollama (richardyoung) | Q4_K_M (9.0 GB) |
| Maximum quality | bartowski/huihui-ai | Q6_K (12.12 GB) |
| Low VRAM / constrained | bartowski/huihui-ai | IQ3_M (6.88 GB) |
| Near-lossless | bartowski/huihui-ai | Q8_0 (15.70 GB) |

---

## Disclaimer

Abliterated models have reduced safety guardrails. Use responsibly and in accordance with applicable laws and regulations.
