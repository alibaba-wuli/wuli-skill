#!/usr/bin/env python3
"""
Wuli Platform - Unified AI Image/Video Generation Skill
Uses WULI_API_TOKEN env var for Bearer token authentication via the open platform API.
"""

import argparse
import json
import os
import platform
import subprocess
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

API_BASE = "https://platform.wuli.art/api/v1/platform"

CONTENT_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".avi": "video/x-msvideo",
    ".webm": "video/webm",
}

ACTION_DEFAULTS = {
    "image-gen": {
        "media_type": "IMAGE",
        "predict_type": "TXT_2_IMG",
        "model": "Qwen Image 2.0",
        "aspect_ratio": "1:1",
        "resolution": "2K",
        "needs_image": False,
    },
    "image-edit": {
        "media_type": "IMAGE",
        "predict_type": "REF_2_IMG",
        "model": "Qwen Image 2.0",
        "aspect_ratio": "1:1",
        "resolution": "2K",
        "needs_image": True,
    },
    "txt2video": {
        "media_type": "VIDEO",
        "predict_type": "TXT_2_VIDEO",
        "model": "通义万相 2.2 Turbo",
        "aspect_ratio": "16:9",
        "resolution": "720P",
        "needs_image": False,
    },
    "image2video": {
        "media_type": "VIDEO",
        "predict_type": "FF_2_VIDEO",
        "model": "通义万相 2.2 Turbo",
        "aspect_ratio": "16:9",
        "resolution": "720P",
        "needs_image": True,
    },
}


