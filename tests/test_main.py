from unittest.mock import Mock
import requests
import main

def make_response(data):
    response = Mock()
    response.json.return_value = data
    response.raise_for_status.return_value = None
    return response


def test_display_email_prints_message(monkeypatch, capsys):
    fake_email_data = {
        "from_name": "John Lewis",
        "from_addr": "JL@testing.com",
        "subject": "hacked!!",
        "received_at": 1_750_000_000_000,
        "text": "you've been hacked.",
        "html": None,
    }

    monkeypatch.setattr(
        main.requests,
        "get",
        lambda *args, **kwargs: make_response(fake_email_data),
    )

    main.display_email("message-123", {"Authorization": "Bearer test"})
    output = capsys.readouterr().out

    assert "John Lewis" in output
    assert "JL@testing.com" in output
    assert "hacked!!" in output
    assert "you've been hacked." in output


def test_display_email_handles_http_error(monkeypatch, capsys):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.Timeout("Request timed out")

    monkeypatch.setattr(main.requests, "get", mock_get)

    main.display_email("message-123", {})

    output = capsys.readouterr().out
    assert "There was an error" in output