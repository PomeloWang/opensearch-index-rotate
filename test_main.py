import unittest

from datetime import datetime
from main import build_filter_function, filter_by_age


class TestFilterByAge(unittest.TestCase):
    def setUp(self) -> None:
        self.indices = [
            "pdauditlog-2021-10-01",
            "pdauditlog-2021-10-02",
            "pdauditlog-2021-10-03",
            "pddebuglog-2021-10-01",
            "pddebuglog-2021-10-02",
            "pddebuglog-2021-10-03",
        ]
        return

    def test_filter_2_days_ago(
        self, unit_count: int = 2, today_timestring: str = "2021-10-04"
    ):
        print(f"\nIndices: {self.indices}")
        print(f"Today ==> {today_timestring}")

        fn = build_filter_function(
            unit_count,
            today_timeobj=datetime.strptime(str(today_timestring), "%Y-%m-%d"),
        )
        indices = filter_by_age(fn, self.indices)

        print(f"Filter {unit_count} days ago indices.")
        print(f"Found {len(indices)} indices {indices}")
        self.assertEqual(
            indices,
            [
                "pdauditlog-2021-10-01",
                "pddebuglog-2021-10-01",
            ],
        )

    def test_filter_empty_indices(
        self, unit_count: int = 10, today_timestring: str = "2021-10-04"
    ):
        print(f"\nIndices: {self.indices}")
        print(f"Today ==> {today_timestring}")

        fn = build_filter_function(
            unit_count,
            today_timeobj=datetime.strptime(str(today_timestring), "%Y-%m-%d"),
        )
        indices = filter_by_age(fn, self.indices)

        print(f"Filter {unit_count} days ago indices.")
        print(f"Found {len(indices)} indices {indices}")
        self.assertEqual(indices, [])


if __name__ == "__main__":
    unittest.main()
