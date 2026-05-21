# Qwen3 14B Abliterated Q4_K_M GGUF — Research Report

## Download Links

### Primary Recommendation: bartowski/huihui-ai_Qwen3-14B-abliterated-GGUF
- **HF URL**: https://huggingface.co/bartowski/huihui-ai_Qwen3-14B-abliterated-GGUF
- **Direct Q4_K_M download**: https://huggingface.co/bartowski/huihui-ai_Qwen3-14B-abliterated-GGUF/resolve/main/huihui-ai_Qwen3-14B-abliterated-Q4_K_M.gguf
- **Size**: 9.0 GB, 4.85 BPW
- **CLI**: `huggingface-cli download bartowski/huihui-ai_Qwen3-14B-abliterated-GGUF --include "huihui-ai_Qwen3-14B-abliterated-Q4_K_M.gguf" --local-dir ./`

### Easiest Setup: Ollama (richardyoung)
- **One-command run**: `ollama run richardyoung/qwen3-14b-abliterated`
- **URL**: https://ollama.com/richardyoung/qwen3-14b-abliterated
- **Ollama Downloads**: 7,627+

### Alternatives
| Source | URL | Notes |
|--------|-----|-------|
| huihui-ai (original) | https://huggingface.co/huihui-ai/Qwen3-14B-abliterated-GGUF | Original upload |
| Mungert | https://huggingface.co/Mungert/Qwen3-14B-abliterated-GGUF | Includes ultra-low-bit quants |

---

## Evidence That Fewer Refusals Is Better

### 1. Academic Foundation: Refusal Is a Single Direction (NeurIPS 2024)
The paper *"Refusal in Language Models Is Mediated by a Single Direction"* (Arditi et al., arXiv:2406.11717) proved that refusal behavior is a **shallow, brittle feature** — a single 1D subspace in the residual stream. Erasing it surgically via weight orthogonalization disables refusal with **minimal effect on other capabilities**.

### 2. Community Use Cases for Reduced Refusal
- **Creative writing/roleplay**: Safety filters falsely flag fantasy violence, adult themes, and conflict-driven plots. Abliterated models remove these false positives.
- **Code generation**: Censored models refuse legitimate requests for security tools, encryption, and admin scripts. Abliterated models don't block these.
- **Unbiased information**: Censored models inject forced positive framing. Abliterated models give data-driven answers without mandatory disclaimers.
- **Agentic tool-use**: A model that refuses instructions is broken for autonomous agents. User should be in control.

### 3. Important Caveats
- **Performance can degrade** if abliteration is done without post-ablation fine-tuning (source: r/LocalLLaMA, 451 upvotes)
- **Keyword-matching evaluation overstates uncensoring** — models may produce circumlocutory refusals instead of genuine compliance
- **Universal "danger zone"** at ~50-56% model depth where modification kills performance

### Verdict
The strongest argument: refusal is a brittle fine-tuning patch, not an integral capability. When done correctly (with proper evaluation and post-ablation fine-tuning), abliteration produces models that are more useful and under user control. This specific Qwen3 14B abliterated model achieves ~80% refusal reduction with KL divergence of only 0.98 — preserving most original capabilities.
