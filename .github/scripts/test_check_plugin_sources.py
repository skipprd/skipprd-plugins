#!/usr/bin/env python3

import unittest

from check_plugin_sources import FORBIDDEN_SOURCE, collect_violations


class CheckPluginSourcesTests(unittest.TestCase):
    def test_live_catalog_has_no_host_imports(self) -> None:
        self.assertEqual(collect_violations(), [])

    def test_bans_skipprd_and_skippr_core(self) -> None:
        self.assertIn("skipprd crate import", FORBIDDEN_SOURCE)
        self.assertIn("direct skippr_core import", FORBIDDEN_SOURCE)

    def test_bans_host_running_rwlock_pattern(self) -> None:
        self.assertIn("SDK RUNNING is AtomicBool", FORBIDDEN_SOURCE)


if __name__ == "__main__":
    unittest.main()
