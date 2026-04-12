# AI Models Available in China for Coding Tasks (2025-2026 Research)

## Overview
This report summarizes major AI models developed in China that are suitable for coding tasks, including code generation, completion, translation, and debugging. The focus is on models accessible to Chinese users, with information on API availability, supported platforms, and official documentation.

## 1. DeepSeek (深度求索)

### Key Facts
- **Developer**: DeepSeek AI (杭州深度求索人工智能基础技术研究有限公司)
- **Latest Models**: DeepSeek-V3.2 (2025-12-01), DeepSeek Coder V2
- **Specialization**: General-purpose AI with strong coding capabilities, multilingual support
- **Training Data**: 2T tokens (87% code, 13% natural language in English and Chinese)
- **Context Window**: Up to 128K tokens
- **License**: Open source (MIT for code, specific license for models)

### API Availability
- **API Platform**: https://platform.deepseek.com
- **API Documentation**: https://api-docs.deepseek.com
- **Base URL**: https://api.deepseek.com
- **Available Models**:
  - `deepseek-chat` (DeepSeek-V3.2, non-thinking mode)
  - `deepseek-reasoner` (DeepSeek-V3.2, thinking mode)

### Pricing (as of 2026)
- **deepseek-chat/deepseek-reasoner**:
  - 1M input tokens (cache hit): $0.028
  - 1M input tokens (cache miss): $0.28
  - 1M output tokens: $0.42
- **Context Length**: 128K
- **Max Output**: 4K-8K (chat), 32K-64K (reasoner)

### Supported Platforms
- Web interface: https://chat.deepseek.com
- Mobile app available
- VS Code extensions and other IDE integrations
- OpenAI-compatible API

### Coding-Specific Models
- **DeepSeek-Coder**: Series of code-specific models (1B, 5.7B, 6.7B, 33B parameters)
- **Training**: Project-level code corpus with 16K window size, fill-in-the-blank tasks
- **Languages**: Supports 87+ programming languages
- **Performance**: State-of-the-art on HumanEval, MultiPL-E, MBPP, DS-1000, APPS benchmarks

### Official Resources
- Website: https://www.deepseek.com
- GitHub: https://github.com/deepseek-ai
- DeepSeek-Coder: https://github.com/deepseek-ai/DeepSeek-Coder
- Documentation: https://api-docs.deepseek.com

## 2. Qwen (通义千问) - Alibaba

### Key Facts
- **Developer**: Alibaba Cloud (阿里云)
- **Latest Models**: Qwen3.6-Plus (2026), Qwen3.5-Omni, Qwen3-Coder-Next
- **Specialization**: Multimodal models with strong coding capabilities
- **Training**: Large-scale multilingual training with emphasis on Chinese and English
- **Context Window**: Up to 128K (Qwen3.5-128K)

### API Availability
- **Platform**: Alibaba Cloud Bailian (百炼) - https://bailian.console.aliyun.com
- **API Access**: Through Dashscope platform
- **Models Available**: Qwen3.6-Plus, Qwen3.5-Omni, Qwen3-Coder-Next, Qwen3-VL series
- **Free Tier**: New users get over 70 million free tokens (90-day validity)

### Pricing
- **Qwen3.6-Plus**: Pricing varies based on model size and features
- **Qwen3.5-Turbo**: Competitive pricing for general use
- **Customizable**: Resource packages and savings plans available
- Detailed pricing on Alibaba Cloud Bailian platform

### Supported Platforms
- Alibaba Cloud console
- Web interface: https://chat.qwen.ai
- API integration via Dashscope
- Various enterprise deployment options

### Coding-Specific Models
- **Qwen3-Coder-Next**: 80B parameter model specialized for code generation
- **Features**: Strong performance on coding benchmarks, support for multiple programming languages
- **Qwen3.5-Coder**: Previous generation coding models
- **Integration**: Available on Hugging Face and ModelScope

