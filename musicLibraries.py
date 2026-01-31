from typing import Dict

musicLinks: Dict[str, str] = {
    "animal": "https://www.youtube.com/watch?v=CPsUhaf1RQ0",
    "starboy": "https://www.youtube.com/watch?v=34Na4j8AVgA",
    "impala": "https://www.youtube.com/watch?v=2SUwOgmvzK4",
    "borderline": "https://www.youtube.com/channel/UCdI8MAC5HoPJSJ4zrgDDI-Q",
}


def normalized_music_links() -> Dict[str, str]:
    return {" ".join(k.strip().lower().split()): v for k, v in musicLinks.items()}