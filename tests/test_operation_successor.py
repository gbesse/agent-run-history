import unittest

from operation_successor import inspect


class SuccessorTests(unittest.TestCase):
    def test_explicit_successor(self):
        failed = {"id": "a", "status": "failed", "bank_id": "b", "source_ids": ["x"], "superseded_by": "z"}
        successor = {"id": "z", "status": "completed", "bank_id": "b", "source_ids": ["x"], "supersedes": "a"}
        self.assertEqual(inspect([failed, successor])["status"], "covered")
        self.assertEqual(inspect([failed, {**successor, "source_ids": ["y"]}])["status"], "inconclusive")
        self.assertEqual(inspect([{**failed, "superseded_by": None}])["status"], "unresolved")


if __name__ == "__main__":
    unittest.main()
