#!/usr/bin/env python3
"""Verify the entire Marimay learning corpus without collecting timings."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import platform
import re
import shutil
import subprocess
import tempfile


def test_names(source: Path) -> set[str]:
    names = set()
    for path in source.rglob("*_test.my"):
        if ".mmay" in path.parts:
            continue
        package = "course.local/algorithms"
        relative = path.parent.relative_to(source).as_posix()
        if relative != ".":
            package += "/" + relative
        pattern = r"(?m)^@test\s+fn\s+(\w+)\s*\("
        for name in re.findall(pattern, path.read_text(encoding="utf-8")):
            qualified = package + "." + name
            if qualified in names:
                raise ValueError("duplicate test: " + qualified)
            names.add(qualified)
    if not names:
        raise ValueError("no Marimay tests discovered")
    return names


def validate_tests(output: str, expected: set[str]) -> int:
    actual = re.findall(r"(?m)^test (\S+) \.\.\. ok$", output)
    summary = re.findall(r"(?m)^test result: ok\. (\d+) passed; 0 failed$", output)
    if (
        len(summary) != 1
        or int(summary[0]) != len(actual)
        or len(actual) != len(set(actual))
    ):
        raise ValueError("missing or inconsistent passing-test summary")
    if set(actual) != expected:
        raise ValueError(
            "test discovery mismatch; missing=" + str(sorted(expected - set(actual)))
            + "; unexpected=" + str(sorted(set(actual) - expected))
        )
    return len(actual)


def validate_lessons(source: Path, manifest: object) -> list[dict[str, str]]:
    """Require a safe, complete one-to-one inventory of runnable examples."""
    if not isinstance(manifest, list) or not manifest:
        raise ValueError("lesson manifest must be a nonempty list")
    root = source.resolve()
    declared = set()
    lessons = []
    for lesson in manifest:
        if not isinstance(lesson, dict) or set(lesson) != {"path", "stdout"}:
            raise ValueError("each lesson must contain only path and stdout")
        raw = lesson["path"]
        if not isinstance(raw, str) or not raw:
            raise ValueError("lesson path must be a nonempty string")
        path = PurePosixPath(raw)
        if (
            path.is_absolute()
            or PureWindowsPath(raw).drive
            or "\\" in raw
            or "\0" in raw
            or any(part in ("", ".", "..") for part in raw.split("/"))
            or path.as_posix() != raw
            or path.parts[0] != "examples"
        ):
            raise ValueError("unsafe lesson path: " + raw)
        try:
            (root / raw).resolve().relative_to(root)
            (root / raw / "main.my").resolve().relative_to(root)
        except ValueError as error:
            raise ValueError("lesson path escapes the repository: " + raw) from error
        if raw in declared:
            raise ValueError("duplicate lesson path: " + raw)
        if not isinstance(lesson["stdout"], str):
            raise ValueError("lesson stdout must be a string: " + raw)
        declared.add(raw)
        lessons.append({"path": raw, "stdout": lesson["stdout"]})
    discovered = set()
    for main in (root / "examples").rglob("main.my"):
        if ".mmay" in main.relative_to(root).parts or not main.is_file():
            continue
        try:
            main.resolve().relative_to(root)
        except ValueError as error:
            raise ValueError("discovered example escapes the repository") from error
        discovered.add(main.parent.relative_to(root).as_posix())
    if declared != discovered:
        raise ValueError(
            "lesson discovery mismatch; missing=" + str(sorted(discovered - declared))
            + "; unexpected=" + str(sorted(declared - discovered))
        )
    return lessons


def validate_version(version: object) -> dict:
    if not isinstance(version, dict):
        raise ValueError("compiler version must be a JSON object")
    expected = {
        "schema": "marimay.version/2",
        "compiler": "0.1.0-alpha.1",
        "runtime": "0.1.0-alpha.1",
        "language": "0.1-design",
    }
    for field, value in expected.items():
        if version.get(field) != value:
            raise ValueError("unsupported Marimay version field: " + field)
    standard = version.get("standardLibrary")
    if not isinstance(standard, dict) or standard.get("version") != expected["compiler"]:
        raise ValueError("unsupported Marimay standard library version")
    commands = version.get("commands")
    available = commands.get("available") if isinstance(commands, dict) else None
    if (
        not isinstance(available, list)
        or not all(isinstance(name, str) for name in available)
        or len(available) != len(set(available))
    ):
        raise ValueError("invalid implemented-command inventory")
    required = {"version", "fmt", "check", "test", "run", "build"}
    missing = required - set(available)
    if missing:
        raise ValueError("required compiler commands unavailable: " + str(sorted(missing)))
    return version


def execute(argv: list[str], cwd: Path) -> str:
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, timeout=600,
    )
    if result.returncode:
        raise RuntimeError(
            "command failed: " + " ".join(argv) + "\n" + result.stdout + result.stderr
        )
    if result.stderr:
        print(result.stderr, end="")
    return result.stdout


def git_revision(path: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        )
    except OSError:
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def working_tree_dirty(path: Path) -> bool | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(path), "status", "--porcelain", "--untracked-files=normal"],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        )
    except OSError:
        return None
    return bool(result.stdout) if result.returncode == 0 else None


def compiler_source_root(compiler: Path) -> Path | None:
    candidate = None
    if compiler.parent.parent.name == "build":
        candidate = compiler.parent.parent.parent
    elif (
        compiler.parent.name in {"Debug", "Release", "RelWithDebInfo", "MinSizeRel"}
        and compiler.parent.parent.parent.name == "build"
    ):
        candidate = compiler.parent.parent.parent.parent
    if (
        candidate is not None
        and (candidate / "CMakeLists.txt").is_file()
        and (candidate / "bootstrap/include/mmay").is_dir()
        and (candidate / "runtime").is_dir()
    ):
        return candidate
    return None


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_digest(source: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(source.rglob("*.my")):
        if ".mmay" in path.parts:
            continue
        digest.update(path.relative_to(source).as_posix().encode("utf-8") + b"\0")
        digest.update(path.read_bytes() + b"\0")
    for name in ("mmay.mod", "lessons.json"):
        digest.update(name.encode("utf-8") + b"\0")
        digest.update((source / name).read_bytes() + b"\0")
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mmay", type=Path, help="current compiler (or set MMAY)")
    parser.add_argument("--output", type=Path, help="write a local correctness report")
    args = parser.parse_args()
    repository = Path(__file__).resolve().parents[1]
    selected = args.mmay or os.environ.get("MMAY") or shutil.which("mmay")
    if not selected:
        parser.error("set MMAY or pass --mmay /absolute/path/to/mmay")
    compiler = Path(selected).resolve()
    compiler_before = file_sha256(compiler)
    source = repository
    before = source_digest(source)
    lessons = validate_lessons(
        source, json.loads((repository / "lessons.json").read_text(encoding="utf-8"))
    )
    version = validate_version(
        json.loads(execute([str(compiler), "version", "--json"], repository))
    )
    expected = test_names(source)
    commands = [
        [str(compiler), "fmt", str(source), "--check"],
        [str(compiler), "check", str(source), "--all-targets"],
        [str(compiler), "test", str(source), "--engine", "both"],
    ]
    for command in commands:
        output = execute(command, repository)
        print(output, end="")
    count = validate_tests(output, expected)
    with tempfile.TemporaryDirectory(prefix="marimay-algorithms-") as temporary:
        for index, lesson in enumerate(lessons):
            demo = repository / lesson["path"]
            vm = execute([str(compiler), "run", str(demo)], repository)
            if vm != lesson["stdout"]:
                raise ValueError("unexpected example output: " + lesson["path"])
            for mode in ("debug", "release"):
                binary = Path(temporary) / (str(index) + "-" + demo.name + "-" + mode)
                command = [str(compiler), "build", str(demo), "--output", str(binary)]
                if mode == "release":
                    command.append("--release")
                execute(command, repository)
                native = execute([str(binary)], repository)
                if native != vm:
                    raise ValueError("VM/native " + mode + " mismatch: " + lesson["path"])
            print(lesson["path"] + ": VM/native debug/release passed")
    if source_digest(source) != before:
        raise ValueError("algorithm sources or lesson manifest changed during verification")
    if file_sha256(compiler) != compiler_before:
        raise ValueError("compiler changed during verification; use a stable binary")
    compiler_root = compiler_source_root(compiler)
    report = {
        "schema": "marimay.course-correctness/1",
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Local correctness; no performance or platform acceptance claim",
        "repository_revision": git_revision(repository),
        "working_tree_dirty": working_tree_dirty(repository),
        "source_sha256": before,
        "compiler_sha256": compiler_before,
        "compiler_source_checkout_revision": (
            git_revision(compiler_root) if compiler_root is not None else None
        ),
        "compiler_identity_scope": (
            "Binary SHA-256 identifies the executable; source checkout revision, "
            "when available, does not assert which source built that executable"
        ),
        "compiler_version": version,
        "host": {"system": platform.system(), "machine": platform.machine()},
        "checks": {
            "format": "passed", "check_all_targets": "passed",
            "tests_engine_both": {
                "passed": count, "failed": 0, "names": sorted(expected),
            },
            "examples": [
                {"path": lesson["path"], "engines": ["vm", "native-debug", "native-release"]}
                for lesson in lessons
            ],
        },
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        f"Marimay corpus verified: {count} tests in VM/native; "
        f"{len(lessons)} examples in VM/native debug/release."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        raise SystemExit(str(error))
