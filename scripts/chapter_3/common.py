"""The one import line of a Chapter 3 page module:

    from chapter_3.common import *

It brings the figure kit and Chapter 1's style (chapter_1.style: fmt, text, callout, arrow,
dimension, angle_arc, kind_arrow, flow_arrow, moment_arrow, legend_key, pt, the fills, line
weights and arrow kinds), units and Earth (constants.py), the atmosphere, continuity, Bernoulli
and the manometer (atmosphere.py, flow.py), the shapes and their drawing (geometry.py: naca4,
planform; aircraft.py: the 737-800 in three views; drawing.py: draw_parts, label_part,
hatched_wall, draw_manometer, dimension_outside), the diagram helpers (diagrams.py: canvas, box,
route, step_marker, key_disc, brace, trim_canvas), then Chapter 3's own record and saver
(chapter_3/style.py: record, save_figure and write_values of Chapter 3) and its modules: aero,
tunnel, airfoil_data, drawing3, published. The API is in scripts/chapter_3/README.md.

Name clashes resolved on purpose: `dynamic_pressure` and `manometer_dp` are Chapter 3's (same
formulas as Chapter 1's); `G0` is 9.81 m/s^2 in both (the value used throughout the course); `T_SL`, `RHO_SL` are the values of page 1.4.
"""
from chapter_1.style import *        # noqa: F401,F403
from chapter_1.constants import *    # noqa: F401,F403
from chapter_1.atmosphere import *   # noqa: F401,F403
from chapter_1.flow import *         # noqa: F401,F403
from chapter_1.geometry import *     # noqa: F401,F403
from chapter_1.aircraft import *     # noqa: F401,F403
from chapter_1.drawing import *      # noqa: F401,F403
from chapter_1.diagrams import *     # noqa: F401,F403
from chapter_3.style import *        # noqa: F401,F403  (record, save_figure, write_values of Chapter 3)
from chapter_3.aero import *         # noqa: F401,F403
from chapter_3.tunnel import *       # noqa: F401,F403
from chapter_3.airfoil_data import *  # noqa: F401,F403
from chapter_3.drawing3 import *     # noqa: F401,F403
from chapter_3.published import *    # noqa: F401,F403
from chapter_3.style import record, save_figure, write_values, VALUES, WRITTEN, PAGES, CHAPTER  # noqa: F401,E402