### Official Resources
- Official site: https://qwen.ai
- GitHub: https://github.com/QwenLM
- Hugging Face: https://huggingface.co/Qwen
- Bailian platform: https://bailian.console.aliyun.com
- Documentation: https://help.aliyun.com/product/230218.html

## 3. GLM/ChatGLM (智谱清言) - Zhipu AI

### Key Facts
- **Developer**: Zhipu AI (智谱AI) & Tsinghua KEG
- **Latest Models**: GLM-4 series (2026), ChatGLM3-6B
- **Specialization**: Bilingual (Chinese/English) dialogue models with coding capabilities
- **Training**: Extensive training on Chinese and English corpora
- **Open Source**: ChatGLM3-6B, ChatGLM3-6B-Base, ChatGLM3-6B-32K, ChatGLM3-6B-128K

### API Availability
- **API Platform**: https://open.bigmodel.cn (智谱AI开放平台)
- **Available Models**: GLM-4, GLM-4-air, GLM-4-airx, GLM-4-flash, GLM-3-Turbo, CharacterGLM-3
- **Features**: System Prompt, Function Call, Retrieval, Web Search support

### Pricing
- **GLM-4 series**: Tiered pricing based on model and usage
- **GLM-3-Turbo**: Lower-cost option for general tasks
- Free trial available with limited tokens
- Enterprise pricing upon request

### Supported Platforms
- Web interface: https://chatglm.cn
- Mobile apps
- API integration
- Local deployment for open-source models

### Coding Capabilities
- **ChatGLM3-6B**: Strong performance on coding benchmarks (GSM8K: 72.3, MATH: 25.7, MBPP: 52.4)
- **Features**: Tool calling, code execution, Agent tasks support
- **Context**: Up to 128K tokens (ChatGLM3-6B-128K)
- **Fine-tuning**: Support for custom fine-tuning

### Official Resources
- Official site: https://chatglm.cn
- GitHub: https://github.com/THUDM/ChatGLM3
- GLM-4: https://github.com/THUDM/GLM-4
- API docs: https://open.bigmodel.cn/dev/api
- Hugging Face: https://huggingface.co/THUDM

## 4. CodeGeeX - Tsinghua & Zhipu AI

### Key Facts
- **Developer**: Tsinghua KEG & Zhipu AI
- **Latest Models**: CodeGeeX4 (最新一代), CodeGeeX2 (2023-07-24), CodeGeeX (13B)
- **Specialization**: Multilingual code generation model
- **Training**: 13B parameters, trained on 850B+ tokens across 20+ programming languages
- **Open Source**: Model weights available for research

### API Availability
- **Online Demo**: https://models.aminer.cn/codegeex
- **VSCode Extension**: Available in marketplace
- **JetBrains Plugin**: Supported for IntelliJ IDEA, PyCharm, etc.
- **Cloud Studio**: Web IDE integration

### Pricing
- **Free**: Open-source models available for download
- **Online Services**: Free access with limitations
- **Enterprise**: Custom deployment options

