thonfrom typing import Any, Dict, Iterable, List

from .facebook_parser import FollowingProfile

def following_to_dicts(entries: Iterable[FollowingProfile]) -> List[Dict[str, Any]]:
    """
    Convert an iterable of FollowingProfile instances into a list of plain dicts
    ready for serialization to JSON/CSV/etc.
    """
    result: List[Dict[str, Any]] = []
    for entry in entries:
        if isinstance(entry, FollowingProfile):
            result.append(entry.to_dict())
        elif isinstance(entry, dict):
            # Already a dict; make a shallow copy to avoid accidental mutations.
            result.append(dict(entry))
        else:
            # Fallback: best-effort mapping via vars()
            result.append(dict(vars(entry)))
    return result