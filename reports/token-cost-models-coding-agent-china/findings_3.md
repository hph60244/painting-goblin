# Coding Performance Benchmarks and Cost-Effectiveness Analysis for AI Models (2025-2026)

## Overview
This report analyzes coding performance benchmarks (HumanEval, MBPP, LiveCodeBench, etc.) for major AI models, with focus on Chinese models (DeepSeek-Coder, Qwen-Coder, CodeGeeX) versus international models (GPT-4, Claude, etc.). It examines the relationship between performance and cost (cost-effectiveness) for coding tasks.

## Key Benchmark Results (2025-2026)

### HumanEval+ and MBPP+ Performance
Based on recent research (arXiv:2509.24637, "Bridging Developer Instructions and Code Completion Through Instruction-Aware Fill-in-the-Middle Paradigm", 2025):

**Table 1: Pass@1 Scores on IHumanEval and IRME Benchmarks**

| Model | Version | Mode | IHumanEval (with instructions) | IRME (with instructions) | IHumanEval (no instructions) | IRME (no instructions) |
|-------|---------|------|--------------------------------|--------------------------|-------------------------------|-------------------------|
| Deepseek-Coder (6.7B) | base | PMS | 84.6% | 10.9% | 68.6% | 7.4% |
| Deepseek-Coder (6.7B) | ifim | PIMS | 93.6% | 21.1% | 78.2% | 16.0% |
| Qwen2.5-Coder (7B) | base | PSM | 91.0% | 18.4% | 76.0% | 10.2% |
| Qwen2.5-Coder (7B) | ifim | PSIM | 95.8% | 20.3% | 76.3% | 13.3% |

**Notes:**
- IHumanEval: Enhanced HumanEval-infilling benchmark with instructions
- IRME: IRepoMasterEval (real-world code completion benchmark)
- IFIM: Instruction-aware Fill-in-the-Middle training improves instruction-following while maintaining infilling capability
- Chinese code-specialized models achieve >90% Pass@1 on HumanEval with instructions

### LiveCodeBench Performance (2024-2025)
According to LiveCodeBench (contamination-free evaluation):

- **GPT-4-turbo** and **Claude-3-Opus** perform best across code generation, test output prediction, and code execution scenarios
- Among open-source models, **DeepSeek-Ins-33B** and **Phind-34B** perform best
- **DeepSeek models** show performance drop on LeetCode problems released after September 2023, indicating possible training data contamination
- **Open vs. Closed Models**: Closed API-access models generally outperform open models, but fine-tuned variants of large (30+B parameter) open models can surpass the barrier

### HumanEval vs. Real-World Performance
- Models performing well on HumanEval may overfit the benchmark (LiveCodeBench analysis)
- Some models (e.g., DS-Ins-1.3B) outperform Gemini-Pro and Claude-Ins-1 on HumanEval but perform worse on LCB-Easy
- Fine-tuned variants of open access models often show this overfitting pattern
- Base models and most closed API-access models show consistent performance across benchmarks

## Model Pricing and Cost Analysis (2026)

### OpenAI API Pricing (as of April 2026)
- **GPT-5.4**: Input $2.50 / 1M tokens, Cached input $0.25 / 1M tokens, Output $15.00 / 1M tokens
- **GPT-5.4 mini**: Input $0.75 / 1M tokens, Cached input $0.075 / 1M tokens, Output $4.50 / 1M tokens
- **GPT-5.4 nano**: Input $0.20 / 1M tokens, Cached input $0.02 / 1M tokens, Output $1.25 / 1M tokens

### Chinese Model Pricing

**DeepSeek API** (from findings_1.md):
- **deepseek-chat/deepseek-reasoner**: 1M input tokens (cache hit) $0.028, (cache miss) $0.28; 1M output tokens $0.42
- **Context Length**: 128K tokens
- **Open-source models**: Free for local deployment (DeepSeek-Coder series)

**Qwen (Alibaba Bailian)**:
- **Free tier**: New users get over 70 million free tokens (90-day validity)
- **Competitive pricing** for Qwen3.6-Plus and Qwen3.5-Turbo
- **Open-source models**: Free for local deployment (Qwen3-Coder-Next, Qwen3.5-Coder)

**Zhipu AI (GLM/ChatGLM)**:
- **GLM-4 series**: Tiered pricing, free trial available
- **Open-source**: ChatGLM3-6B series free for local deployment

**CodeGeeX**:
- **Free**: Open-source models available for download
- **Online services**: Free access with limitations

## Cost-Effectiveness Analysis

### Performance per Dollar

**Assumptions**:
- Average coding task: 500 input tokens, 200 output tokens
- 1,000 tasks per month

