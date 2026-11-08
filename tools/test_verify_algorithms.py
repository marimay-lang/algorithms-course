from __future__ import annotations

from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import verify_algorithms as verifier
from verify_algorithms import test_names, validate_lessons, validate_tests, validate_version


def lesson(root: Path, path: str = "examples/one", stdout: str = "ok\n") -> dict:
    directory = root / path
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "main.my").write_text("fn main(): void {}\n", encoding="utf-8")
    return {"path": path, "stdout": stdout}


def current_version() -> dict:
    return {
        "schema": "marimay.version/2", "compiler": "0.1.0-alpha.1",
        "runtime": "0.1.0-alpha.1", "language": "0.1-design",
        "standardLibrary": {"version": "0.1.0-alpha.1"},
        "commands": {"available": ["build", "check", "fmt", "run", "test", "version"]},
    }


class AlgorithmVerificationTests(unittest.TestCase):
    def test_discovery_covers_nested_packages_and_excludes_cache(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "family").mkdir()
            (root / ".mmay").mkdir()
            (root / "main_test.my").write_text("@test\nfn rootCase(): void {}\n")
            (root / "family/extra_test.my").write_text("@test\nfn nestedCase(): void {}\n")
            (root / ".mmay/cached_test.my").write_text("@test\nfn stale(): void {}\n")
            self.assertEqual(test_names(root), {
                "course.local/algorithms.rootCase",
                "course.local/algorithms/family.nestedCase",
            })

    def test_rejects_skipped_duplicate_failed_or_inconsistent_tests(self) -> None:
        outputs = (
            "test a ... ok\ntest result: ok. 1 passed; 0 failed\n",
            "test a ... ok\ntest a ... ok\ntest result: ok. 2 passed; 0 failed\n",
            "test a ... ok\ntest b ... FAILED\ntest result: FAILED. 1 passed; 1 failed\n",
            "test a ... ok\ntest b ... ok\ntest result: ok. 9 passed; 0 failed\n",
        )
        for output in outputs:
            with self.subTest(output=output), self.assertRaises(ValueError):
                validate_tests(output, {"a", "b"})

    def test_accepts_complete_passing_output(self) -> None:
        output = "test b ... ok\ntest a ... ok\ntest result: ok. 2 passed; 0 failed\n"
        self.assertEqual(validate_tests(output, {"a", "b"}), 2)

    def test_lesson_manifest_accepts_complete_nested_examples_and_empty_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = [lesson(root), lesson(root, "examples/family/two", "")]
            self.assertEqual(validate_lessons(root, manifest), manifest)

    def test_lesson_manifest_rejects_omitted_discovered_example(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = [lesson(root)]
            lesson(root, "examples/two")
            with self.assertRaisesRegex(ValueError, "missing=.*examples/two"):
                validate_lessons(root, manifest)

    def test_lesson_manifest_rejects_extra_or_duplicate_entries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            valid = lesson(root)
            with self.assertRaisesRegex(ValueError, "unexpected=.*examples/absent"):
                validate_lessons(root, [valid, {"path": "examples/absent", "stdout": ""}])
            with self.assertRaisesRegex(ValueError, "duplicate lesson"):
                validate_lessons(root, [valid, valid.copy()])

    def test_lesson_manifest_rejects_unsafe_or_noncanonical_paths(self) -> None:
        paths = (
            "", "../one", "/absolute/one", "examples/../one", "examples/./one",
            "examples//one", "examples/one/", "C:/one", "C:\\one",
            "\\\\server\\one", "examples\\one", "other/one", "examples/\0one",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lesson(root)
            for path in paths:
                with self.subTest(path=path), self.assertRaises(ValueError):
                    validate_lessons(root, [{"path": path, "stdout": ""}])

    def test_lesson_manifest_rejects_bad_shape_and_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lesson(root)
            invalid = (
                None, {}, [], "examples/one", [None], [{}],
                [{"path": "examples/one"}],
                [{"path": "examples/one", "stdout": 3}],
                [{"path": None, "stdout": ""}],
                [{"path": "examples/one", "stdout": "", "typo": True}],
            )
            for manifest in invalid:
                with self.subTest(manifest=manifest), self.assertRaises(ValueError):
                    validate_lessons(root, manifest)

    def test_lesson_manifest_rejects_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            (root / "examples").mkdir(parents=True)
            outside = Path(directory) / "outside"
            outside.mkdir()
            (outside / "main.my").write_text("fn main(): void {}\n")
            try:
                (root / "examples/escape").symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest("symbolic links are unavailable")
            with self.assertRaisesRegex(ValueError, "escapes"):
                validate_lessons(root, [{"path": "examples/escape", "stdout": ""}])

    def test_version_contract_requires_matching_runtime_stdlib_and_commands(self) -> None:
        self.assertEqual(validate_version(current_version()), current_version())
        for field in ("schema", "compiler", "runtime", "language"):
            value = current_version()
            value[field] = "unsupported"
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_version(value)
        for field, value in (
            ("standardLibrary", None), ("standardLibrary", {"version": "other"}),
            ("commands", None), ("commands", {"available": ["fmt"]}),
            ("commands", {"available": ["fmt", "fmt"]}),
            ("commands", {"available": [True]}),
        ):
            version = current_version()
            version[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                validate_version(version)

    def test_compiler_checkout_is_detected_only_for_source_build_layout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "bootstrap/include/mmay").mkdir(parents=True)
            (root / "runtime").mkdir()
            (root / "CMakeLists.txt").write_text("project(Marimay)\n")
            self.assertEqual(verifier.compiler_source_root(root / "build/debug/mmay"), root)
            self.assertEqual(
                verifier.compiler_source_root(root / "build/debug/Debug/mmay.exe"), root
            )
            self.assertIsNone(verifier.compiler_source_root(root / "prefix/bin/mmay"))

    def test_git_metadata_is_optional(self) -> None:
        with patch.object(verifier.subprocess, "run", side_effect=FileNotFoundError):
            self.assertIsNone(verifier.git_revision(Path("source")))
            self.assertIsNone(verifier.working_tree_dirty(Path("source")))

    def run_mock_verification(self, root: Path, mutate_compiler: bool) -> dict:
        manifest = [lesson(root)]
        (root / "tools").mkdir()
        (root / "mmay.mod").write_text('module "course.local/algorithms"\n')
        (root / "lessons.json").write_text(json.dumps(manifest))
        (root / "main_test.my").write_text("@test\nfn sample(): void {}\n")
        compiler = root / "prefix/bin/mmay"
        compiler.parent.mkdir(parents=True)
        compiler.write_bytes(b"original compiler")
        report = root / "build/report.json"

        def fake_execute(argv: list[str], cwd: Path) -> str:
            if len(argv) == 1:
                return "ok\n"
            if argv[1] == "version":
                return json.dumps(current_version())
            if argv[1] == "test":
                if mutate_compiler:
                    compiler.write_bytes(b"changed compiler")
                return (
                    "test course.local/algorithms.sample ... ok\n"
                    "test result: ok. 1 passed; 0 failed\n"
                )
            return "ok\n" if argv[1] == "run" else ""

        argv = ["verify_algorithms.py", "--mmay", str(compiler), "--output", str(report)]
        with (
            patch.object(verifier, "__file__", str(root / "tools/verify_algorithms.py")),
            patch.object(verifier, "execute", side_effect=fake_execute),
            patch.object(verifier, "git_revision", return_value="base-commit") as revision,
            patch.object(verifier, "working_tree_dirty", return_value=True),
            patch("sys.argv", argv),
            redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(verifier.main(), 0)
            revision.assert_called_once_with(root)
        return json.loads(report.read_text())

    def test_runner_rejects_compiler_changes_during_verification(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "compiler changed"):
                self.run_mock_verification(Path(directory), mutate_compiler=True)

    def test_report_identifies_dirty_source_and_actual_installed_binary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report = self.run_mock_verification(Path(directory), mutate_compiler=False)
            self.assertTrue(report["working_tree_dirty"])
            self.assertEqual(report["repository_revision"], "base-commit")
            self.assertIsNone(report["compiler_source_checkout_revision"])
            self.assertNotIn("compiler_source_revision", report)
            self.assertEqual(
                report["compiler_sha256"], hashlib.sha256(b"original compiler").hexdigest()
            )


if __name__ == "__main__":
    unittest.main()
