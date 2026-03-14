# AI大模型评测数据

本目录包含从DataLearnerAI大模型评测榜单爬取的模型信息。

## 数据来源
- 网站: https://www.datalearner.com/leaderboards
- 数据更新时间: 2025/11/08 22:10:24

## 包含的模型文件

1. [OpenAI o1](./OpenAI_o1.md) - 排名第1
2. [Gemini 3.0 Pro (Preview 11-2025)](./Gemini_3.0_Pro.md) - 排名第2
3. [Claude Opus 4.5](./Claude_Opus_4.5.md) - 排名第3
4. [Qwen3.5-397B-A17B](./Qwen3.5-397B-A17B.md) - 排名第7
5. [DeepSeek V3.2-Exp](./DeepSeek_V3.2-Exp.md) - 排名第18
6. [GPT-4.5](./GPT-4.5.md) - 排名第11
7. [GLM-4.5](./GLM-4.5.md) - 排名第22
8. [Kimi K2 Thinking](./Kimi_K2_Thinking.md) - 排名第23
9. [Llama 4 Behemoth Instruct](./Llama_4_Behemoth_Instruct.md) - 排名第34
10. [GPT-4o](./GPT-4o.md) - 排名第56

## 文件格式
每个模型文件包含以下信息：
- 基本信息（排名、模型名称、参数数量、开源情况）
- 评测分数（MMLU Pro、GPQA Diamond、SWE-bench Verified、MATH-500、AIME 2024、LiveCodeBench）
- 模型简介
- 数据来源

## 评测基准说明
1. **MMLU Pro**: 大规模多任务语言理解专业版
2. **GPQA Diamond**: 研究生水平物理问答
3. **SWE-bench Verified**: 软件工程基准测试
4. **MATH-500**: 数学问题求解
5. **AIME 2024**: 美国数学邀请赛2024
6. **LiveCodeBench**: 实时编程能力测试