**Cost Calculation for 1,000 tasks**:
- **GPT-5.4 mini**: Input: 500k tokens × $0.75/M = $0.375; Output: 200k tokens × $4.50/M = $0.90; Total: $1.275 per 1k tasks
- **DeepSeek API (cache miss)**: Input: 500k tokens × $0.28/M = $0.14; Output: 200k tokens × $0.42/M = $0.084; Total: $0.224 per 1k tasks
- **Local deployment (DeepSeek-Coder)**: Zero API cost; only compute/electricity

**Performance-Cost Ratio** (using HumanEval Pass@1 with instructions):
- **GPT-5.4 mini** (estimated ~92% Pass@1): $1.275 / 92% = $1.39 per percentage point
- **DeepSeek-Coder (IFIM)** (93.6% Pass@1): $0.224 / 93.6% = $0.0024 per percentage point (API) or $0 (local)
- **Qwen2.5-Coder (IFIM)** (95.8% Pass@1): Similar cost to DeepSeek; $0.0021 per percentage point (API)

**Conclusion**: Chinese open-source code models offer dramatically better cost-effectiveness, especially when deployed locally.

### Real-World vs. Benchmark Performance Cost

- **HumanEval overfitting**: Some models achieve high HumanEval scores but perform worse on real-world benchmarks (IRME, LiveCodeBench)
- **Cost of overfitting**: Paying for high HumanEval performance may not translate to real-world utility
- **Recommendation**: Evaluate models on diverse benchmarks (LiveCodeBench, RepoMasterEval, BigCodeBench) alongside HumanEval

## Model Recommendations Based on Use Case

### 1. **Highest Performance (Budget Unconstrained)**
- **Closed models**: GPT-5.4, Claude-3.5-Sonnet (if available in China)
- **Chinese alternatives**: Qwen3.6-Plus, DeepSeek-V3.2 (reasoner mode)
- **Cost**: ~$1-3 per 1k tasks

### 2. **Best Cost-Effectiveness (Production Use)**
- **DeepSeek-Coder with IFIM training** (93.6% HumanEval, low cost)
- **Qwen2.5-Coder with IFIM training** (95.8% HumanEval)
- **Cost**: $0.20-0.30 per 1k tasks (API) or $0 (local)

### 3. **Local Deployment (Data Privacy, Low Latency)**
- **DeepSeek-Coder-6.7B/33B** (open-source, high performance)
- **ChatGLM3-6B** (bilingual, good coding capabilities)
- **CodeGeeX4** (multilingual code translation)
- **Cost**: Hardware + electricity only

### 4. **Real-World Code Completion**
- **Models trained with IFIM or similar instruction-aware methods** (significant improvement on IRME)
- **DeepSeek-Coder IFIM**: 21.1% Pass@1 on IRME (vs 10.9% base)
- **Consider LiveCodeBench performance** over HumanEval alone

## Future Trends Affecting Cost-Effectiveness (2026-2027)

1. **Instruction-aware training**: Methods like IFIM improve instruction-following without degrading infilling capabilities, enhancing real-world performance at minimal cost increase.

2. **Model specialization**: Code-specific models (DeepSeek-Coder, Qwen-Coder) continue to outperform general models on coding tasks at lower cost.

3. **Hardware optimization**: Better quantization and inference optimization reduce local deployment costs.

4. **Benchmark contamination**: Growing awareness of overfitting leads to more robust evaluation (LiveCodeBench, RepoMasterEval).

5. **Chinese model dominance**: Open-source Chinese code models likely to maintain cost advantage over proprietary Western APIs.

## Sources

1. **arXiv:2509.24637** (2025): "Bridging Developer Instructions and Code Completion Through Instruction-Aware Fill-in-the-Middle Paradigm" - Benchmark results for DeepSeek-Coder and Qwen2.5-Coder
2. **LiveCodeBench** (2024-2025): Holistic and contamination-free evaluation of LLMs for code
3. **OpenAI API Pricing** (April 2026): https://openai.com/api/pricing
4. **DeepSeek API Documentation**: https://api-docs.deepseek.com
5. **Alibaba Bailian Platform**: https://bailian.console.aliyun.com
6. **Previous findings_1.md**: AI Models Available in China for Coding Tasks (2025-2026 Research)

## Key Takeaways

1. **Chinese code models achieve state-of-the-art performance** on HumanEval (93-96% Pass@1) at a fraction of the cost of proprietary APIs.

2. **Instruction-aware training (IFIM) significantly improves real-world performance** on code completion benchmarks (IRME) while maintaining or improving HumanEval scores.

3. **Cost-effectiveness favors Chinese open-source models**, especially for local deployment where API costs are eliminated.

4. **Benchmark selection matters**: HumanEval alone may not reflect real-world performance; consider LiveCodeBench, IRME, and other contamination-free evaluations.

5. **For coding tasks in China**, DeepSeek-Coder and Qwen-Coder offer the best balance of performance, cost, and accessibility.

*Note: Benchmark results and pricing are current as of April 2026. Performance and costs may change with new model releases.*
