

References and materials: 

https://ravinkumar.com/GenAiGuidebook/audio/audio_tokenization.html#audio-tokenization-acoustic-tokens-neural-compression 
good introduction to audio tokenization, 

Current speech LMs utilize two primary audio tokenization methods: **Acoustic Tokens**, which focus on sound patterns, and **Semantic Tokens**, which emphasize meaning. However, it's important to note that these categories are not mutually exclusive, and some methods may capture both acoustic and semantic properties to varying degrees.

### Comparison of Acoustic and semantic Tokens

| **Aspect** | **Acoustic Tokens** | **Semantic Tokens** |
| ---| ---| --- |
| **Focus** | Low-level acoustic properties | High-level semantic information |
| **Objective** | Efficient compression and reconstruction | Capturing meaningful audio units |
| **Training Approach** | Often unsupervised or self-supervised | Typically self-supervised on large datasets |
| **Interpretability** | Generally less interpretable | Can be more interpretable (e.g., phoneme-like units) |
| **Downstream Tasks** | Better for generation and reconstruction | Better for classification and understanding tasks |
| **Cross-modal Alignment** | Less suitable | More suitable for alignment with text or other modalities |
| **Compression Efficiency** | Usually higher | Can be lower, as semantic information is prioritized |
| **Robustness to Noise** | Often more sensitive to acoustic variations | Can be more robust to minor acoustic changes |
| **Language Dependency** | Generally language-independent | May capture language-specific features |



## Deep reserach reports

* Gemini Deepreserch report v1: https://gemini.google.com/app/6323f0641eff5860
* Gemini Deepreserch report v2: https://gemini.google.com/app/6323f0641eff5860



https://tincans.ai/report - This post describes Tincans' research in pursuit of a real-time AI voice system, largely performed from January to April 2024. We detail four main contributions and release code for each component.


publications: 

1. Moshi: a speech-text foundation model for real-time dialogue https://arxiv.org/pdf/2410.00037 github:  https://github.com/kyutai-labs/moshi
2. Qwen2.5-Omni Technical Report https://arxiv.org/abs/2503.20215
3. Ultravox - https://github.com/fixie-ai/ultravox
4.  Recent Advances in Speech Language Models: A Survey https://arxiv.org/pdf/2410.03751v3, 8.08 2025
5.  MiniCPM-o 2.6 - technical report, blog post https://openbmb.notion.site/MiniCPM-o-2-6-A-GPT-4o-Level-MLLM-for-Vision-Speech-and-Multimodal-Live-Streaming-on-Your-Phone-185ede1b7a558042b5d5e45e6b237da9 - describe end-to-end multimodal model for audio input and output streaming, audio encoder based on Whisper, audio decoder is auto-regressinve lightweight model initialized from ChatTTS (jointly models speech embeddings, text tokens and audio tokens) MiniCPM-o 2.6 is the latest and most capable model in the MiniCPM-o series. The model is built in an end-to-end fashion based on SigLip-400M, Whisper-medium-300M, ChatTTS-200M, and Qwen2.5-7B with a total of 8B parameters
6.  