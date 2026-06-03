from __future__ import annotations

"""Default project entry point.

The CLI itself lives in :mod:`app_cli`. This file exists to define the
project's preferred generator configuration, especially the weighting of the
soft constraints.

To customize the generator for experiments, adjust :func:`build_constraints`
below and run::

    python3 code/main.py --form sentence --pdf

The rest of the command-line workflow, including parsing, rendering, and
rerender mode, is handled by ``app_cli.run_cli``.
"""

from app_cli import run_cli
from melody_engine import (
    ChordTonePreferenceConstraint,
    DirectionChangeConstraint,
    LargeLeapConstraint,
    LeapRecoveryConstraint,
    LeadingToneResolutionConstraint,
    MotifPreferenceConstraint,
    FormSectionConstraint,
    PhraseCadenceConstraint,
    RepeatedPitchConstraint,
    RestConstraint,
    SingleClimaxConstraint,
    StepwiseMotionConstraint,
    StrongBeatStabilityConstraint,
)


def build_constraints() -> list:
    """Construct the weighted soft-constraint stack used by the default CLI configuration."""
    return [
        StepwiseMotionConstraint(weight=1.5),
        LargeLeapConstraint(weight=1.8),
        LeapRecoveryConstraint(weight=1.2),
        LeadingToneResolutionConstraint(weight=1.3),
        ChordTonePreferenceConstraint(weight=1.4),
        StrongBeatStabilityConstraint(weight=1.0),
        PhraseCadenceConstraint(weight=1.6),
        SingleClimaxConstraint(weight=1.5),
        MotifPreferenceConstraint(weight=1.0),
        RepeatedPitchConstraint(weight=1.0),
        DirectionChangeConstraint(weight=0.9),
        RestConstraint(weight=1.2),
        FormSectionConstraint(weight=1.0),
    ]
def main() -> None:
    """Run the default project CLI configuration."""
    run_cli(build_constraints)


if __name__ == "__main__":
    main()
