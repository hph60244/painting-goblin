# 自架 Uncensored LLM 研究報告 — NVIDIA RTX 4070 (12GB VRAM)

> 研究日期：2026-05-20
> 硬體：RTX 4070 (12GB GDDR6X, 504 GB/s, Ada Lovelace)

---

## 硬體規格摘要

| 項目 | 值 |
|------|------|
| VRAM | 12 GB GDDR6X |
| 記憶體頻寬 | 504 GB/s |
| 架構 | Ada Lovelace |
| CUDA 核心 | 5,888 |
| Tensor Core | 第4代 (FP16/INT8/INT4) |

---

## 模型選擇策略：VRAM 限制

### 各量化等級所需 VRAM

| 模型大小 | Q4_K_M | Q5_K_M | Q6_K | Q8_0 |
|---------|--------|--------|------|------|
| 7B | ~5.0 GB | ~6.0 GB | ~7.0 GB | ~9.0 GB |
| 8B | ~5.5 GB | ~6.5 GB | ~7.5 GB | ~10 GB |
| 13B | ~8.5 GB | ~10 GB | ~11.5 GB | ❌ |
| 14B | ~9.0 GB | ~10.5 GB | ~12 GB | ❌ |
| 20B+ | ❌ 無法裝載 | ❌ | ❌ | ❌ |

**結論：** RTX 4070 最佳甜蜜點為 **7-14B 模型**，14B 以上僅 Q4_K_M 勉強可行。

---

## 何謂真正的 Uncensored？

| 類別 | 代表模型 | 真正 Uncensored？ |
|------|---------|-----------------|
| **Dolphin 系列** (cognitivecomputations) | Dolphin 2.6/2.8/2.9/3.0 | ✅ **是** — 使用未過濾數據訓練，無拒絕機制 |
| **Abliterated 系列** (FailSpy 方法) | Abliterated Llama/Mistral/Qwen | ✅ **是** — 手術式移除拒絕神經元 |
| Bagel DPO (jondurbin) | Bagel 13B DPO | ⚠️ 幾乎是 — 極少拒絕訓練 |
| Nous Hermes 2 | Nous Hermes 2 Mixtral | ❌ 保留基礎模型防護 |
| 原始 Llama/Mistral/Qwen Instruct | — | ❌ 高度拒絕訓練，需 abliterate |