def api_request(method, url, token, data=None, content_type="application/json"):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    body = None
    if data is not None:
        if content_type == "application/json":
            body = json.dumps(data).encode("utf-8")
            headers["Content-Type"] = "application/json"
        else:
            body = data
            headers["Content-Type"] = content_type

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"Error: HTTP {e.code} - {err_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def upload_file(file_path, token):
    path = Path(file_path)
    if not path.is_file():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    filename = path.name
    print(f"Uploading file: {filename} ...")

    encoded_filename = urllib.parse.quote(filename)
    resp = api_request("GET", f"{API_BASE}/image/getUploadUrl?filename={encoded_filename}", token)
    if not resp.get("success"):
        print(f"Error: Failed to get upload URL: {json.dumps(resp, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    upload_url = resp["data"]["uploadUrl"]
    object_name = resp["data"]["objectName"]

    # Build public URL from upload_url (strip query params)
    parsed = urllib.parse.urlparse(upload_url)
    public_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    file_data = path.read_bytes()
    put_req = urllib.request.Request(upload_url, data=file_data, method="PUT")
    put_req.add_header("Content-Type", "application/octet-stream")
    with urllib.request.urlopen(put_req, timeout=120) as _:
        pass

    print(f"Upload complete: {public_url}")
    return public_url


def upload_url_image(image_url, token):
    """Download a remote image and re-upload it to OSS."""
    print(f"Downloading remote image: {image_url} ...")
    req = urllib.request.Request(image_url)
    with urllib.request.urlopen(req, timeout=60) as resp:
        image_data = resp.read()
        ct = resp.headers.get("Content-Type", "")

    ext = ".jpg"
    for suffix, mime in CONTENT_TYPES.items():
        if mime in ct:
            ext = suffix
            break

    url_path = urllib.parse.urlparse(image_url).path
    if "." in url_path.split("/")[-1]:
        ext = "." + url_path.split("/")[-1].rsplit(".", 1)[-1].lower()

    filename = f"upload{ext}"
    encoded_filename = urllib.parse.quote(filename)
    print(f"Re-uploading to OSS as {filename} ...")

    resp = api_request("GET", f"{API_BASE}/image/getUploadUrl?filename={encoded_filename}", token)
    if not resp.get("success"):
        print(f"Error: Failed to get upload URL: {json.dumps(resp, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    upload_url = resp["data"]["uploadUrl"]

    # Build public URL from upload_url (strip query params)
    parsed = urllib.parse.urlparse(upload_url)
    public_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    put_req = urllib.request.Request(upload_url, data=image_data, method="PUT")
    put_req.add_header("Content-Type", "application/octet-stream")
    with urllib.request.urlopen(put_req, timeout=120) as _:
        pass

    print(f"Upload complete: {public_url}")
    return public_url


def get_no_watermark_urls(task_ids, token):
    """Fetch no-watermark URLs for given task IDs."""
    urls = {}
    for task_id in task_ids:
        try:
            resp = api_request("POST", f"{API_BASE}/predict/noWatermarkImage", token,
                               data={"taskId": task_id})
            if resp.get("success") and resp.get("data", {}).get("url"):
                urls[task_id] = resp["data"]["url"]
        except Exception:
            pass
    return urls


def download_file(url, filename):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=120) as resp:
        Path(filename).write_bytes(resp.read())


def open_file(filepath):
    """Open a local file with the OS default viewer after download."""
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.Popen(["open", filepath])
        elif system == "Windows":
            os.startfile(filepath)
        elif system == "Linux":
            subprocess.Popen(["xdg-open", filepath])
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description="Wuli Platform - AI Image/Video Generation")
    parser.add_argument("--action", required=True, choices=ACTION_DEFAULTS.keys(),
                        help="Action: image-gen, image-edit, txt2video, image2video")
    parser.add_argument("--prompt", required=True, help="Generation prompt (max 2000 chars)")
    parser.add_argument("--model", default=None, help="Model name")
    parser.add_argument("--aspect_ratio", default=None, help="Aspect ratio (e.g. 1:1, 16:9)")
    parser.add_argument("--resolution", default=None, help="Resolution (e.g. 2K, 4K, 720P, 1080P)")
    parser.add_argument("--n", type=int, default=1, help="Number of images (1-4, image only)")
    parser.add_argument("--image_url", default=None, help="Reference image URL")
    parser.add_argument("--image_path", default=None, help="Local file path (auto-uploaded)")
    parser.add_argument("--duration", type=int, default=None, help="Video duration in seconds")
    parser.add_argument("--negative_prompt", default=None, help="Negative prompt")
    parser.add_argument("--optimize", action="store_true", help="Enable prompt optimization")
    args = parser.parse_args()

    token = os.environ.get("WULI_API_TOKEN")
    if not token:
        print("Error: WULI_API_TOKEN environment variable is not set\n"
              "Get your API token from https://wuli.art (左下角 -> API 开放平台)\n"
              "Then set it:\n"
              '  export WULI_API_TOKEN="wuli-your-token-here"', file=sys.stderr)
        sys.exit(1)

    cfg = ACTION_DEFAULTS[args.action]
    model = args.model or cfg["model"]
    aspect_ratio = args.aspect_ratio or cfg["aspect_ratio"]
    resolution = args.resolution or cfg["resolution"]
    media_type = cfg["media_type"]
    predict_type = cfg["predict_type"]

    if cfg["needs_image"] and not args.image_url and not args.image_path:
        print(f"Error: --image_url or --image_path is required for {args.action}", file=sys.stderr)
        sys.exit(1)

    # Handle image input: always upload to OSS (local file or remote URL)
    input_image_list = []
    if args.image_path:
        object_name = upload_file(args.image_path, token)
        input_image_list = [{"imageUrl": object_name}]
    elif args.image_url:
        object_name = upload_url_image(args.image_url, token)
        input_image_list = [{"imageUrl": object_name}]

    # Build request
    body = {
        "modelName": model,
        "mediaType": media_type,
        "predictType": predict_type,
        "prompt": args.prompt,
        "aspectRatio": aspect_ratio,
        "resolution": resolution,
        "n": args.n if media_type == "IMAGE" else 1,
        "optimizePrompt": args.optimize,
        "inputImageList": input_image_list,
        "inputVideoList": [],
    }

    duration = args.duration
    if media_type == "VIDEO":
        body["videoTotalSeconds"] = duration if duration else 5
    if args.negative_prompt:
        body["negativePrompt"] = args.negative_prompt

    print(f"\n=== Wuli Platform: {args.action} ===")
    print(f"Model:  {model}")
    print(f"Prompt: {args.prompt}")
    if media_type == "VIDEO":
        print(f"Duration: {body.get('videoTotalSeconds', 5)}s")
    print(f"Aspect: {aspect_ratio}  Resolution: {resolution}")
    print("\nSubmitting request...")

    # Submit
    resp = api_request("POST", f"{API_BASE}/predict/submit", token, data=body)
    if not resp.get("success"):
        print(f"Error: Submit failed - {json.dumps(resp, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    record_id = resp["data"]["recordId"]
    print(f"Record ID: {record_id}")
    print("Waiting for generation...")

    # Poll
    poll_interval = 10 if media_type == "VIDEO" else 5
    max_attempts = 120 if media_type == "VIDEO" else 60

    for attempt in range(1, max_attempts + 1):
        time.sleep(poll_interval)

        query_resp = api_request("GET", f"{API_BASE}/predict/query?recordId={record_id}", token)
        status = query_resp.get("data", {}).get("recordStatus", "UNKNOWN")

        if status == "SUCCEED":
            print("Generation completed!\n")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            results = query_resp["data"].get("results", [])

            # Fetch no-watermark URLs
            task_ids = [item["taskId"] for item in results if item.get("taskId")]
            print("Fetching no-watermark URLs...")
            nw_urls = get_no_watermark_urls(task_ids, token)

            if media_type == "IMAGE":
                downloaded = []
                for i, item in enumerate(results, 1):
                    task_id = item.get("taskId")
                    url = nw_urls.get(task_id) or item.get("imageUrl")
                    if url:
                        filename = f"wuli_image_{timestamp}_{i}.png"
                        src = "no-watermark" if task_id in nw_urls else "watermarked"
                        print(f"Downloading ({src}): {filename}")
                        download_file(url, filename)
                        downloaded.append(filename)
                print(f"\nDownloaded {len(downloaded)} image(s) to current directory")
                for f in downloaded:
                    open_file(f)
            else:
                task_id = results[0].get("taskId") if results else None
                url = nw_urls.get(task_id) or (results[0].get("imageUrl") if results else None)
                if url:
                    filename = f"wuli_video_{timestamp}.mp4"
                    src = "no-watermark" if task_id in nw_urls else "watermarked"
                    print(f"Downloading ({src}): {filename}")
                    download_file(url, filename)
                    print("Video downloaded to current directory")
                    open_file(filename)
            return

        if status in ("FAILED", "REVIEW_FAILED", "TIMEOUT", "CANCELLED"):
            print(f"Generation {status}")
            for item in query_resp.get("data", {}).get("results", []):
                err = item.get("errorMsg")
                if err:
                    print(f"  Task {item.get('taskId')}: {err}")
            sys.exit(1)

        elapsed = attempt * poll_interval
        print(f"Status: {status} ({elapsed}s elapsed)")

    print(f"Timeout: Generation took too long (>{max_attempts * poll_interval}s)")
    sys.exit(1)


if __name__ == "__main__":
    main()
