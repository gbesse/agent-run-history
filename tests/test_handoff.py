import unittest

from handoff_receipt import audit


class HandoffTests(unittest.TestCase):
    def test_accepted_but_absent_turn_is_missing(self):
        rows = [{"turn_id": "1", "operation_id": "op", "marker": "M1",
                 "phase": "accepted", "mode": "append"}]
        self.assertEqual(audit(rows, "")["turns"][0]["state"], "missing")

    def test_failed_reply_is_uncertain_even_when_marker_absent(self):
        rows = [{"turn_id": "1", "operation_id": "op", "marker": "M1",
                 "phase": "failed"}]
        self.assertEqual(audit(rows, "")["turns"][0]["state"], "uncertain")

    def test_present_marker_resolves_uncertain_handoff(self):
        rows = [{"turn_id": "1", "operation_id": "op", "marker": "M1",
                 "phase": "failed", "mode": "replace"}]
        self.assertTrue(audit(rows, "something M1 here")["ok"])


if __name__ == "__main__":
    unittest.main()
