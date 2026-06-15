---
name: opencli-bilibili-research-video-router
description: Router for Bilibili creator video-map skills maintained through `opencli`. Use when the user wants a curated checklist of videos from a specific creator about bioinformatics, AI skills, plotting, research methods, or adjacent learning workflows and you need to choose the right creator-specific skill.
---

# opencli-bilibili-research-video-router

Use this router when the user asks for videos from a named Bilibili creator and the goal is to fetch or refresh a curated creator-specific skill instead of doing a one-off ad hoc search.

## Creator Skills

- `huage-bioinfo-video-catalog`
- `opencli-omics-lecture-hall-bioinfo-videos`
- `opencli-wangyao-adong-bioinfo-videos`
- `opencli-purplepotato-bioinfo-videos`
- `opencli-mango-bioinfo-videos`
- `opencli-ai-ghost-lab-ai-skills`
- `opencli-sanzhuang-bioinfo-videos`
- `opencli-onekeyai-bioinfo-videos`
- `opencli-waike-xiaoxiaoshuo-ai-plotting-research-videos`
- `opencli-yangyarenjia-bioinfo-ai-videos`

## Routing guidance

- Use `opencli-ai-ghost-lab-ai-skills` for AI coding workflow, skills, prompts, AGENTS, Codex, or project-evolution topics.
- Use `opencli-waike-xiaoxiaoshuo-ai-plotting-research-videos` for plotting, AI-assisted medical research workflow, or research-method videos from 外科小小硕.
- Use `opencli-yangyarenjia-bioinfo-ai-videos` when the user wants AI-for-research, DeepSeek, office productivity, or broader science-workflow talks from 养鸭人家.
- Use the bioinformatics leaf skills for creator-specific learning catalogs:
  - `huage-bioinfo-video-catalog`
  - `opencli-omics-lecture-hall-bioinfo-videos`
  - `opencli-wangyao-adong-bioinfo-videos`
  - `opencli-purplepotato-bioinfo-videos`
  - `opencli-mango-bioinfo-videos`
  - `opencli-sanzhuang-bioinfo-videos`
  - `opencli-onekeyai-bioinfo-videos`
- Use `opencli-learning-content-router` as the broader parent entry when the user has not yet decided between Bilibili and Weixin source collections.

## Maintenance

- Keep creator-specific curation logic in the leaf skills.
- Refresh a leaf skill with its own `scripts/refresh_index.py`.
- Use this router as the source-specific child router for the opencli Bilibili skill family.