**Abliteration**（FailSpy 方法，[github.com/failspy/abliterator](https://github.com/failspy/abliterator)）是目前最佳做法：保留完整智能，僅移除拒絕方向，不像舊方法需重新訓練。

---

## 五大推薦方案（RTX 4070 最佳化）

### 🥇 首選：Qwen3 14B (abliterated) — Q4_K_M

| 項目 | 數值 |
|------|------|
| VRAM 使用 | ~9.0 GB（留有餘裕） |
| 推理速度 | ~30 t/s |
| 上下文長度 | 4K-32K 舒適，64K 臨界 |
| 適用場景 | 對話、編碼、創作、推理 |
| 來源 | Hugging Face 搜尋 `abliterated qwen3 14b` |

**推薦理由：** 2026 年 12GB VRAM 最佳模型，品質與速度的完美平衡。需自行尋找 abliterated 版本。

### 🥈 次選：Phi-4 14B (abliterated) — Q4_K_M

| 項目 | 數值 |
|------|------|
| VRAM 使用 | ~8.8 GB |
| 推理速度 | ~30 t/s |
| 適用場景 | **編碼最佳**、推理任務 |

### 🥉 現成 Uncensored：Dolphin 3.0 Llama 3.1 8B — Q5_K_M

| 項目 | 數值 |
|------|------|
| VRAM 使用 | ~6.5 GB |
| 推理速度 | ~60 t/s |
| 特色 | **無需 abliterate，開箱即用** |

**推薦理由：** 如果你不想處理 abliteration，Dolphin 3.0 是真正的開箱即用無審查模型。速度極快，品質優良。

### 4. Abliterated Llama 3.1 8B Instruct — Q8_0

| 項目 | 數值 |
|------|------|
| VRAM 使用 | ~9-10 GB |
| 推理速度 | ~35 t/s |
| 特色 | 近乎無損品質，廣泛社群支援 |

### 5. DeepSeek R1 Distill 14B (abliterated) — Q4_K_M

| 項目 | 數值 |
|------|------|
| VRAM 使用 | ~9.0 GB |
| 推理速度 | ~28 t/s |
| 特色 | 逐步推理能力最強 |

---

## 推理引擎比較

| 引擎 | 適合對象 | 速度表現 |
|------|---------|---------|
| **Ollama** | 初學者、快速上線 | 好（底層 llama.cpp + CUDA） |
| **llama.cpp** | 進階使用者、最大效能 | 最佳，完整 CUDA 支援 |
| **LM Studio** | 偏好 GUI 的使用者 | 好（同樣基於 llama.cpp） |
| **TensorRT-LLM** | 追求極速者 | 最高（7B int4 達 85 t/s） |

**建議：** 從 **Ollama** 開始，熟悉後可改用 **llama.cpp** 直接獲得更好控制。

---

## 速度基準（RTX 4070 實測）

| 模型 | 量化 | VRAM | Token/s |
|------|------|------|---------|
| TinyLlama 1.1B | Q4_K_M | ~1.0 GB | 324 t/s |
| Llama 3.1 8B | Q4_K_M | ~5.3 GB | 62-68 t/s |
| Llama 3.1 8B | Q8_0 | ~8.5 GB | ~35 t/s |
| Qwen3 14B | Q4_K_M | ~9.0 GB | 30-33 t/s |
| Phi-4 14B | Q4_K_M | ~8.8 GB | ~30 t/s |
| DeepSeek R1 Distill 14B | Q4_K_M | ~9.0 GB | ~28 t/s |
| Gemma 3 12B | Q4_K_M | ~7.4 GB | ~41 t/s |

---

## 課金注意事項

- **GPU 專屬模式 vs CPU 卸載：** 全 GPU 30-68 t/s，卸載至 CPU 僅 3-10 t/s（10-20 倍懲罰）
- **始終優先選擇完全裝入 VRAM 的模型**
- **KV Cache 量化**（`--cache-type-k q8_0`）可額外節省 ~50% KV cache VRAM
- **長上下文：** 7-8B 可達 128K，14B 建議維持 32K 內

---

## 快速開始指令（Ollama）

```bash
# 安裝 Ollama
# 從 https://ollama.com 下載

# 拉取真正 uncensored 模型
ollama pull dolphin-llama3:8b

# 或使用 abliterated 模型（搜尋社群標籤）
# 例如 abliterated Qwen3 14B（若 Ollama 有收錄）
```

---

## 資料來源

1. [LLMHardware.io — RTX 4070 LLM Guide](https://llmhardware.io/guides/rtx-4070-llm-guide)
2. [Hardware Corner — RTX 4070 LLM Benchmarks](https://www.hardware-corner.net/gpu-llm-benchmarks/rtx-4070/)
3. [llmrun.dev — Best AI Models for RTX 4070](https://llmrun.dev/gpu/rtx-4070)
4. [GigaChad LLC — RTX 4070 AI Benchmarks](https://gigachadllc.com/geforce-rtx-4070-ai-benchmarks-breakdown/)
5. [FailSpy Abliterator (GitHub)](https://github.com/failspy/abliterator)
6. [Watsonout — The Sovereign Stack: Best Uncensored LLMs](https://www.watsonout.com/editorials/the-sovereign-stack-best-uncensored-llms-for-local-inference-dec-2025/)
7. [LocalLLM.in — llama.cpp VRAM Requirements](https://localllm.in/blog/llamacpp-vram-requirements-for-local-llms)
8. [cognitivecomputations — Dolphin Model Series (HuggingFace)](https://huggingface.co/cognitivecomputations)
