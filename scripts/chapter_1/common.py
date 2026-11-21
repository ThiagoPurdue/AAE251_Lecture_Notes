"""The one import line of a Chapter 1 page module:

    from chapter_1.common import *

It brings the figure kit and the chapter style (style.py: record, save_figure, fmt, text,
callout, arrow, dimension, the arrow kinds, the fills and line weights), units and Earth (constants.py), the physics
(atmosphere.py, flow.py, sizing.py), the operating environment (environment.py), the shapes (geometry.py, aircraft.py, launchers.py), and the
drawing helpers for
hardware (drawing.py) and diagrams (diagrams.py). The API is in scripts/chapter_1/README.md.
"""
from chapter_1.style import *        # noqa: F401,F403
from chapter_1.constants import *    # noqa: F401,F403
from chapter_1.atmosphere import *   # noqa: F401,F403
from chapter_1.environment import *  # noqa: F401,F403
from chapter_1.flow import *         # noqa: F401,F403
from chapter_1.sizing import *       # noqa: F401,F403
from chapter_1.geometry import *     # noqa: F401,F403
from chapter_1.aircraft import *     # noqa: F401,F403
from chapter_1.launchers import *    # noqa: F401,F403
from chapter_1.drawing import *      # noqa: F401,F403
from chapter_1.diagrams import *     # noqa: F401,F403
