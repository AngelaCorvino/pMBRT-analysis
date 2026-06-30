"""BEDR placeholder.

No BEDR calculation was found in the inspected legacy scripts. This module is
kept explicit so that a future manuscript-defined formula can be added without
silently inventing a method.
"""


def compute_bedr(*args, **kwargs):
    """Raise until the manuscript BEDR formula is supplied."""

    raise NotImplementedError(
        "BEDR was requested for the public summary table, but no BEDR formula "
        "was present in the inspected legacy analysis scripts."
    )
