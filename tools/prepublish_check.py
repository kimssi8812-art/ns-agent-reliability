#!/usr/bin/env python3
from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "FILE_INDEX.json"

FAIL_PATTERNS = {
    "github_token": re.compile(r"\b(?:gho|ghp|github_pat)_[A-Za-z0-9_]+\b"),
    "aws_access_key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "bearer_token": re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]+", re.IGNORECASE),
    "authorization_value": re.compile(r"Authorization\s*[:=]\s*[A-Za-z0-9._~+/=-]+", re.IGNORECASE),
    "private_key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "private_home_path": re.compile(r"/home/[A-Za-z0-9._-]+/"),
    "credential_url": re.compile(r"https?://[^\s/@:]+:[^\s/@]+@", re.IGNORECASE),
    "private_ipv4": re.compile(r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b"),
}
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
CHATGPT_SHARE_RE = re.compile(r"https://chatgpt\.com/share/([A-Za-z0-9-]{20,})")
NULL_SHARE_SLUG = "00000000-0000-0000-0000-000000000000"
FORBIDDEN_NAME_RE = re.compile(r"(^|/)(?:\.env(?:\..*)?|id_rsa|id_ed25519|credentials(?:\..*)?|cookies?(?:\..*)?|[^/]+\.(?:pem|p12|pfx|key))$", re.IGNORECASE)
FORBIDDEN_PATH_PARTS = {"build", "dist", "__pycache__", ".pytest_cache", "state", "logs", ".git"}
REQUIRED_RELEASE_FILES = {
    "README.md", "LICENSE", "LICENSES/CC-BY-4.0.txt", "LICENSE_POLICY.md", "NOTICE",
    "TRADEMARKS.md", "THIRD_PARTY_NOTICES.md", "SBOM.spdx.json", "pyproject.toml",
    "src/ns_agent_reliability/doctor.py", "examples/doctor_broken_system.json", "tests/test_doctor.py",
    "release/TECHNICAL_PREPUBLICATION_RECEIPT_20260908.json",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_rel(rel: str) -> bool:
    p = PurePosixPath(rel)
    return bool(rel) and not p.is_absolute() and ".." not in p.parts


def main() -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    tracked = data["tracked_files"]
    failures: list[str] = []
    manifest: list[dict[str, object]] = []

    if len(tracked) != len(set(tracked)):
        failures.append("DUPLICATE_TRACKED_PATH")
    missing_required = sorted(REQUIRED_RELEASE_FILES - set(tracked))
    failures.extend(f"REQUIRED_NOT_TRACKED:{x}" for x in missing_required)

    for rel in tracked:
        if not safe_rel(rel):
            failures.append(f"UNSAFE_TRACKED_PATH:{rel}")
            continue
        if FORBIDDEN_NAME_RE.search(rel):
            failures.append(f"SENSITIVE_FILENAME:{rel}")
        if any(part in FORBIDDEN_PATH_PARTS for part in PurePosixPath(rel).parts):
            failures.append(f"FORBIDDEN_BUILD_RUNTIME_PATH:{rel}")
        path = ROOT / rel
        if path.is_symlink():
            failures.append(f"SYMLINK_TRACKED:{rel}")
            continue
        if not path.is_file():
            failures.append(f"MISSING:{rel}")
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(raw.splitlines(), 1):
            for name, pattern in FAIL_PATTERNS.items():
                if pattern.search(line):
                    failures.append(f"SENSITIVE:{name}:{rel}:{line_no}")
            for m in EMAIL_RE.finditer(line):
                if not m.group(0).lower().endswith("@example.invalid"):
                    failures.append(f"EMAIL:{rel}:{line_no}")
            for m in CHATGPT_SHARE_RE.finditer(line):
                slug = m.group(1)
                if slug != NULL_SHARE_SLUG:
                    failures.append(f"REAL_OR_UNVERIFIED_CHATGPT_SHARE:{rel}:{line_no}")
        if path.suffix == ".json":
            try:
                json.loads(raw)
            except Exception as exc:
                failures.append(f"INVALID_JSON:{rel}:{type(exc).__name__}")
        manifest.append({"path": rel, "sha256": sha256(path), "bytes": path.stat().st_size})

    # Package release metadata must reflect the selected software license and non-placeholder version.
    try:
        meta = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
        license_value = meta.get("license")
        if isinstance(license_value, dict):
            license_value = license_value.get("text")
        if license_value != "Apache-2.0":
            failures.append(f"PYPROJECT_LICENSE_NOT_APACHE_2_0:{license_value!r}")
        if str(meta.get("version") or "") in {"", "0.0.0"}:
            failures.append("PYPROJECT_VERSION_PLACEHOLDER")
        declared_deps = list(meta.get("dependencies") or [])
    except Exception as exc:
        failures.append(f"PYPROJECT_PARSE_FAIL:{type(exc).__name__}")
        declared_deps = []

    # If there are no declared runtime dependencies, public source must not import undeclared third-party modules.
    if not declared_deps:
        external: set[str] = set()
        stdlib = set(getattr(sys, "stdlib_module_names", ()))
        for path in (ROOT / "src" / "ns_agent_reliability").glob("*.py"):
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"))
            except Exception as exc:
                failures.append(f"PYTHON_PARSE_FAIL:{path.relative_to(ROOT)}:{type(exc).__name__}")
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    external.update(x.name.split(".")[0] for x in node.names)
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    external.add(node.module.split(".")[0])
        external = {x for x in external if x not in stdlib and x != "ns_agent_reliability"}
        if external:
            failures.append("UNDECLARED_RUNTIME_IMPORTS:" + ",".join(sorted(external)))

    # The candidate root itself must be clean of generated package/test residue before staging.
    for name in ("build", "dist", ".pytest_cache"):
        if (ROOT / name).exists():
            failures.append(f"GENERATED_RESIDUE:{name}")
    for residue in (ROOT / "src").glob("*.egg-info"):
        failures.append(f"GENERATED_RESIDUE:{residue.relative_to(ROOT)}")

    out = ROOT / "PUBLIC_TREE_MANIFEST.generated.json"
    out.write_text(json.dumps({
        "schema_version": "NS_GPT_PUBLIC_TREE_MANIFEST_V2",
        "file_count": len(manifest),
        "files": manifest,
        "checks": {
            "tracked_unique": len(tracked) == len(set(tracked)),
            "required_release_files": not missing_required,
            "path_and_symlink_policy": not any(x.startswith(("UNSAFE_TRACKED_PATH", "SYMLINK_TRACKED", "FORBIDDEN_BUILD_RUNTIME_PATH")) for x in failures),
            "secret_private_pattern_scan": not any(x.startswith(("SENSITIVE:", "EMAIL:", "REAL_OR_UNVERIFIED_CHATGPT_SHARE:", "SENSITIVE_FILENAME:")) for x in failures),
            "json_parse": not any(x.startswith("INVALID_JSON:") for x in failures),
            "package_metadata": not any(x.startswith(("PYPROJECT_", "UNDECLARED_RUNTIME_IMPORTS:")) for x in failures),
        },
        "scan": "PASS" if not failures else "FAIL",
        "failures": failures,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"TRACKED_FILES={len(tracked)}")
    print(f"MANIFEST_FILES={len(manifest)}")
    print(f"PUBLIC_SCAN={'PASS' if not failures else 'FAIL'}")
    for failure in failures:
        print(failure)
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
