"""The one import line of a Chapter 5 page module:

    from chapter_5.common import *

Brings Chapter 1's style, constants, atmosphere, geometry, aircraft, drawing and diagrams,
Chapter 3's aerodynamics and vector/angle/disc helpers, then rebinds Chapter 5's record,
save_figure, write_values, perf, and drawing5.
"""
from chapter_1.style import *        # noqa: F401,F403
from chapter_1.constants import *    # noqa: F401,F403
from chapter_1.atmosphere import *   # noqa: F401,F403
from chapter_1.geometry import *     # noqa: F401,F403
from chapter_1.aircraft import *     # noqa: F401,F403
from chapter_1.drawing import *      # noqa: F401,F403
from chapter_1.diagrams import *     # noqa: F401,F403
from chapter_3.aero import polar_K, polar_CD, min_drag_point, level_CL, dynamic_pressure  # noqa: F401
from chapter_3.drawing3 import disc, vector, angle_mark, ray, unit, rotate, step_label  # noqa: F401
from chapter_5.style import *        # noqa: F401,F403
from chapter_5.perf import *         # noqa: F401,F403
from chapter_5.drawing5 import *     # noqa: F401,F403
from chapter_5.style import record, save_figure, write_values, VALUES, WRITTEN, PAGES, CHAPTER  # noqa: F401,E402
