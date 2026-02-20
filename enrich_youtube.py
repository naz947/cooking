import json
import re
import base64
import httpx
from bs4 import BeautifulSoup
import subprocess

YOUTUBE_REGEX = re.compile(
    r"(https?://(?:www\.)?(?:youtube\.com/(?:watch\?v=|shorts/)|youtu\.be/)([\w\-]+))"
)

YOUTUBE_REGEX = re.compile(
    r"(https?://(?:www\.)?(?:youtube\.com/(?:watch\?v=|shorts/)|youtu\.be/)([\w\-]+))"
)

HASHTAG_REGEX = re.compile(r"#\w+")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def extract_video_id(url):
    match = YOUTUBE_REGEX.search(url)
    if match:
        return match.group(2)
    return None

def get_youtube_metadata(url, video_id):
    try:
        # Try using yt-dlp for reliable metadata extraction
        result = subprocess.run(
            [
                "yt-dlp",
                "-j",
                "--no-warnings",
                url
            ],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            info = json.loads(result.stdout)
            title = info.get("title")
            description = info.get("description")
            return title, description
    except Exception as e:
        print(f"yt-dlp not available, falling back to HTML parsing: {e}")

    # Fallback: Parse HTML metadata
    try:
        with httpx.Client(timeout=10, follow_redirects=True, headers=HEADERS) as client:
            r = client.get(url)
            soup = BeautifulSoup(r.text, "html.parser")

            # Try to find title
            title = None
            title_tag = soup.find("h1")
            if title_tag:
                title = title_tag.text.strip()
            else:
                title_tag = soup.find("title")
                if title_tag:
                    title = title_tag.text.replace(" - YouTube", "").strip()

            # Try to find description
            description = None
            desc_tag = soup.find("meta", attrs={"name": "description"})
            if desc_tag and desc_tag.get("content"):
                description = desc_tag["content"].strip()
            else:
                # Try another meta tag
                desc_tag = soup.find("meta", attrs={"property": "og:description"})
                if desc_tag and desc_tag.get("content"):
                    description = desc_tag["content"].strip()

            return title, description
    except Exception as e:
        print(f"Error fetching metadata {url}: {e}")

    return None, None

def get_thumbnail_base64(video_id):
    thumb_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

    try:
        with httpx.Client(timeout=10) as client:
            r = client.get(thumb_url)
            if r.status_code == 200:
                return base64.b64encode(r.content).decode("utf-8")
    except Exception as e:
        print(f"Error fetching thumbnail {video_id}: {e}")

    return None

def main():
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        text = item.get("text", "")

        # extract hashtags
        item["hashtags"] = HASHTAG_REGEX.findall(text)

        item["youtube_title"] = None
        item["youtube_description"] = None
        item["youtube_thumbnail_base64"] = None

        for url in item.get("urls", []):
            video_id = extract_video_id(url)
            if video_id:
                title, description = get_youtube_metadata(url, video_id)
                thumbnail_b64 = get_thumbnail_base64(video_id)

                item["youtube_title"] = title
                item["youtube_description"] = description
                item["youtube_thumbnail_base64"] = thumbnail_b64
                break

    with open("data_enriched.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Saved to data_enriched.json")

if __name__ == "__main__":
    main()