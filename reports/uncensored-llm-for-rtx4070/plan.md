# Research Plan: Uncensored LLMs for RTX 4070 (12GB VRAM)

## Main Research Question
What are the best uncensored/open-weight LLMs that can run effectively on an NVIDIA RTX 4070 (12GB VRAM) for self-hosting?

## Hardware Context
- NVIDIA GeForce RTX 4070 (12GB VRAM)
- Shared GPU memory: ~16GB (total ~28GB)
- DirectX 12, driver version 32.0.15.9186 (Jan 2026)

## Subtopic 1: Top Uncensored LLM Models for 12GB VRAM
Which uncensored/open-weight models (e.g., Dolphin, NousResearch, Yi, Mistral, Llama-based) fit in 12GB VRAM at various quantization levels (4-bit, 6-bit, 8-bit). What are their strengths and parameter sizes (7B, 13B, 30B)?

## Subtopic 2: Performance and Quality on RTX 4070
How do these uncensored models perform on RTX 4070 class hardware? Speed (tokens/sec), quality benchmarks, context window sizes that fit, and practical usability for conversation/coding/writing tasks.

## Synthesis Plan
Compare models across: VRAM fit, inference speed, uncensoring quality, ease of setup, and practical use cases. Produce a ranked recommendation.
