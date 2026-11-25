"""The one import line of a Chapter 4 page module:

    from chapter_4.common import *

It brings the figure kit and Chapter 1's style (chapter_1.style: fmt, text, callout, arrow,
dimension, kind_arrow, flow_arrow, legend_key, pt, the fills, line weights and arrow kinds), units
(constants.py), the atmosphere of page 1.4 and the flow relations of page 1.5 (atmosphere.py,
flow.py), the shapes and their drawing (geometry.py; launchers.py: launch_vehicle,
two_stage_vehicle, draw_cutaway, bell_contour, engine_side, PROPELLANT_STYLE, ARIANE5, FALCON9;
drawing.py: draw_parts, label_part, hatched_wall, dimension_outside), the diagram helpers
(diagrams.py: canvas, box, route, step_marker, key_disc, brace, trim_canvas), Chapter 3's numbered
disc and vector helpers (drawing3.disc, vector, step_label), then Chapter 4's own record and saver
(chapter_4/style.py) and its modules: rocket, staging, nozzle, published, drawing4, and the bridge
to the published numbers of Chapters 1 and 2 (links.py: HOHMANN_22, LAUNCH_23, ARIANE5_CORE). The API
is in scripts/chapter_4/README.md.

Name clashes resolved on purpose: `G0` is 9.81 m/s^2 everywhere (page 1.4's value, the one used
throughout the course); Chapter 2's orbit code comes only through links.py (a star import of
chapter_2.orbits would rebind record and save_figure to Chapter 2's).
"""
from chapter_1.style import *        # noqa: F401,F403
from chapter_1.constants import *    # noqa: F401,F403
from chapter_1.atmosphere import *   # noqa: F401,F403
from chapter_1.flow import *         # noqa: F401,F403
from chapter_1.geometry import *     # noqa: F401,F403
from chapter_1.launchers import *    # noqa: F401,F403
from chapter_1.launchers import HATCH_INK  # noqa: F401
from chapter_1.drawing import *      # noqa: F401,F403
from chapter_1.diagrams import *     # noqa: F401,F403
from chapter_3.drawing3 import disc, vector, step_label, unit, data_per_pt  # noqa: F401
from chapter_4.style import *        # noqa: F401,F403  (record, save_figure, write_values of Chapter 4)
from chapter_4.rocket import *       # noqa: F401,F403
from chapter_4.staging import *      # noqa: F401,F403
from chapter_4.nozzle import *       # noqa: F401,F403
from chapter_4.published import *    # noqa: F401,F403
from chapter_4.links import *        # noqa: F401,F403
from chapter_4.drawing4 import *     # noqa: F401,F403
from chapter_4.style import record, save_figure, write_values, VALUES, WRITTEN, PAGES, CHAPTER  # noqa: F401,E402
