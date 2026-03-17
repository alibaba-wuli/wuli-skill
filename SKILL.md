---
name: wuli
description: Generate AI images and videos with 15+ models via Wuli.art open platform API. Use when creating images from text prompts, editing or modifying existing images with AI, generating videos from text descriptions, animating static images into videos, batch generating artwork, or choosing between models like Qwen Image, Seedream, Wan Xiang, Kling, Seedance, and MiniMax Hailuo. Covers text-to-image, image-to-image, text-to-video, image-to-video, prompt optimization, and no-watermark downloads.
version: 1.0.1
author: sir1st
metadata: {"clawdbot":{"emoji":"🎨","requires":{"anyBins":["python3"]},"os":["linux","darwin","win32"]}}
tags:
  - ai
  - image-generation
  - video-generation
  - text-to-image
  - text-to-video
  - image-to-video
  - image-editing
  - art
  - creative
  - wuli
triggers:
  - generate image
  - generate video
  - text to image
  - text to video
  - image to video
  - AI art
  - edit image
  - create artwork
  - animate image
  - wuli
---

# Wuli Platform — AI Image & Video Generation

Generate AI images and videos via the [Wuli.art](https://wuli.art) open platform API. Supports text-to-image, image editing, text-to-video, and image-to-video across 15+ models including Qwen Image, Seedream, Wan Xiang (通义万相), Kling (可灵), Seedance, and MiniMax Hailuo — with automatic no-watermark downloads.

## When to Use

- User wants to generate images from a text description
- User wants to edit or transform an existing image with AI
- User wants to create video from a text prompt
- User wants to animate a static image into a video
- User needs high-resolution (up to 4K) AI artwork
- User wants batch generation (up to 4 images at once)
- User needs to choose between multiple AI models for best results

## Setup

```bash
export WULI_API_TOKEN="wuli-your-token-here"
```

Get your token: log in to [wuli.art](https://wuli.art), click the **API entry** at the bottom-left corner.

No additional dependencies — uses only Python 3 standard library.

## Quick Start

```bash
# Generate an image (simplest usage)
python3 skill.py --action image-gen --prompt "a serene mountain lake at sunrise"

# Generate a video
python3 skill.py --action txt2video --prompt "waves crashing on a golden beach at sunset"
```

## Complete Command Reference

```bash
python3 skill.py --action <action> --prompt "description" [options]
```

### Actions

| Action | Description | Image Required |
|---|---|---|
| `image-gen` | Text to image | No |
| `image-edit` | Edit/transform image with prompt | Yes (`--image_url` or `--image_path`) |
| `txt2video` | Text to video | No |
| `image2video` | Animate image into video | Yes (`--image_url` or `--image_path`) |

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `--prompt` | *(required)* | Generation prompt, max 2000 chars |
| `--model` | auto-selected | Model name (see Model Selection Guide) |
| `--aspect_ratio` | 1:1 (image) / 16:9 (video) | Aspect ratio |
| `--resolution` | 2K (image) / 720P (video) | Output resolution |
| `--n` | 1 | Number of images to generate (1-4, image-gen only) |
| `--image_url` | — | Reference image URL (for edit/animate) |
| `--image_path` | — | Local file path, auto-uploaded (for edit/animate) |
| `--duration` | 5 | Video length in seconds |
| `--negative_prompt` | — | Exclude unwanted elements |
| `--optimize` | false | Enable AI prompt optimization (flag) |

### Aspect Ratios

| Ratio | Use Case |
|---|---|
| `1:1` | Square — social media posts, avatars, icons |
| `16:9` | Widescreen — videos, desktop wallpapers, presentations |
| `9:16` | Vertical — phone wallpapers, stories, reels |
| `4:3` | Classic — photos, prints |
| `3:2` | Photography — DSLR-style landscape shots |
| `21:9` | Ultra-wide — cinematic banners (image only) |

## Model Selection Guide

### Image Models — Which to Choose

| Model | Best For | Resolution | Ref Images | Cost |
|---|---|---|---|---|
| **Qwen Image 2.0** *(default)* | General purpose, fast, versatile | 2K, 4K | 4 | 1 credit |
| Qwen Image Turbo | Quick drafts, iterations | 2K, 4K | 4 | 1 credit |
| Qwen Image 25.08 | Text-only generation, latest quality | 2K, 4K | 0 | 1 credit |
| Seedream 4.5 | Photorealism, high-fidelity detail | 2K, 4K | 8 | 4 credits |
| Seedream 4.0 | Multi-resolution photorealism | 1K–4K | 8 | 4 credits |
| 通义万相 2.6 | Chinese-style art, specific aesthetics | 1K | 4 | 4 credits |

**Recommendations:**
- **Fastest & cheapest**: Qwen Image Turbo (1 credit, fast inference)
- **Best quality for photos**: Seedream 4.5 (photorealistic, 4 credits)
- **Best all-rounder**: Qwen Image 2.0 (default, supports both text and edit)
- **Need 4K**: Qwen Image 2.0 or Seedream 4.5 with `--resolution 4K`

### Video Models — Which to Choose

| Model | Best For | Resolution | Duration | Cost |
|---|---|---|---|---|
| **通义万相 2.2 Turbo** *(default)* | Quick videos, low cost | 720P | 5s | 20 credits |
| 通义万相 2.6 | High quality, long videos, multi-mode | 720P–1080P | 5–15s | 40–180 |
| 通义万相 2.6 Flash | Fast image-to-video | 720P–1080P | 5–15s | 20–120 |
| 可灵 O1 | Premium quality, all modes | 720P–1080P | 5–10s | 40–160 |
| 可灵 2.6 | Top-tier 1080P video | 1080P | 5–10s | 60–120 |
| 可灵 2.5 Turbo | Balanced quality/speed | 720P–1080P | 5–10s | 40–80 |
| Seedance 1.5 Pro | Dance/motion, up to 12s | 480P–720P | 5–12s | 20–100 |
| Seedance 1.0 Pro | Full resolution range | 480P–1080P | 5–10s | 20–160 |
| MiniMax Hailuo 2.3 | Cinematic quality | 768P–1080P | 6–10s | 40–120 |
| MiniMax Hailuo 2.3 Fast | Fast image-to-video | 768P–1080P | 6–10s | 20–80 |

**Recommendations:**
- **Fastest & cheapest**: 通义万相 2.2 Turbo (default, 20 credits for 5s)
- **Best quality**: 可灵 O1 or 可灵 2.6
- **Longest video**: 通义万相 2.6 (up to 15s) or Seedance 1.5 Pro (up to 12s)
- **Best for 1080P**: 可灵 2.6 or MiniMax Hailuo 2.3

## Examples

### Text to Image

```bash
# Simple generation
python3 skill.py --action image-gen --prompt "anime girl with blue hair in a garden"

# Batch generate 4 images to pick the best
python3 skill.py --action image-gen --prompt "cyberpunk cityscape at night" --n 4

# Photorealistic with premium model
python3 skill.py --action image-gen --prompt "photorealistic mountain landscape, golden hour" \
  --model "Seedream 4.5" --resolution 4K --aspect_ratio 16:9

# Vertical phone wallpaper
python3 skill.py --action image-gen --prompt "ethereal forest with fireflies" \
  --aspect_ratio 9:16 --resolution 4K

# With prompt optimization (AI enhances your prompt)
python3 skill.py --action image-gen --prompt "a cat" --optimize
```

### Image Editing

```bash
# Edit a local image
python3 skill.py --action image-edit --prompt "add sunglasses and a hat" \
  --image_path ./photo.jpg

# Edit a remote image
python3 skill.py --action image-edit --prompt "change background to sunset beach" \
  --image_url "https://example.com/photo.jpg"

# Style transfer
python3 skill.py --action image-edit --prompt "convert to oil painting style" \
  --image_path ./landscape.jpg --model "Seedream 4.5"
```

### Text to Video

```bash
# Simple video
python3 skill.py --action txt2video --prompt "waves crashing on a golden beach at sunset"

# Longer duration with higher quality
python3 skill.py --action txt2video --prompt "a cat playing piano in a jazz club" \
  --model "通义万相 2.6" --duration 10 --resolution 1080P

# Cinematic quality
python3 skill.py --action txt2video --prompt "slow-motion rain drops on a window" \
  --model "可灵 O1" --resolution 1080P --aspect_ratio 16:9
```

### Image to Video (Animate)

```bash
# Animate a landscape photo
python3 skill.py --action image2video --prompt "slow zoom in with gentle wind blowing" \
  --image_path ./landscape.jpg --duration 5

# Animate from URL with premium model
python3 skill.py --action image2video --prompt "character turns head and smiles" \
  --image_url "https://example.com/portrait.jpg" --model "可灵 O1"
```

## Workflow

```
1. (Optional) Upload reference image
   --image_path ./photo.jpg  → auto-uploaded to cloud storage
   --image_url https://...   → auto-downloaded and re-uploaded

2. Submit generation task
   → Returns recordId for tracking

3. Auto-poll for completion
   → Images: polls every 5s (up to 5 min)
   → Videos: polls every 10s (up to 20 min)

4. Auto-download results
   → Fetches no-watermark version when available
   → Saves to current directory
   → Auto-opens on macOS/Linux/Windows
```

## Troubleshooting

- **"WULI_API_TOKEN not set"**: Run `export WULI_API_TOKEN="wuli-your-token"`. Get your token from [wuli.art](https://wuli.art) bottom-left corner → API. The token is sent as `Authorization: Bearer <token>`.
- **"HTTP 401"**: Token is invalid or expired. Regenerate it on the wuli.art platform.
- **"HTTP 429"**: Rate limited. Wait a few seconds and retry.
- **"Error code 2001"**: Insufficient credits. Top up at [wuli.art](https://wuli.art).
- **"REVIEW_FAILED"**: Content moderation rejected the prompt. Rephrase to avoid sensitive content.
- **"TIMEOUT"**: Generation took too long. Try a faster model (Turbo variants) or shorter duration.
- **Image upload fails**: Check file format — supported: jpg, jpeg, png, webp. For video: mp4, mov, avi, webm.

## Tips

- Use `--optimize` to let AI enhance your prompt for better results — especially useful for short/vague prompts.
- Start with the default models (Qwen Image 2.0 / 通义万相 2.2 Turbo) — they're the cheapest and fastest. Switch to premium models only when you need higher quality.
- Generate multiple images with `--n 4` and pick the best — it costs the same per-image but gives more options.
- Use `--negative_prompt` to exclude unwanted elements, e.g. `--negative_prompt "blurry, low quality, watermark"`.
- For video, start with 5-second duration to preview, then re-generate at longer duration once you're happy with the style.
- All results are auto-downloaded without watermarks when available.

For complete API documentation including credit pricing tables, see [references/api-docs.md](references/api-docs.md).
