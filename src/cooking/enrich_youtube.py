import json
import re
import base64
import httpx
from bs4 import BeautifulSoup

YOUTUBE_REGEX = re.compile(
    r"(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w\-]+))"
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

def get_youtube_metadata(url):
    try:
        with httpx.Client(timeout=10, follow_redirects=True, headers=HEADERS) as client:
            r = client.get(url)
            soup = BeautifulSoup(r.text, "html.parser")

            # title
            title_tag = soup.find("title")
            title = title_tag.text.replace(" - YouTube", "").strip() if title_tag else None

            # description
            desc_tag = soup.find("meta", attrs={"name": "description"})
            description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else None

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
                title, description = get_youtube_metadata(url)
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