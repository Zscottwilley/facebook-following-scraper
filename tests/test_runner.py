thonfrom pathlib import Path
from textwrap import dedent
from typing import Any, Dict, Optional

import json
import types

from src import runner as runner_module

SAMPLE_HTML = dedent(
    """
    <html>
      <body>
        <div data-testid="follow_list_item" class="following-item" data-profile-id="100064487118317">
          <a href="https://www.facebook.com/UncutMagazine">
            <img src="https://scontent-ams4-1.xx.fbcdn.net/photo1.jpg" />
            <span class="following-title">Uncut Magazine</span>
          </a>
          <div class="following-subtitle"></div>
        </div>
        <div data-testid="follow_list_item" class="following-item" data-profile-id="100012345678900">
          <a href="https://www.facebook.com/example.profile">
            <img src="https://example.com/photo.jpg" />
            <span class="following-title">Example Profile</span>
          </a>
          <div class="following-subtitle">Music · Artist</div>
        </div>
      </body>
    </html>
    """
)

def fake_fetch_following_page(
    profile_url: str, settings: Optional[Dict[str, Any]] = None
) -> str:
    # Ignore the URL and settings; always return the sample HTML.
    return SAMPLE_HTML

def test_runner_creates_output_files(tmp_path, monkeypatch):
    # Patch fetch_following_page so runner does not hit the real network.
    from src.extractors import facebook_parser

    monkeypatch.setattr(
        facebook_parser,
        "fetch_following_page",
        fake_fetch_following_page,
        raising=True,
    )
    # Ensure runner uses the patched function too.
    monkeypatch.setattr(
        runner_module,
        "fetch_following_page",
        fake_fetch_following_page,
        raising=True,
    )

    # Create a temporary inputs JSON file.
    input_cfg = [
        {
            "url": "https://www.facebook.com/UncutMagazine/following",
            "maxItems": 2,
            "exportFormats": ["json", "csv"],
        }
    ]
    input_path = tmp_path / "inputs.json"
    input_path.write_text(json.dumps(input_cfg), encoding="utf-8")

    output_dir = tmp_path / "output"

    argv = [
        "--input",
        str(input_path),
        "--output-dir",
        str(output_dir),
        "--log-level",
        "ERROR",
    ]
    runner_module.main(argv)

    # Expect at least JSON and CSV files for the single profile.
    # Base filename is "00_profile" because slug_from_url will derive from path "/UncutMagazine/following".
    json_files = list(output_dir.glob("*.json"))
    csv_files = list(output_dir.glob("*.csv"))

    assert json_files, "Expected at least one JSON export file"
    assert csv_files, "Expected at least one CSV export file"

    # Validate that JSON output contains parsed records.
    content = json.loads(json_files[0].read_text(encoding="utf-8"))
    assert isinstance(content, list)
    assert len(content) == 2
    assert content[0]["title"] == "Uncut Magazine"