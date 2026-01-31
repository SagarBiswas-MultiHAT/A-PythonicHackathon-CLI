from sagar_assistant import AssistantConfig, handle_command


def _dummy_ai_process(command, context):
    return f"echo:{command}"


def _dummy_opener(url):
    return True


def test_help_command_returns_help_text():
    config = AssistantConfig(url_map={}, music_links={}, model_fallbacks=[], max_context_messages=5)
    _, response = handle_command(
        "help",
        None,
        config=config,
        ai_process=_dummy_ai_process,
    )
    assert "Commands:" in response


def test_list_songs():
    config = AssistantConfig(
        url_map={},
        music_links={"song a": "http://example.com"},
        model_fallbacks=[],
        max_context_messages=5,
    )
    _, response = handle_command(
        "list songs",
        None,
        config=config,
        ai_process=_dummy_ai_process,
    )
    assert "song a" in response


def test_play_song_opens_url():
    config = AssistantConfig(
        url_map={},
        music_links={"song a": "http://example.com"},
        model_fallbacks=[],
        max_context_messages=5,
    )
    _, response = handle_command(
        "play song a",
        None,
        config=config,
        opener=_dummy_opener,
        ai_process=_dummy_ai_process,
    )
    assert "Playing" in response


def test_unknown_command_uses_ai_process_and_updates_context():
    config = AssistantConfig(url_map={}, music_links={}, model_fallbacks=[], max_context_messages=5)
    context, response = handle_command(
        "what is crypto",
        None,
        config=config,
        ai_process=_dummy_ai_process,
    )
    assert response.startswith("AI Response:")
    assert context is not None
    assert len(context) == 2
