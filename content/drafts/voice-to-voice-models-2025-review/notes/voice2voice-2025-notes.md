

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



Gemini Deepreserch report: https://gemini.google.com/app/6323f0641eff5860



https://tincans.ai/report - This post describes Tincans' research in pursuit of a real-time AI voice system, largely performed from January to April 2024. We detail four main contributions and release code for each component.