### Supported Platforms
- VS Code extension
- JetBrains IDEs (IntelliJ, PyCharm, GoLand, CLion, etc.)
- Cloud Studio (Tencent's web IDE)
- Local deployment via Hugging Face

### Coding Capabilities
- **Multilingual Generation**: Python, C++, Java, JavaScript, Go, and more
- **Crosslingual Translation**: Convert code between programming languages
- **HumanEval-X Benchmark**: 820 human-crafted problems across 5 languages
- **Features**: Code completion, explanation, summarization

### Official Resources
- Official site: https://codegeex.cn
- GitHub: https://github.com/THUDM/CodeGeeX
- CodeGeeX4: https://github.com/THUDM/CodeGeeX4
- Paper: https://arxiv.org/abs/2303.17568
- Hugging Face: https://huggingface.co/datasets/THUDM/humaneval-x

## 5. Other Notable Models

### Baidu ERNIE Code (文心代码)
- **Developer**: Baidu
- **Status**: Part of Baidu's ERNIE family
- **Access**: Through Baidu AI Cloud platform
- **Features**: Code generation and understanding
- **Note**: Limited public information compared to other models

### Inspur Yuan (浪潮源)
- **Developer**: Inspur
- **Focus**: Enterprise AI solutions
- **Coding Support**: General AI with coding capabilities
- **Access**: Primarily through enterprise partnerships

### 360 Zhinao (360智脑)
- **Developer**: 360 (Qihoo 360)
- **Features**: General AI with coding support
- **Access**: Through 360's ecosystem

## Comparison Summary

| Model | Developer | Open Source | API Available | Coding Specialization | Context Window | Key Features |
|-------|-----------|-------------|---------------|----------------------|----------------|--------------|
| DeepSeek Coder | DeepSeek AI | Yes | Yes | High | 16K-128K | Project-level completion, 87+ languages |
| Qwen3-Coder-Next | Alibaba | Yes | Yes | High | 128K | 80B params, strong benchmarks |
| ChatGLM3-6B | Zhipu AI | Yes | Yes | Medium-High | 8K-128K | Bilingual, tool calling, code execution |
| CodeGeeX4 | Tsinghua/Zhipu | Yes | Limited | High | 2K+ | Multilingual generation, translation |
| GLM-4 | Zhipu AI | Partial | Yes | Medium | 128K+ | Latest generation, function calling |

## Access Considerations for Chinese Users

### 1. API Access
- All major models offer API access through their respective platforms
- Registration typically requires Chinese phone number or business credentials
- Pricing competitive with international alternatives
- Free tiers available for testing

### 2. Local Deployment
- Open-source models (DeepSeek-Coder, ChatGLM3-6B, CodeGeeX) can be deployed locally
- Hardware requirements vary (6GB+ VRAM for smaller models)
- Support for NVIDIA and Ascend platforms

### 3. IDE Integrations
- VS Code extensions available for most models
- JetBrains plugin support growing
- Cloud IDE integrations (Tencent Cloud Studio, Alibaba Cloud IDE)

### 4. Compliance and Regulations
- Models comply with Chinese AI regulations
- Content filtering built-in for sensitive topics
- Data residency options for enterprise users

## Recommendations for Coding Tasks

1. **For General Coding Assistance**: DeepSeek Chat API or Qwen3.6-Plus
2. **For Code Generation Specialization**: DeepSeek-Coder or Qwen3-Coder-Next
3. **For Local Deployment**: ChatGLM3-6B or DeepSeek-Coder-6.7B
4. **For Multilingual Projects**: CodeGeeX4 for translation between languages
5. **For Enterprise Integration**: Alibaba Bailian or Zhipu API platforms

## Future Trends (2025-2026)

1. **Increased Context Windows**: 128K+ becoming standard
2. **Specialized Coding Models**: More fine-tuned variants for specific languages/frameworks
3. **Tool Integration**: Better IDE and development tool integration
4. **Multimodal Coding**: Integration of code with images, diagrams, and documentation
5. **Agent Capabilities**: Autonomous coding agents with planning and execution

## Sources

1. DeepSeek Official Site: https://www.deepseek.com
2. DeepSeek API Docs: https://api-docs.deepseek.com
3. Alibaba Bailian Platform: https://bailian.console.aliyun.com
4. Qwen GitHub: https://github.com/QwenLM
5. ChatGLM3 GitHub: https://github.com/THUDM/ChatGLM3
6. Zhipu AI Open Platform: https://open.bigmodel.cn
7. CodeGeeX Official Site: https://codegeex.cn
8. CodeGeeX GitHub: https://github.com/THUDM/CodeGeeX
9. Research Papers and Technical Documentation (2024-2026)

*Note: Information current as of April 2026. Pricing and features subject to change.*
