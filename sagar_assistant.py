from __future__ import annotations

import os
import webbrowser
from dataclasses import dataclass
from typing import Callable, Optional, Tuple

from dotenv import load_dotenv
from groq import Groq

import musicLibraries


@dataclass(frozen=True)
class AssistantConfig:
    url_map: dict[str, str]
    music_links: dict[str, str]
    model_fallbacks: list[str]
    max_context_messages: int


def _get_model_fallbacks() -> list[str]:
    preferred = os.getenv("GROQ_MODEL")
    return [m for m in [preferred, "llama-3.3-70b-versatile", "llama-3.1-8b-instant"] if m]


def default_config() -> AssistantConfig:
    return AssistantConfig(
        url_map={
            "open google": "https://google.com",
            "open youtube": "https://youtube.com",
            "open facebook": "https://facebook.com",
            "open instagram": "https://instagram.com",
            "open github": "https://github.com",
            "open stackoverflow": "https://stackoverflow.com",
            "open linkedin": "https://linkedin.com",
            "open whatsapp": "https://whatsapp.com",
            "open chatgpt": "https://chat.openai.com/chat",
            "open gemini": "https://gemini.google.com/",
            "open chatbot": "https://cdn.botpress.cloud/webchat/v2/shareable.html?botId=2b113ef8-ac77-4553-b353-7e381fcffdde",
        },
        music_links=musicLibraries.normalized_music_links(),
        model_fallbacks=_get_model_fallbacks(),
        max_context_messages=10,
    )


def _normalize_song_key(text: str) -> str:
    return " ".join(text.strip().lower().split())


def _ai_process(command: str, context: Optional[list[dict]]) -> str:
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Create a .env file with GROQ_API_KEY=your_key or set it in the environment."
        )

    client = Groq(api_key=api_key)

    messages = [
        {
            "role": "system",
            "content": (
                "You are Sagar, a helpful, professional virtual assistant for CSE and "
                "cybersecurity learners. Keep answers concise, accurate, and easy to "
                "understand. Follow safety best practices: refuse harmful requests and "
                "offer safe alternatives or high-level educational guidance instead."
            ),
        },
    ]

    if context is not None:
        messages.append({"role": "system", "content": str(context)})

    messages.append({"role": "user", "content": command})

    last_err = None
    for model_name in _get_model_fallbacks():
        try:
            completion = client.chat.completions.create(model=model_name, messages=messages)
            return completion.choices[0].message.content
        except Exception as exc:
            last_err = exc
            continue

    raise RuntimeError(
        f"All model attempts failed (tried: {', '.join(_get_model_fallbacks())}). Last error: {last_err}"
    )


def _trim_context(context: list[dict], max_messages: int) -> list[dict]:
    if max_messages <= 0:
        return []
    keep = max_messages * 2
    return context[-keep:]


def help_text() -> str:
    return (
        "Commands:\n"
        "  open <site>      (google, youtube, facebook, instagram, github, stackoverflow, linkedin, whatsapp, chatgpt, gemini, chatbot)\n"
        "  play <song>      (try: list songs)\n"
        "  list songs       (show available songs)\n"
        "  help             (show this help)\n"
        "  exit             (quit the app)"
    )


def handle_command(
    command: str,
    context: Optional[list[dict]],
    config: Optional[AssistantConfig] = None,
    opener: Callable[[str], bool] = webbrowser.open,
    ai_process: Callable[[str, Optional[list[dict]]], str] = _ai_process,
) -> Tuple[Optional[list[dict]], str]:
    if config is None:
        config = default_config()

    command = command.strip()
    if not command:
        return context, "..:: Empty command. Type 'help' to see options."

    command_lower = command.lower()

    if command_lower in {"help", "?"}:
        return context, help_text()

    if command_lower in {"list songs", "songs"}:
        songs = sorted(config.music_links.keys())
        if not songs:
            return context, "..:: No songs configured."
        return context, "Available songs: " + ", ".join(songs)

    if command_lower in config.url_map:
        opener(config.url_map[command_lower])
        return context, f"..:: Opened: {command_lower}"

    if command_lower.startswith("play"):
        song = command[4:].strip()
        if not song:
            return context, "..:: Invalid command. No song specified."

        song_key = _normalize_song_key(song)
        link = config.music_links.get(song_key)
        if link:
            opener(link)
            return context, f"..:: Playing: {song}"
        return context, "..:: Song is not found in the music library."

    output = ai_process(command, context)

    if context is None or not isinstance(context, list):
        context = []

    context.append({"role": "user", "content": command})
    context.append({"role": "assistant", "content": output})

    context = _trim_context(context, config.max_context_messages)

    return context, f"AI Response: {output}"
