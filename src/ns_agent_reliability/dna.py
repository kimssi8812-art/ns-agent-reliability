from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any


DETERMINISTIC_ONLY_INTENTS = frozenset({"CHAT_SHARE", "DNA_HYDRATION"})
_SHARE_RE = re.compile(r"^https://chatgpt\.com/share/([A-Za-z0-9-]{16,})(?:\?.*)?$")


class DNAError(RuntimeError):
    pass


@dataclass(frozen=True)
class ChatShareIntake:
    slug: str
    url: str
    idempotency_key: str


def provider_required_for_intent(intent: str) -> bool:
    return (intent or "").upper() not in DETERMINISTIC_ONLY_INTENTS


def parse_share_url(url: str) -> ChatShareIntake:
    match = _SHARE_RE.fullmatch(url.strip())
    if not match:
        raise DNAError("INVALID_CHAT_SHARE_URL")
    slug = match.group(1)
    canonical = f"https://chatgpt.com/share/{slug}"
    return ChatShareIntake(slug=slug, url=canonical, idempotency_key=f"chat-export:{slug}")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _clip(value: Any, limit: int) -> str:
    text = str(value or "").strip().replace("\x00", "")
    return text if len(text) <= limit else text[: max(0, limit - 1)].rstrip() + "…"


def _json_size(value: Any) -> int:
    return len(json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def build_inheritance_packet(
    dna: dict[str, Any],
    *,
    slug: str,
    source_digest: str,
    max_bytes: int = 4096,
) -> dict[str, Any]:
    if max_bytes < 1024:
        raise DNAError("PACKET_BUDGET_TOO_SMALL")
    if len(source_digest) != 64:
        raise DNAError("SOURCE_DIGEST_UNVERIFIED")

    last_context = dna.get("last_context") if isinstance(dna.get("last_context"), dict) else {}
    packet: dict[str, Any] = {
        "schema_version": "1.0",
        "authority": "NON_SSOT",
        "mode": "DETERMINISTIC_ZERO_UNNECESSARY_AI",
        "slug": slug,
        "source_digest": source_digest,
        "completeness": dna.get("completeness"),
        "conversation_type": dna.get("conversation_type"),
        "title": _clip(dna.get("title"), 160),
        "current_state": _clip(dna.get("current_state"), 80),
        "core_purpose": _clip(dna.get("core_purpose"), 320),
        "summary": _clip(dna.get("summary"), 600),
        "last_context": {
            "user_intent": _clip(last_context.get("user_intent"), 360),
            "unfinished_point": _clip(last_context.get("unfinished_point"), 480),
        },
        "provider_calls_required": 0,
        "full_history_default_read": False,
    }

    for key in ("open_tasks", "next_actions", "decisions", "constraints"):
        items = dna.get(key)
        if not isinstance(items, list):
            continue
        bucket: list[dict[str, str]] = []
        packet[key] = bucket
        for item in reversed(items):
            if not isinstance(item, dict) or not item.get("text"):
                continue
            bucket.append({
                "message_ref": _clip(item.get("message_ref"), 40),
                "text": _clip(item.get("text"), 240),
            })
            if _json_size(packet) > max_bytes:
                bucket.pop()
                break
        if not bucket:
            packet.pop(key, None)

    if _json_size(packet) > max_bytes:
        packet["summary"] = _clip(packet.get("summary"), 240)
        packet["core_purpose"] = _clip(packet.get("core_purpose"), 180)
        packet["last_context"]["user_intent"] = _clip(packet["last_context"].get("user_intent"), 180)
        packet["last_context"]["unfinished_point"] = _clip(packet["last_context"].get("unfinished_point"), 220)

    if _json_size(packet) > max_bytes:
        raise DNAError("INHERITANCE_PACKET_BUDGET_EXCEEDED")

    packet["packet_bytes"] = 0
    while True:
        size = _json_size(packet)
        if packet["packet_bytes"] == size:
            break
        packet["packet_bytes"] = size
    if packet["packet_bytes"] > max_bytes:
        raise DNAError("INHERITANCE_PACKET_BUDGET_EXCEEDED")
    return packet
