---
title: "🛠️ 2025 modern setup for AI-powered blogging with Hugo, Github pages, and Cursor.ai"
date: 2025-08-27
lastmod: 2025-08-28T21:00:00Z
draft: false
description: "A detailed guide to my personal blogging setup, from local development with Hugo and the Congo theme to automated deployment with GitHub Actions and AI-assisted content creation with Cursor."
slug: "ai-powered-hugo-blogging-workflow"
tags: ["Hugo", "AI", "Workflow", "Blogging", "GitHub", "Congo Theme", "Cursor"]
---

## Finding the Right Tools for My Blog

If you've read my [blog manifesto](/posts/blog-manifesto/), you'll know that transparency and sharing my journey are core values for me. In that spirit, I want to pull back the curtain on my technical setup and share the workflow I've developed for this blog.

When I started, I had a clear set of requirements for my blogging platform:

*   **Simplicity:** I wanted a setup that was easy to maintain without the hassle of managing databases, hosting platforms, or complex plugin ecosystems.
*   **Efficiency:** The publishing process needed to be straightforward, allowing me to focus on content rather than formatting and styling.
*   **AI Integration:** A crucial requirement was the ability to seamlessly use AI as a writing companion for drafting, editing, and brainstorming. The process of preparing context for AI models had to be simple.
*   **Flexibility:** I wanted the freedom to experiment with different AI models and even explore agentic workflows for more complex tasks like research and paper summarization.
*   **Modern Aesthetics:** The platform needed to look clean, modern, and have access to a good selection of themes.

## Platform Evaluation: My Path to Hugo

I considered several popular options before landing on my current stack:

*   **Obsidian, Sync, and Vercel:** This was a tempting option. While setting up a digital garden with Obsidian and deploying it via Vercel was relatively easy, I found integrating AI to be cumbersome, I have tried the paid version of [Obsidian Copilot](https://www.obsidiancopilot.com/en), it was ok, but it felt like there were too many moving parts for the simple workflow I was aiming for.
*   **Medium or Substack:** These platforms are simple, but they are "walled gardens." I wanted full ownership of my content and the using AI was not so straight forward, I could use seperate AI chats, but this was not I wanted.
*   **MkDocs with Material Theme:** I have a soft spot for [MkDocs Material](https://squidfunk.github.io/mkdocs-material/), having used it to build the [PyTorch course website](https://pytorchcourse.com/). It's excellent and markdown-native, which is great for AI workflows. However, the performance was a sticking point. Build times of 6-9 minutes felt too slow and hindered a rapid, iterative writing process.
*   **Hugo:** When I came across [Hugo](https://gohugo.io/), what caught my attention was its reputation for speed. I decided to give it a try, and the performance was a significant factor in my decision. Local builds are nearly instantaneous, providing a real-time feedback loop that has transformed my writing process. Paired with the clean, modern, and highly configurable [Congo theme](https://jpanther.github.io/congo/docs/), I felt I had found a setup that met my requirements.
  

{{< figure src="notes/hugo-fast-rebuilding.png" alt="Hugo fast page rebuild after edit" caption="Hugo fast page rebuild after edit" >}}

## A Closer Look at My Hugo and Congo Setup

Getting started with Hugo is straightforward. You can follow the official [Hugo installation guide](https://gohugo.io/getting-started/installing/) to install the "Extended" version. As a Windows 11 user, I used the [Chocolatey](https://chocolatey.org/) package manager for a one-line installation.

I installed the Congo theme as a [git submodule](https://jpanther.github.io/congo/docs/installation/#install-using-git), which makes it easy to keep the theme updated.

One of the interesting things about the Congo theme is its approach to configuration. Instead of a single monolithic `hugo.toml` file, it splits the configuration into logical parts within the [`config/_default`](https://github.com/ksopyla/ksopyla-ai-blog/tree/main/config/_default) directory. I find this approach much cleaner and easier to maintain.

Here’s a quick breakdown of the configuration files:

*   [`hugo.toml`](https://github.com/ksopyla/ksopyla-ai-blog/blob/main/config/_default/hugo.toml): The main configuration file for the site.
*   [`languages.en.toml`](https://github.com/ksopyla/ksopyla-ai-blog/blob/main/config/_default/languages.en.toml): Contains blog and author descriptions, social links, and supports multi-language setups.
*   [`markup.toml`](https://github.com/ksopyla/ksopyla-ai-blog/blob/main/config/_default/markup.toml): Configures the Markdown parser for features like table of contents, code highlighting, and LaTeX support.
*   [`menus.en.toml`](https://github.com/ksopyla/ksopyla-ai-blog/blob/main/config/_default/menus.en.toml): Defines the navigation menus, including the main menu, search, and footer links.
*   [`module.toml`](https://github.com/ksopyla/ksopyla-ai-blog/blob/main/config/_default/module.toml): Handles Hugo modules configuration. I've left this with its default settings.
*   [`params.toml`](https://github.com/ksopyla/ksopyla-ai-blog/blob/main/config/_default/params.toml): This is where you customize the theme's appearance and features, such as color schemes, dark mode, search functionality, and image optimizations.

### Automated Deployment with GitHub Actions

The entire blog is hosted on GitHub Pages, and the deployment process is fully automated using a [GitHub Actions workflow](https://github.com/ksopyla/ksopyla-ai-blog/blob/main/.github/workflows/hugo-deployment.yml). Most of this workflow was generated by an AI, and I just tweaked a few parameters to fit my needs. Every time I push a change to the `main` branch, the action automatically builds the site with Hugo and deploys it.

## My AI-Assisted Content Workflow

My primary development environment is Cursor, which puts a powerful AI assistant right inside my editor. This is the cornerstone of my content creation process.

We all know that AI isn't a magic bullet. It can't read your mind or generate perfect, nuanced content from a simple prompt. It's a tool that needs guidance, context, and high-quality source material to shine. My workflow is designed around this principle.

For each post, located in `content/posts`, I create a `notes` subfolder. This folder is my private scratchpad where I dump raw ideas, interesting quotes, links to research papers, and rough observations. These markdown notes are messy and unstructured, but they serve as the perfect, rich context for the AI. When it's time to write, I can feed these notes to my AI assistant and ask it to help me draft, refine, and structure the final article. Often I put there the [prompts form the AI chat for further use and reference](https://github.com/ksopyla/ksopyla-ai-blog/tree/main/content/posts/hugo-blog-ai-workflow/notes).

My [Cursor rules are defined in my repository](https://github.com/ksopyla/ksopyla-ai-blog/tree/main/.cursor/rules), and my go-to model is currently `gemini-2.5-pro`. I find it fits my writing style well—it's not overly verbose and follows instructions precisely without overusing tools.

## Additional Tools in My Workflow

Beyond the core stack, I use a couple of other tools:

*   **Umami:** For analytics, I chose [Umami](https://umami.is/) because it's a privacy-first tool that gives me the insights I need without collecting personal data from my visitors. Thats why my [privacy policy](/privacy-policy/) is so simple
*   **Midjourney:** All the featured images on this blog are generated with Midjourney. I've developed a specific profile to create abstract images that maintain a consistent style across all posts.
*   **Giscus:** For comments, I'm using [Giscus](https://giscus.app/), a system built on GitHub Discussions. It is easy to setup and was a natural fit for audience of this blog. 

## Final Thoughts and Observations

After several weeks of using this workflow, a few things have become clear:

*   **Speed is a Feature:** I initially underestimated the importance of build speed. Hugo's instant feedback loop allows me to iterate on content much faster, which has significantly improved my writing process.
*   **AI as a Companion:** Treating AI as a collaborator rather than a content generator is the key. By providing it with well-researched notes and clear guidance, it becomes an invaluable assistant for polishing and structuring my thoughts.

This entire setup is open-source, and you can explore the full configuration in the [ksopyla-ai-blog GitHub repository](https://github.com/ksopyla/ksopyla-ai-blog). I hope this deep dive into my workflow has been helpful. If you have any questions or suggestions, feel free to reach out!







