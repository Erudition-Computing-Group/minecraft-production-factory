# LLM stack — which model runs which agent

Each agent has a different workload, so route simple formatting to fast/cheap models and reserve heavy
reasoning models for 3D math and Java compilation. Keeps the pipeline fast and cost-effective.

## Local / open-weight stack (Ollama or LM Studio) — $0/month

| Agent | Model | Why |
|-------|-------|-----|
| Concept & Spec | `gemma4:12b` or `llama4:scout` | Brainstorm + clean structured JSON. |
| Math & Geometry | `qwen3:27b` or `deepseek-r1:14b` | Step-by-step "thinking" for parametric equations, Bezier curves, rotation matrices. |
| Builder (Java/Bedrock) | `devstral-small-2` (24B) or `qwen3-coder:30b` | Purpose-built for multi-file agentic coding; MoE with only 3.3B active params. |
| QA & Performance | `gpt-oss:20b` or `qwen3:27b` | Deep logic tracing, Gradle/Maven stack traces, root-cause isolation. |
| Storefront & Ops | `gemma4:12b` | Lightweight text generation for Tebex descriptions + markdown. |

Hardware note: 24B–30B models need ~16–24 GB VRAM or 32 GB unified memory. On tighter hardware drop
heavy slots to `gemma4:12b` or `deepseek-r1:14b`.

## Cloud / frontier API stack — max accuracy

| Agent | Model | Why |
|-------|-------|-----|
| Concept & Storefront | Claude Sonnet (fast mini-tier) | High throughput, cheap per token, strict JSON schema adherence. |
| Math & Geometry | GPT-6.1 Sol (or GPT-6 Astra for complex shapes) | Top-tier scientific/math reasoning for 3D coordinates. |
| Builder & QA | Claude Opus 5.5 / Claude Sonnet 5.5 | Lead agentic coding + terminal-use benchmarks (SWE-bench Pro, OSWorld). |
| High-volume budget alt. | DeepSeek-V4-Pro | Strong coding + math at a fraction of Western frontier cost. |

## Crucial tip for the Math Agent

Give it a **Python interpreter tool** (numpy/scipy). Never let it guess `(x,y,z)` coordinates of a double helix
or flapping wing in its head — have it write a quick script to calculate and sanity-check the bounding box and
particle density before handing formulas to the Builder.

## Cost per batch

A typical batch of 20 particle effects (spec + math + Java compile) consumes ~1–3M tokens → $5–$20 on cloud APIs.
Local stack: $0.
