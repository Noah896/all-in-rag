import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = ROOT / "code" / "C8"
DATA_DIR = ROOT / "data" / "C8" / "cook"


class DatasetTests(unittest.TestCase):
    def test_dataset_is_present_and_complete(self):
        markdown_files = list(DATA_DIR.rglob("*.md"))
        self.assertGreaterEqual(len(markdown_files), 300)
        self.assertTrue(all(path.stat().st_size > 0 for path in markdown_files))

    def test_markdown_files_are_utf8_and_have_headings(self):
        markdown_files = list(DATA_DIR.rglob("*.md"))
        files_with_headings = 0

        for path in markdown_files:
            content = path.read_text(encoding="utf-8")
            if any(line.startswith("# ") for line in content.splitlines()):
                files_with_headings += 1

        self.assertGreaterEqual(files_with_headings, len(markdown_files) - 5)


class ConfigurationTests(unittest.TestCase):
    def test_default_paths_resolve_from_any_working_directory(self):
        sys.path.insert(0, str(PROJECT_DIR))
        try:
            from config import RAGConfig
        finally:
            sys.path.pop(0)

        config = RAGConfig()
        self.assertTrue(Path(config.data_path).is_dir())
        self.assertEqual(
            Path(config.index_save_path).resolve(),
            (PROJECT_DIR / "vector_index").resolve(),
        )


if __name__ == "__main__":
    unittest.main()

