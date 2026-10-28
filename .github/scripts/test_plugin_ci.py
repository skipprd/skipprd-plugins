#!/usr/bin/env python3

from __future__ import annotations

import unittest
from pathlib import Path

CI = Path(__file__).resolve().parents[1] / "workflows" / "ci.yml"


class PluginCiTests(unittest.TestCase):
    def test_skipprd_checkout_pins_invert_branch_until_main_has_split(self) -> None:
        text = CI.read_text(encoding="utf-8")
        self.assertGreaterEqual(text.count("repository: skipprd/skipprd"), 2)
        self.assertGreaterEqual(
            text.count("ref: issue-23-plugin-repos"),
            2,
            "catalog CI must compile against the inverted skipprd branch until it is main",
        )


if __name__ == "__main__":
    unittest.main()
