from __future__ import annotations

import logging
import re
from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

FOLLOWING_URL_PATTERNS = (
    "/friends",
    "/friends_mutual",
    "/following",
    "/profile.php",
    "facebook.com",
)

@dataclass
class FollowingProfile:
    id: str
    image: Optional[str]
    title: str
    subtitle_text: Optional[str]
    url: str
    username: Optional[str]
    profile_details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class FacebookFollowingScraper:
    """
    A lightweight HTML scraper that attempts to extract following entries
    from publicly accessible Facebook profile pages.

    Note:
        Facebook's markup can change over time and may require adjustments to
        the CSS selectors used here. This implementation focuses on a
        generic, best-effort extraction strategy without authentication.
    """

    def __init__(
        self,
        session: Optional[requests.Session] = None,
        logger: Optional[logging.Logger] = None,
        base_url: str = "https://www.facebook.com",
    ) -> None:
        self.session = session or self._build_session()
        self.base_url = base_url.rstrip("/")
        self.logger = logger or logging.getLogger("facebook_following_scraper")

    @staticmethod
    def _build_session() -> requests.Session:
        session = requests.Session()
        # Use a desktop-like user agent so Facebook returns standard markup
        session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.8",
            }
        )
        return session

    def scrape(self, urls: Iterable[str], max_items: Optional[int] = None) -> List[Dict[str, Any]]:
        all_profiles: List[Dict[str, Any]] = []
        remaining = max_items if max_items is not None else None

        for url in urls:
            if remaining is not None and remaining <= 0:
                break

            self.logger.info("Scraping profile: %s", url)
            try:
                profiles = self._scrape_profile(url, limit=remaining)
            except Exception as exc:  # noqa: BLE001
                self.logger.error("Failed to scrape %s: %s", url, exc, exc_info=True)
                continue

            all_profiles.extend([p.to_dict() for p in profiles])

            if remaining is not None:
                remaining -= len(profiles)

        return all_profiles

    def _scrape_profile(
        self,
        profile_url: str,
        limit: Optional[int] = None,
    ) -> List[FollowingProfile]:
        """
        Fetch a profile page and parse potential 'following' entries.

        This works in a best-effort manner since Facebook layouts can differ.
        """
        resolved_url = self._normalize_profile_url(profile_url)
        self.logger.debug("Resolved profile URL: %s", resolved_url)

        response = self.session.get(resolved_url, timeout=30)
        response.raise_for_status()

        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        cards = self._find_candidate_cards(soup)
        self.logger.debug("Found %d candidate anchor tags.", len(cards))

        profiles: List[FollowingProfile] = []
        seen_urls = set()

        for a in cards:
            href = a.get("href")
            if not href:
                continue

            full_url = self._normalize_profile_url(href)
            if full_url in seen_urls:
                continue

            seen_urls.add(full_url)
            profile = self._build_profile_from_anchor(a, full_url)
            profiles.append(profile)

            if limit is not None and len(profiles) >= limit:
                break

        return profiles

    def _normalize_profile_url(self, url: str) -> str:
        if url.startswith("http://") or url.startswith("https://"):
            return url
        if url.startswith("//"):
            return f"https:{url}"
        return urljoin(self.base_url + "/", url.lstrip("/"))

    def _find_candidate_cards(self, soup: BeautifulSoup) -> List[Any]:
        """
        Heuristic search for anchor tags that likely represent people/pages.

        Strategy:
            - Find <a> tags whose href contains known Facebook patterns.
            - Skip navigation, settings, and other non-profile links.
        """
        anchors = soup.find_all("a", href=True)
        candidates: List[Any] = []

        for a in anchors:
            href = a["href"]
            if not any(pattern in href for pattern in FOLLOWING_URL_PATTERNS):
                continue

            text = a.get_text(strip=True)
            if not text:
                continue

            # Skip navigation/utility anchors
            lower = text.lower()
            if any(
                skip in lower
                for skip in (
                    "home",
                    "create",
                    "marketplace",
                    "groups",
                    "friends",
                    "watch",
                    "menu",
                    "log in",
                    "log out",
                    "privacy",
                    "terms",
                )
            ):
                continue

            candidates.append(a)

        return candidates

    def _build_profile_from_anchor(self, a: Any, full_url: str) -> FollowingProfile:
        title = a.get_text(strip=True)
        subtitle = a.get("aria-label") or a.get("title") or None

        img_tag = a.find("img")
        image_url: Optional[str] = None
        if img_tag is not None:
            image_url = img_tag.get("src") or img_tag.get("data-src")

        parsed = urlparse(full_url)
        username = None
        profile_id = ""

        if "profile.php" in parsed.path:
            # Example: /profile.php?id=12345
            query = parsed.query
            m = re.search(r"id=(\d+)", query)
            if m:
                profile_id = m.group(1)
        else:
            # Example: /SomeUsername or /pages/category/SomePage/12345
            segments = [seg for seg in parsed.path.split("/") if seg]
            if segments:
                username = segments[-1]
                # If last segment looks numeric, treat as ID
                if re.fullmatch(r"\d+", username):
                    profile_id = username
                else:
                    profile_id = username

        if not profile_id:
            profile_id = full_url

        profile_details: Dict[str, Any] = {}
        data_gt = a.get("data-gt")
        if data_gt:
            profile_details["data_gt"] = data_gt
        data_hovercard = a.get("data-hovercard")
        if data_hovercard:
            profile_details["data_hovercard"] = data_hovercard

        if not profile_details:
            profile_details = None  # type: ignore[assignment]

        return FollowingProfile(
            id=profile_id,
            image=image_url,
            title=title,
            subtitle_text=subtitle,
            url=full_url,
            username=username,
            profile_details=profile_details,
        )