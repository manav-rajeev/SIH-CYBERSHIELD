from pathlib import Path

from services.detection_history_service import (
    clear_detection_history,
    get_detection_history,
    record_detection,
)


def sample_result() -> dict:
    return {
        "url": "https://example.com",
        "score": 8,
        "classification": "SAFE",
        "reasons": [
            "No significant phishing indicators detected"
        ],
        "url_features": {
            "uses_https": True,
            "has_ip_address": False,
        },
        "website_features": {
            "form_count": 0,
            "password_field_count": 0,
        },
    }


def test_record_and_read_detection(tmp_path: Path):
    db_path = tmp_path / "history.db"

    saved = record_detection(
        sample_result(),
        db_path=db_path,
    )

    assert saved["id"] == 1
    assert saved["url"] == "https://example.com"
    assert saved["score"] == 8
    assert saved["classification"] == "SAFE"

    history = get_detection_history(
        db_path=db_path,
    )

    assert len(history) == 1
    assert history[0]["url"] == "https://example.com"
    assert history[0]["reasons"] == [
        "No significant phishing indicators detected"
    ]
    assert history[0]["url_features"]["uses_https"] is True
    assert (
        history[0]["website_features"]["form_count"] == 0
    )


def test_history_returns_newest_first(tmp_path: Path):
    db_path = tmp_path / "history.db"

    first = sample_result()

    second = {
        **sample_result(),
        "url": "http://suspicious.example/login",
        "score": 61,
        "classification": "HIGH RISK",
    }

    record_detection(first, db_path=db_path)
    record_detection(second, db_path=db_path)

    history = get_detection_history(
        db_path=db_path,
    )

    assert history[0]["url"] == (
        "http://suspicious.example/login"
    )
    assert history[1]["url"] == "https://example.com"


def test_history_limit(tmp_path: Path):
    db_path = tmp_path / "history.db"

    for index in range(5):
        result = {
            **sample_result(),
            "url": f"https://example{index}.com",
        }

        record_detection(
            result,
            db_path=db_path,
        )

    history = get_detection_history(
        limit=2,
        db_path=db_path,
    )

    assert len(history) == 2


def test_clear_history(tmp_path: Path):
    db_path = tmp_path / "history.db"

    record_detection(
        sample_result(),
        db_path=db_path,
    )

    clear_detection_history(
        db_path=db_path,
    )

    assert get_detection_history(
        db_path=db_path,
    ) == []