thonfrom textwrap import dedent

from src.extractors.facebook_parser import parse_following_html

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

def test_parse_following_html_parses_two_items():
    profiles = parse_following_html(SAMPLE_HTML)
    assert len(profiles) == 2

    first = profiles[0]
    assert first.id == "100064487118317"
    assert first.title == "Uncut Magazine"
    assert first.url == "https://www.facebook.com/UncutMagazine"
    assert first.image.startswith("https://scontent-ams4-1.xx.fbcdn.net")

    second = profiles[1]
    assert second.id == "100012345678900"
    assert second.title == "Example Profile"
    assert second.subtitle_text == "Music · Artist"
    assert second.url == "https://www.facebook.com/example.profile"

def test_parse_following_html_respects_max_items():
    profiles = parse_following_html(SAMPLE_HTML, max_items=1)
    assert len(profiles) == 1
    assert profiles[0].title == "Uncut Magazine"