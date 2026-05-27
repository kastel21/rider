"""Unit tests for trip others free-text aggregation."""

from django.test import SimpleTestCase

from operations.services.other_specify_aggregate import (
    aggregate_other_specify_texts,
    parse_other_specify,
)


class ParseOtherSpecifyTests(SimpleTestCase):
    def test_count_and_label(self):
        self.assertEqual(parse_other_specify("8 CD4, 10 FBC"), [(8, "CD4"), (10, "FBC")])

    def test_hyphenated_label(self):
        self.assertEqual(parse_other_specify("17 COVID-19"), [(17, "COVID-19")])

    def test_glued_count(self):
        self.assertEqual(parse_other_specify("10fbc"), [(10, "fbc")])

    def test_opaque_segments_omitted_from_parse(self):
        self.assertEqual(parse_other_specify("misc samples"), [])


class AggregateOtherSpecifyTextsTests(SimpleTestCase):
    def test_merge_same_category_across_strings(self):
        self.assertEqual(
            aggregate_other_specify_texts(["5 CD4", "3 CD4"]),
            "8 CD4",
        )

    def test_merge_within_and_across_strings(self):
        self.assertEqual(
            aggregate_other_specify_texts(["5 CD4, 2 FBC", "3 CD4"]),
            "8 CD4, 2 FBC",
        )

    def test_case_insensitive_merge_preserves_first_casing(self):
        self.assertEqual(
            aggregate_other_specify_texts(["5 cd4", "3 CD4"]),
            "8 cd4",
        )

    def test_glued_count_merges_by_label(self):
        self.assertEqual(
            aggregate_other_specify_texts(["10fbc", "5 fbc"]),
            "15 fbc",
        )

    def test_empty_input(self):
        self.assertEqual(aggregate_other_specify_texts([]), "")
        self.assertEqual(aggregate_other_specify_texts(["", "  "]), "")

    def test_opaque_segment_preserved(self):
        self.assertEqual(
            aggregate_other_specify_texts(["misc samples", "misc samples"]),
            "misc samples",
        )

    def test_counted_and_opaque_combined(self):
        self.assertEqual(
            aggregate_other_specify_texts(["5 CD4", "misc samples"]),
            "5 CD4, misc samples",
        )
