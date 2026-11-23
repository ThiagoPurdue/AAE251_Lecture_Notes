"""Measured airfoil section data, redrawn from NACA Report 824, and the helper that draws them in
the report's chart layout (3.2 Airfoil and Finite Wing, 3.3 Drag Polar).

Source: Abbott, I. H., von Doenhoff, A. E., and Stivers, L. S., Jr., "Summary of Airfoil Data",
NACA Report 824, 1945 (NASA Technical Reports Server 19930090976), Supplementary Data V,
"Aerodynamic characteristics of various airfoil sections": the unnumbered chart pages
  - report page 192, "Aerodynamic characteristics of the NACA 64(3)-018 airfoil section, 24-inch
    chord" (symmetric, 18 percent thick), and
  - report page 195, the same for the NACA 64(3)-618 airfoil section (cambered for a design lift
    coefficient of 0.6, 18 percent thick; same thickness form).
Each chart shows, for smooth models at Reynolds numbers 3.0, 6.0 and 9.0 million (circles,
squares, diamonds), c_l and c_m,c/4 against the section angle of attack (left panel) and c_d
and c_m,ac against c_l (right panel), plus standard-roughness and split-flap runs (not recorded).
The report's chart pages carry no figure number: cite them by page.

How the numbers were read: each page was rendered at the
scan's own 300 dpi; every grid line was located and fitted (the scan is turned about 0.7 deg and
the printed grid is uneven by up to 2 px), and a point is mapped by interpolating between its
neighboring grid lines. The plotted symbols were found by their outline (circle, square,
diamond), checked one by one on enlarged overlays, and the ones hidden in clusters were read by
eye at 4x. Where the three Reynolds-number curves lie on one line (the straight part of the lift
curve) every smooth-model symbol there counts for all three. The values are the centers of the
test-point symbols (the report's curves join them): angles to 0.01 deg, c_l to 0.001, c_m to
0.0001, c_d to 0.00001. A reading is good to about +-0.005 in c_l, +-0.1 deg, +-0.00005 in c_d
and +-0.002 in c_m (a third of a symbol).

Section characteristics stated by the report (unit checks in this file):
  - a.c. position, from the table on each chart: 64(3)-618: x/c = 0.289, 0.275, 0.273 and
    y/c = 0.074, 0.005, -0.019 at 3, 6, 9 million; 64(3)-018: x/c = 0.269, 0.268, 0.266 and
    y/c = -0.053, -0.054, -0.044.
  - Figure 37(c) (zero-lift angle at R = 6 million): -4.0 deg for the 64-series section of
    design lift 0.6 at 18 percent thickness; 0 for the symmetric one. The chart's own lift curve
    crosses zero at -3.7 deg: the summary figure and the chart page differ by 0.3 deg inside the
    report (checked on the scan: the symbols at c_l = 0 sit at -3.75 deg).
  - Figure 38(c) (lift-curve slope, R = 6 million, smooth): 0.108 to 0.118 per deg for the
    64-series sections of 15 to 21 percent thickness.
  - Figure 41(d) (maximum lift, 18 percent thick 64-series): about 1.22, 1.36, 1.50 (c_li = 0)
    and 1.38, 1.53, 1.62 (c_li = 0.6, flagged symbols) at 3, 6, 9 million.

Ordinates: Supplementary Data III, report pages 105 and 106 (NACA 64(3)-018 and 64(3)-618, upper
and lower surface stations and ordinates in percent of chord; leading-edge radius 2.208 percent
of chord). The cambered section is the thickness form laid on the NACA a = 1.0 mean line for
c_li = 0.6 (report pages 4 to 6, and Supplementary Data II): a unit check rebuilds the
tabulated ordinates from that construction.

Designation (report page 5): NACA 64(3)-618: 6-series; minimum pressure of the basic symmetric
section at 0.4 c; the subscript 3: low drag within c_l = 0.6 +- 0.3; design lift coefficient 0.6;
18 percent thick. In figure text write "NACA 64$_3$-618".

Run this file for its unit checks:  python3 -B scripts/chapter_3/airfoil_data.py
"""
import math
import sys
from pathlib import Path

import numpy as np

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# ===================================================================== the recorded data
# DATA[airfoil][curve][Reynolds number] = [(x, y), ...] in increasing x:
#   cl_alpha: (alpha deg, c_l); cm_alpha: (alpha deg, c_m,c/4); cd_cl: (c_l, c_d); cmac_cl: (c_l, c_m,ac)
DATA = {
    '64-618': {
        'cl_alpha': {
            3.0e6: [(-14.10, -0.991), (-12.11, -0.867), (-10.15, -0.685), (-7.63, -0.419), (-6.01, -0.273), (-4.94, -0.141), (-4.06, -0.043), (-2.94, 0.092), (-1.71, 0.244), (-1.00, 0.332), (0.02, 0.446), (1.08, 0.558), (3.15, 0.797), (4.19, 0.917), (5.02, 1.014), (5.02, 1.014), (6.12, 1.095), (8.15, 1.192), (10.23, 1.256), (11.20, 1.275), (12.32, 1.293), (13.24, 1.320), (14.21, 1.338), (15.22, 1.366), (16.27, 1.366), (17.19, 1.358), (18.27, 1.354), (19.21, 1.354), (20.26, 1.311), (21.23, 1.270), (22.36, 1.215), (24.29, 1.189)],
            6.0e6: [(-16.91, -1.088), (-16.07, -1.110), (-14.98, -1.075), (-14.01, -1.073), (-12.99, -1.007), (-11.60, -0.807), (-10.98, -0.709), (-10.39, -0.767), (-9.63, -0.603), (-7.63, -0.419), (-6.01, -0.273), (-4.94, -0.141), (-4.06, -0.043), (-2.94, 0.092), (-1.71, 0.244), (-1.00, 0.332), (0.02, 0.446), (1.08, 0.558), (3.15, 0.797), (5.02, 1.014), (6.12, 1.095), (8.20, 1.233), (10.21, 1.404), (12.30, 1.454), (13.17, 1.483), (14.35, 1.472), (15.14, 1.493), (16.36, 1.498), (17.23, 1.495), (18.35, 1.513), (19.19, 1.510), (20.24, 1.493), (22.25, 1.425), (24.20, 1.293)],
            9.0e6: [(-14.10, -0.966), (-10.05, -0.728), (-7.63, -0.419), (-6.01, -0.273), (-4.94, -0.141), (-4.06, -0.043), (-2.94, 0.092), (-1.71, 0.244), (-1.00, 0.332), (0.02, 0.446), (1.08, 0.558), (3.15, 0.797), (4.19, 0.917), (5.02, 1.014), (6.12, 1.095), (8.20, 1.233), (10.17, 1.431), (12.26, 1.503), (13.24, 1.536), (14.26, 1.544), (16.32, 1.580), (17.19, 1.587), (18.32, 1.592), (19.21, 1.610), (20.43, 1.604), (21.30, 1.572), (22.38, 1.529), (23.25, 1.325)],
        },
        'cm_alpha': {
            3.0e6: [(-8.07, -0.0648), (-7.17, -0.0750), (-4.49, -0.0862), (-3.63, -0.0897), (-2.20, -0.0872), (-0.81, -0.1009), (0.00, -0.1030), (1.69, -0.1112), (3.44, -0.1181), (3.69, -0.1275), (5.62, -0.1473), (6.76, -0.1420), (7.80, -0.1415), (8.89, -0.1362), (9.77, -0.1316), (10.84, -0.1304), (11.64, -0.1359), (12.93, -0.1360), (13.79, -0.1348), (14.90, -0.1322), (15.69, -0.1377), (16.93, -0.1358), (17.85, -0.1373), (19.01, -0.1388), (19.90, -0.1382), (21.05, -0.1390), (22.13, -0.1452), (24.16, -0.1591)],
            6.0e6: [(-18.21, 0.0241), (-17.05, 0.0133), (-16.21, 0.0019), (-15.38, -0.0196), (-14.42, -0.0341), (-13.27, -0.0560), (-12.49, -0.0676), (-8.53, -0.0796), (-6.43, -0.0832), (-2.32, -0.0946), (-0.45, -0.0996), (1.65, -0.1012), (5.48, -0.1250), (6.35, -0.1224), (7.33, -0.1179), (8.69, -0.1174), (9.57, -0.1155), (10.64, -0.1156), (11.55, -0.1150), (12.68, -0.1172), (13.54, -0.1133), (16.84, -0.1104), (18.77, -0.1093), (19.61, -0.1087), (20.68, -0.1155), (21.61, -0.1183), (23.55, -0.1292)],
            9.0e6: [(-10.87, -0.0759), (-8.75, -0.0816), (-4.76, -0.0909), (-2.72, -0.0966), (1.09, -0.1091), (3.07, -0.1154), (4.99, -0.1183), (7.01, -0.1138), (8.20, -0.1140), (9.19, -0.1128), (9.78, -0.1195), (10.17, -0.1102), (11.07, -0.1110), (12.20, -0.1078), (13.06, -0.1099), (14.14, -0.1080), (15.24, -0.1062), (16.31, -0.1016), (17.29, -0.0984), (18.52, -0.0985), (19.31, -0.0986), (20.48, -0.0981), (21.41, -0.1029), (23.84, -0.1604)],
        },
        'cd_cl': {
            3.0e6: [(-0.862, 0.01812), (-0.680, 0.01310), (-0.475, 0.01070), (-0.251, 0.00914), (-0.125, 0.00833), (-0.018, 0.00793), (0.092, 0.00646), (0.214, 0.00597), (0.348, 0.00584), (0.444, 0.00585), (0.550, 0.00600), (0.678, 0.00591), (0.782, 0.00599), (0.887, 0.00609), (1.085, 0.00699), (1.192, 0.01419)],
            6.0e6: [(-1.066, 0.01605), (-0.918, 0.01350), (-0.708, 0.01098), (-0.490, 0.00907), (-0.258, 0.00818), (-0.017, 0.00714), (0.094, 0.00630), (0.217, 0.00545), (0.344, 0.00514), (0.451, 0.00533), (0.571, 0.00539), (0.685, 0.00530), (0.792, 0.00511), (1.015, 0.00631), (1.088, 0.00867), (1.257, 0.01253), (1.408, 0.01632)],
            9.0e6: [(-0.926, 0.01258), (-0.722, 0.01023), (-0.280, 0.00772), (-0.144, 0.00714), (-0.021, 0.00671), (0.094, 0.00646), (0.247, 0.00531), (0.277, 0.00507), (0.344, 0.00477), (0.461, 0.00490), (0.569, 0.00496), (0.692, 0.00475), (0.805, 0.00471), (1.013, 0.00665), (1.042, 0.00691), (1.110, 0.00883), (1.273, 0.01172), (1.434, 0.01470), (1.509, 0.01577)],
        },
        'cmac_cl': {
            3.0e6: [(-0.747, -0.0864), (-0.552, -0.0806), (-0.327, -0.0837), (0.108, -0.0837), (0.330, -0.0895), (0.561, -0.0878), (0.797, -0.0896), (1.203, -0.0766), (1.245, -0.0698)],
            6.0e6: [(-1.043, -0.0818), (-1.003, -0.0928), (-0.825, -0.0931), (-0.617, -0.0948), (-0.402, -0.0917), (-0.174, -0.0900), (-0.126, -0.0908), (-0.080, -0.0909), (-0.043, -0.0909), (0.056, -0.0918), (0.247, -0.0935), (0.288, -0.0922), (0.383, -0.0923), (0.420, -0.0917), (1.057, -0.0934), (1.132, -0.0881), (1.228, -0.0848), (1.280, -0.0828)],
            9.0e6: [(-0.886, -0.1005), (-0.668, -0.0995), (-0.449, -0.0978), (0.009, -0.0938), (0.242, -0.1009), (0.469, -0.0979), (0.694, -0.0976), (0.914, -0.0973), (1.091, -0.0914), (1.189, -0.0868), (1.277, -0.0890), (1.354, -0.0843), (1.464, -0.0818), (1.493, -0.0811)],
        },
    },
    '64-018': {
        'cl_alpha': {
            3.0e6: [(-12.16, -1.255), (-10.10, -1.094), (-7.02, -0.790), (-6.10, -0.661), (-3.96, -0.463), (-2.01, -0.235), (0.05, 0.000), (2.00, 0.208), (4.08, 0.437), (6.22, 0.668), (8.22, 0.888), (9.00, 0.939), (10.17, 1.010), (12.19, 1.117), (13.24, 1.154), (14.14, 1.186), (15.10, 1.184), (16.12, 1.202), (17.21, 1.176), (18.25, 1.128), (20.24, 1.001)],
            6.0e6: [(-21.16, -1.149), (-20.25, -1.283), (-19.18, -1.385), (-18.12, -1.412), (-17.26, -1.417), (-16.23, -1.431), (-15.09, -1.404), (-14.11, -1.374), (-13.13, -1.305), (-7.02, -0.790), (-6.10, -0.661), (-3.96, -0.463), (-2.01, -0.235), (0.05, 0.000), (2.00, 0.208), (4.08, 0.437), (6.22, 0.668), (8.12, 0.885), (8.31, 0.891), (10.05, 1.047), (12.19, 1.205), (13.19, 1.259), (14.14, 1.295), (15.22, 1.329), (16.26, 1.347), (17.28, 1.339), (18.25, 1.337), (19.26, 1.321), (19.30, 1.323), (20.23, 1.199), (21.26, 1.130)],
            9.0e6: [(-7.02, -0.790), (-6.10, -0.661), (-3.96, -0.463), (-2.01, -0.235), (0.05, 0.000), (2.00, 0.208), (4.08, 0.437), (6.22, 0.668), (8.22, 0.888), (9.00, 0.939), (10.11, 1.085), (12.13, 1.287), (13.23, 1.367), (14.24, 1.417), (15.14, 1.449), (16.11, 1.484), (17.14, 1.500), (18.12, 1.497), (19.15, 1.489), (20.17, 1.409), (21.15, 1.319), (22.14, 1.149)],
        },
        'cm_alpha': {
            3.0e6: [(-10.10, 0.0178), (-4.04, 0.0082), (2.01, -0.0021), (4.05, -0.0054), (5.96, -0.0080), (7.99, -0.0100), (10.00, -0.0126), (12.09, -0.0212), (13.09, -0.0251), (14.04, -0.0278), (15.06, -0.0347), (15.11, -0.0272), (16.08, -0.0374), (17.12, -0.0422), (18.04, -0.0470), (18.15, -0.0306), (19.18, -0.0715)],
            6.0e6: [(-22.01, 0.1100), (-21.48, 0.0958), (-20.10, 0.0809), (-19.14, 0.0711), (-18.08, 0.0482), (-16.19, 0.0395), (-14.99, 0.0301), (-14.00, 0.0233), (-12.11, 0.0185), (-10.37, 0.0300), (-8.09, 0.0171), (-6.08, 0.0130), (7.11, -0.0047), (13.99, -0.0192), (16.02, -0.0326), (16.35, -0.0463), (18.37, -0.0463), (19.12, -0.0442), (19.61, -0.0636), (20.81, -0.0689), (21.59, -0.1010)],
            9.0e6: [(-2.02, 0.0061), (12.09, -0.0146), (13.14, -0.0140), (15.06, -0.0173), (15.97, -0.0225), (17.17, -0.0245), (18.96, -0.0374), (19.93, -0.0583), (20.61, -0.0962), (21.54, -0.1076)],
        },
        'cd_cl': {
            3.0e6: [(-1.036, 0.01613), (-0.855, 0.01268), (-0.665, 0.00973), (-0.564, 0.00808), (-0.478, 0.00636), (-0.355, 0.00603), (-0.236, 0.00601), (-0.116, 0.00588), (-0.013, 0.00588), (0.095, 0.00581), (0.211, 0.00604), (0.321, 0.00581), (0.427, 0.00602), (0.636, 0.00975), (0.838, 0.01266), (1.019, 0.01650)],
            6.0e6: [(-1.259, 0.01561), (-1.091, 0.01279), (-0.898, 0.01034), (-0.675, 0.00879), (-0.519, 0.00779), (-0.358, 0.00511), (-0.240, 0.00489), (-0.169, 0.00481), (-0.127, 0.00479), (-0.006, 0.00481), (0.036, 0.00479), (0.062, 0.00479), (0.178, 0.00484), (0.322, 0.00509), (0.419, 0.00687), (0.430, 0.00648), (0.537, 0.00780), (0.636, 0.00897), (0.860, 0.01039), (1.050, 0.01294), (1.205, 0.01629), (1.301, 0.01887)],
            9.0e6: [(-1.375, 0.01590), (-1.258, 0.01430), (-1.093, 0.01191), (-0.936, 0.01058), (-0.884, 0.00994), (-0.846, 0.00976), (-0.670, 0.00833), (-0.532, 0.00781), (-0.355, 0.00517), (-0.229, 0.00462), (-0.116, 0.00457), (-0.003, 0.00457), (0.109, 0.00463), (0.230, 0.00471), (0.344, 0.00493), (0.448, 0.00671), (0.562, 0.00770), (0.584, 0.00807), (0.884, 0.01005), (1.089, 0.01216), (1.290, 0.01456), (1.361, 0.01659)],
        },
        'cmac_cl': {
            3.0e6: [(-1.115, -0.0092), (-0.866, 0.0003), (-0.685, 0.0036), (-0.254, 0.0049), (0.222, 0.0024), (0.454, 0.0018), (0.638, 0.0005), (0.853, -0.0022), (1.029, -0.0042), (1.163, -0.0104)],
            6.0e6: [(-1.077, -0.0031), (-0.923, -0.0031), (-0.709, -0.0024), (0.420, 0.0024), (1.043, -0.0042), (1.222, -0.0049), (1.264, -0.0042), (1.339, -0.0117)],
            9.0e6: [(-0.910, -0.0024), (-0.467, 0.0056), (0.035, 0.0030), (1.144, -0.0035), (1.236, -0.0056), (1.275, -0.0022), (1.318, -0.0049), (1.380, -0.0090), (1.420, -0.0103)],
        },
    },
}

AIRFOILS = {
    "64-618": dict(
        name="NACA 64$_3$-618", text="NACA 64<sub>3</sub>-618", plain="NACA 643-618", kind="cambered",
        thickness=0.18, design_cl=0.6, report_page=195, pdf_page=197,
        ac={3.0e6: (0.289, 0.074), 6.0e6: (0.275, 0.005), 9.0e6: (0.273, -0.019)},
        summary=dict(alpha_L0=-4.0, slope_band=(0.108, 0.118), clmax={3.0e6: 1.38, 6.0e6: 1.53, 9.0e6: 1.62}),
    ),
    "64-018": dict(
        name="NACA 64$_3$-018", text="NACA 64<sub>3</sub>-018", plain="NACA 643-018", kind="symmetric",
        thickness=0.18, design_cl=0.0, report_page=192, pdf_page=194,
        ac={3.0e6: (0.269, -0.053), 6.0e6: (0.268, -0.054), 9.0e6: (0.266, -0.044)},
        summary=dict(alpha_L0=0.0, slope_band=(0.104, 0.115), clmax={3.0e6: 1.22, 6.0e6: 1.36, 9.0e6: 1.50}),
    ),
}
REYNOLDS = (3.0e6, 6.0e6, 9.0e6)
CURVES = ("cl_alpha", "cm_alpha", "cd_cl", "cmac_cl")

# Ordinates, percent of chord (report pages 105 and 106): upper (station, ordinate), lower (station, ordinate)
ORD_64_3_018 = [(0, 0), (0.5, 1.428), (0.75, 1.720), (1.25, 2.177), (2.5, 3.005), (5.0, 4.186), (7.5, 5.076),
                (10, 5.803), (15, 6.942), (20, 7.782), (25, 8.391), (30, 8.789), (35, 8.979), (40, 8.952),
                (45, 8.630), (50, 8.114), (55, 7.445), (60, 6.658), (65, 5.782), (70, 4.842), (75, 3.866),
                (80, 2.888), (85, 1.951), (90, 1.101), (95, 0.400), (100, 0)]
ORD_64_3_618_UPPER = [(0, 0), (0.150, 1.534), (0.359, 1.885), (0.805, 2.452), (1.982, 3.518), (4.417, 5.093),
                      (6.895, 6.312), (9.395, 7.322), (14.427, 8.937), (19.486, 10.153), (24.560, 11.065),
                      (29.645, 11.698), (34.735, 12.065), (39.827, 12.163), (44.917, 11.915), (50.000, 11.423),
                      (55.071, 10.730), (60.129, 9.870), (65.171, 8.870), (70.196, 7.754), (75.203, 6.544),
                      (80.191, 5.270), (85.161, 3.963), (90.115, 2.646), (95.056, 1.344), (100.0, 0)]
ORD_64_3_618_LOWER = [(0, 0), (0.850, -1.234), (1.141, -1.465), (1.695, -1.810), (3.018, -2.402), (5.583, -3.197),
                      (8.105, -3.768), (10.605, -4.220), (15.573, -4.899), (20.514, -5.377), (25.440, -5.695),
                      (30.355, -5.866), (35.265, -5.885), (40.173, -5.737), (45.083, -5.345), (50.000, -4.805),
                      (54.929, -4.160), (59.871, -3.444), (64.829, -2.690), (69.804, -1.922), (74.797, -1.174),
                      (79.809, -0.494), (84.839, 0.075), (89.885, 0.456), (94.944, 0.552), (100.0, 0)]
LE_RADIUS = 0.02208                 # chord, both sections
LE_SLOPE_618 = 0.253                # slope of the radius through the leading edge (64(3)-618)


# ===================================================================== access
def series(airfoil, curve, Re):
    """The recorded points of one curve: arrays x, y (increasing x, duplicates removed).
    Example: x, y = series("64-618", "cl_alpha", 6e6)"""
    pts = sorted(DATA[airfoil][curve][float(Re)])
    out = [pts[0]]
    for p in pts[1:]:
        if p[0] - out[-1][0] > 1e-9:
            out.append(p)
    a = np.array(out, float)
    return a[:, 0], a[:, 1]


def pchip(xs, ys, x):
    """Shape-preserving piecewise cubic through (xs, ys) (Fritsch and Carlson, 1980: the
    monotone cubic of SciPy's PchipInterpolator, written here in NumPy), evaluated at x.
    Example: pchip([0, 1, 2], [0, 1, 1], 0.5) -> 0.6250"""
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    x = np.asarray(x, float)
    h = np.diff(xs)
    d = np.diff(ys) / h
    n = len(xs)
    m = np.zeros(n)
    for k in range(1, n - 1):
        if d[k - 1] * d[k] > 0:
            w1, w2 = 2 * h[k] + h[k - 1], h[k] + 2 * h[k - 1]
            m[k] = (w1 + w2) / (w1 / d[k - 1] + w2 / d[k])
    def end(h0, h1, d0, d1):
        e = ((2 * h0 + h1) * d0 - h0 * d1) / (h0 + h1)
        if np.sign(e) != np.sign(d0):
            e = 0.0
        elif np.sign(d0) != np.sign(d1) and abs(e) > abs(3 * d0):
            e = 3 * d0
        return e
    if n > 2:
        m[0] = end(h[0], h[1], d[0], d[1])
        m[-1] = end(h[-1], h[-2], d[-1], d[-2])
    else:
        m[:] = d[0]
    i = np.clip(np.searchsorted(xs, x, side="right") - 1, 0, n - 2)
    t = (x - xs[i]) / h[i]
    h00, h10, h01, h11 = 2 * t**3 - 3 * t**2 + 1, t**3 - 2 * t**2 + t, -2 * t**3 + 3 * t**2, t**3 - t**2
    return h00 * ys[i] + h10 * h[i] * m[i] + h01 * ys[i + 1] + h11 * h[i] * m[i + 1]


def curve(airfoil, curve_name, Re, n=400, x=None):
    """The smooth curve through the recorded points (shape-preserving cubic, pchip()), the curve the
    chart draws. Returns (x, y). Example: a, cl = curve("64-018", "cl_alpha", 9e6)"""
    xs, ys = series(airfoil, curve_name, Re)
    if x is None:
        x = np.linspace(xs[0], xs[-1], n)
    return np.asarray(x, float), pchip(xs, ys, x)


def read(airfoil, curve_name, Re, x):
    """A value read off a curve at abscissa x (inside the recorded range), as the chart draws it.
    Example: read("64-618", "cl_alpha", 6e6, 4.0) -> 0.8889"""
    xs, _ = series(airfoil, curve_name, Re)
    if not (xs[0] <= x <= xs[-1]):
        raise ValueError(f"{x} is outside the recorded range {xs[0]} to {xs[-1]} of {airfoil} {curve_name} {Re:g}")
    return float(curve(airfoil, curve_name, Re, x=[x])[1][0])


def lift_line(airfoil, Re=6.0e6, lo=-6.0, hi=4.0):
    """Straight-line fit of the lift curve between lo and hi deg: (a0 per deg, alpha_L=0 deg).
    Example: lift_line("64-618") -> (0.1166, -3.73)"""
    a, cl = series(airfoil, "cl_alpha", Re)
    m = (a >= lo) & (a <= hi)
    k, b = np.polyfit(a[m], cl[m], 1)
    return float(k), float(-b / k)


def properties(airfoil, Re=6.0e6):
    """Section characteristics of the recorded curves at one Reynolds number: a0 (per deg),
    alpha_L0 (deg), cl_max and alpha at cl_max, cd_min and the c_l there, cm_ac (mean over
    -0.5 < c_l < 1.0), and the a.c. position of the report's table.
    Example: properties("64-618")["cl_max"] -> 1.513"""
    a0, aL0 = lift_line(airfoil, Re)
    a, cl = series(airfoil, "cl_alpha", Re)
    i = int(np.argmax(cl))
    c, cd = series(airfoil, "cd_cl", Re)
    j = int(np.argmin(cd))
    cc, cm = series(airfoil, "cmac_cl", Re)
    m = (cc > -0.5) & (cc < 1.0)
    return dict(a0=a0, alpha_L0=aL0, cl_max=float(cl[i]), alpha_cl_max=float(a[i]), cd_min=float(cd[j]),
                cl_cd_min=float(c[j]), cm_ac=float(np.mean(cm[m])), x_ac=AIRFOILS[airfoil]["ac"][float(Re)][0])


# ===================================================================== geometry
def mean_line_a1(x, cli):
    """NACA a = 1.0 mean line (uniform load), chord 1: y_c and dy_c/dx at x (0 < x < 1).
    Example: mean_line_a1(0.5, 0.6)[0] -> 0.03309"""
    x = np.clip(np.asarray(x, float), 1e-9, 1 - 1e-9)
    k = cli / (4.0 * math.pi)
    yc = -k * ((1 - x) * np.log(1 - x) + x * np.log(x))
    dyc = -k * (np.log(x) - np.log(1 - x))
    return yc, dyc


def section_outline(airfoil, chord=1.0, n=10):
    """Closed outline of the section from the report's own ordinates (trailing edge, over the top,
    round the leading edge, under the bottom), a smooth curve through every tabulated point
    (chapter_1 catmull_rom, n samples per interval), chord `chord`, leading edge at the origin.
    (The a = 1.0 mean line has an infinite slope at both ends, so the table, not the construction,
    is drawn; the unit checks show they agree.) Example: xy = section_outline("64-618")"""
    from chapter_1.geometry import catmull_rom
    if airfoil == "64-018":
        up = np.array(ORD_64_3_018, float)
        lo = up * [1.0, -1.0]
    else:
        up, lo = np.array(ORD_64_3_618_UPPER, float), np.array(ORD_64_3_618_LOWER, float)
    pts = np.r_[up[::-1], lo[1:]] / 100.0
    xy = catmull_rom(pts, n=n)
    return xy * chord


# ===================================================================== the chart in the report's layout
RE_STYLE = {3.0e6: dict(series=1, marker="o", text="3.0"), 6.0e6: dict(series=0, marker="s", text="6.0"),
            9.0e6: dict(series=2, marker="D", text="9.0")}
CHART_RANGES = {
    "report": dict(alpha=(-32.0, 32.0), cl=(-2.0, 3.6), cl_right=(-1.6, 1.6), cd=(-0.020, 0.036)),
    "data": dict(alpha=(-24.0, 28.0), cl=(-1.6, 2.0), cl_right=(-1.2, 1.6), cd=(-0.020, 0.024)),
}
CM_PER_CL = 0.25        # left panel: c_m,c/4 scale = c_l scale / 4 (0.1 of c_m per 0.4 of c_l), as the report
CMAC_PER_CD = 25.0      # right panel: c_m,ac scale = 25 x c_d scale (0.1 of c_m per 0.004 of c_d), as the report
CMAC_AXIS_GAP = 0.10    # the c_m,ac axis stands this far (axes fraction) right of the panel, clear of the curve ends


def _ticks(lo, hi, step):
    k0 = math.ceil(lo / step - 1e-9)
    k1 = math.floor(hi / step + 1e-9)
    return [round(k * step, 6) for k in range(k0, k1 + 1)]


def naca_chart(airfoil, re=REYNOLDS, ranges="data", width=6.5, height=6.3, outline=True, key=True,
               family_labels=True, markers=True, reading=None):
    """The redrawn NACA Report 824 chart of one airfoil, in the report's layout: left panel c_l
    (inner axis) and c_m,c/4 (outer axis, 1/4 of the c_l scale) against alpha; right panel c_d
    (upper part) and c_m,ac (lower part, 25 times the c_d scale) against c_l; the section outline
    above the right panel (outline=True); a key to the Reynolds-number curves in the empty lower
    right in the report, here above the left panel (key=True); the curves labeled "lift", "moment", "drag"
    (family_labels=True). Curves: 3.0 million blue dashed with circles, 6.0 million black solid
    with squares, 9.0 million vermilion dotted with diamonds; markers at the recorded test points.
    ranges: "data" (trimmed to the data, the report's scales) or "report" (the report's full axes).
    reading: a list of dicts (curve, re, x, n[, value_label]) drawn with draw_reading(). The key
    sits above the left panel, so a reading anywhere on the panels stays clear of it.
    Returns (fig, dict(left=, right=, outline=, readings=[...])). Call save_figure after any
    additions. Example: fig, ax = naca_chart("64-618", reading=[dict(curve="cl_alpha", re=6e6, x=4.0, n=1)])"""
    from chapter_1.style import (plt, line_kw, text_color, text, INK, GRAY, FS_LABEL, FS_SMALL, LW_THIN, GRID,
                                 LW_OUTLINE, PART_FILL, opaque)
    from matplotlib.patches import Polygon
    import matplotlib.ticker as mt
    R = CHART_RANGES[ranges]
    fig = plt.figure(figsize=(width, height))
    top = 0.78 if (outline or key) else 0.96
    # panel positions in inches: room on the left of each panel for its tick labels and axis
    # label, and on the left of the left panel and the right of the right panel for the moment axes
    W = width
    axL = fig.add_axes([1.55 / W, 0.10, 1.60 / W, top - 0.10])
    axR = fig.add_axes([3.95 / W, 0.10, 1.55 / W, top - 0.10])
    for ax in (axL, axR):
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_axisbelow(True)
        ax.grid(True, color=GRID, lw=0.6)
    axL.set_xlim(*R["alpha"]); axL.set_ylim(*R["cl"])
    axR.set_xlim(*R["cl_right"]); axR.set_ylim(*R["cd"])
    fmt_tick = lambda v, _: (f"{v:g}".replace("-", "\u2212") if v != 0 else "0")
    # grid lines every 4 deg and 0.2 in c_l (every 0.2 c_l and 0.002 c_d on the right), labels at
    # 16 deg, 0.4 c_l (0.8 c_l), 0.004 c_d: a chart made for reading needs a close grid
    lab = lambda step: (lambda v, _: fmt_tick(v, _) if abs(v / step - round(v / step)) < 1e-6 else "")
    axL.set_xticks(_ticks(*R["alpha"], 4.0)); axL.set_yticks(_ticks(*R["cl"], 0.2))
    axL.yaxis.set_major_formatter(mt.FuncFormatter(lab(0.4)))
    axL.xaxis.set_major_formatter(mt.FuncFormatter(lab(16.0)));
    axR.set_xticks(_ticks(*R["cl_right"], 0.2))
    axR.xaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: fmt_tick(v, _) if abs(v / 0.8 - round(v / 0.8)) < 1e-6 else ""))
    cd_ticks = _ticks(R["cd"][0], R["cd"][1], 0.002)
    axR.set_yticks(cd_ticks)
    axR.yaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: "" if v < -1e-12 or abs(v / 0.004 - round(v / 0.004)) > 1e-6
                                                   else ("0" if abs(v) < 1e-12 else f"{v:.3f}")))
    # the moment axes: outside the left panel's c_l axis (as the report) and on the right of the
    # right panel (the report puts both on the left; a 6.5 in page leaves no room for that)
    secL = axL.secondary_yaxis(-0.42, functions=(lambda y: y * CM_PER_CL, lambda y: y / CM_PER_CL))
    secL.set_yticks([v for v in _ticks(R["cl"][0] * CM_PER_CL, R["cl"][1] * CM_PER_CL, 0.1) if -0.45 < v < 0.15])
    secL.yaxis.set_major_formatter(mt.FuncFormatter(fmt_tick))
    secR = axR.secondary_yaxis(1.0 + CMAC_AXIS_GAP, functions=(lambda y: y * CMAC_PER_CD, lambda y: y / CMAC_PER_CD))
    secR.set_yticks([v for v in _ticks(R["cd"][0] * CMAC_PER_CD, 0.0, 0.1)])
    secR.yaxis.set_major_formatter(mt.FuncFormatter(fmt_tick))
    for s_ in (secL, secR):
        s_.tick_params(labelsize=FS_SMALL, width=0.9, length=4)
    # each moment axis line runs only over its own scale, not alongside the values it does not measure
    tl, tr = secL.get_yticks(), secR.get_yticks()
    secL.spines["left"].set_bounds(min(tl), max(tl))
    secR.spines["right"].set_bounds(min(tr), max(tr))
    axL.set_xlabel(r"Section angle of attack, $\alpha$, deg", fontsize=FS_LABEL)
    axR.set_xlabel(r"Section lift coefficient, $c_l$", fontsize=FS_LABEL)
    axL.set_ylabel(r"Section lift coefficient, $c_l$", fontsize=FS_LABEL)
    fig.text(0.08 / W, 0.10 + (top - 0.10) * (-0.6 - R["cl"][0]) / (R["cl"][1] - R["cl"][0]),
             r"Moment coefficient, $c_{m,c/4}$", rotation=90, ha="left", va="center", fontsize=FS_LABEL)
    axR.set_ylabel(r"Section drag coefficient, $c_d$", fontsize=FS_LABEL)
    fig.text((W - 0.08) / W, 0.10 + (top - 0.10) * (-0.010 - R["cd"][0]) / (R["cd"][1] - R["cd"][0]),
             r"Moment coefficient, $c_{m,\mathrm{ac}}$", rotation=90, ha="right", va="center", fontsize=FS_LABEL)
    # each axis label beside its own part of the scale
    span = R["cl"][1] - R["cl"][0]
    axL.yaxis.set_label_coords(-0.27, (0.6 - R["cl"][0]) / span)
    spr = R["cd"][1] - R["cd"][0]
    axR.yaxis.set_label_coords(-0.40, (0.012 - R["cd"][0]) / spr)   # clear of the 0.004 ... 0.024 labels
    out = dict(left=axL, right=axR, sec_left=secL, sec_right=secR, readings=[])
    for Re in re:
        st = RE_STYLE[float(Re)]
        kw = line_kw(st["series"], linewidth=1.6)
        mk = dict(ls="none", marker=st["marker"], ms=4.6 if st["marker"] != "D" else 4.2, mfc="white",
                  mec=kw["color"], mew=1.0)
        for name, ax, sy in (("cl_alpha", axL, 1.0), ("cm_alpha", axL, 1.0 / CM_PER_CL),
                             ("cd_cl", axR, 1.0), ("cmac_cl", axR, 1.0 / CMAC_PER_CD)):
            x, y = curve(airfoil, name, Re)
            ax.plot(x, y * sy, zorder=3, **kw)
            if markers:
                xs, ys = series(airfoil, name, Re)
                ax.plot(xs, ys * sy, zorder=3.5, **mk)
    if outline:
        axO = fig.add_axes([3.95 / W, top + 0.02, 1.55 / W, 0.96 - top - 0.02])
        axO.axis("off"); axO.set_aspect("equal")
        xy = section_outline(airfoil)
        axO.add_patch(opaque(Polygon(xy, closed=True, fc=PART_FILL, ec=INK, lw=1.4, zorder=3)))
        axO.plot([0, 1], [0, 0], color=GRAY, lw=LW_THIN, ls=(0, (4.0, 3.0)), zorder=2)
        axO.set_xlim(-0.03, 1.03); axO.set_ylim(-0.15, 0.17)
        out["outline"] = axO
        fig.text(1.55 / W, 0.975, AIRFOILS[airfoil]["name"] + " airfoil section", fontsize=FS_LABEL, va="top")
    if key:
        # the key to the Reynolds-number curves, in the band above the left panel (clear of any
        # reading): the report puts it in a table inside the right panel
        H_in = height
        y0k, y1k = (top * H_in + 0.10) / H_in, (0.975 * H_in - 0.26) / H_in
        axK = fig.add_axes([1.55 / W, y0k, 2.3 / W, y1k - y0k])
        axK.axis("off"); axK.set_xlim(0, 1); axK.set_ylim(0, 1)
        n = len(re)
        for i, Re in enumerate(re):
            st = RE_STYLE[float(Re)]
            kw = line_kw(st["series"], linewidth=1.6)
            yk = 1.0 - (i + 0.5) / n
            axK.plot([0.0, 0.16], [yk, yk], **kw)
            axK.plot([0.08], [yk], ls="none", marker=st["marker"], ms=4.6, mfc="white", mec=kw["color"], mew=1.0)
            text(axK, (0.16, yk), rf"$R = {st['text']} \times 10^6$", direction=0, dist=5, fs=FS_SMALL,
                 color=text_color(st["series"]))
        out["key"] = axK
    for r in reading or ():
        out["readings"].append(draw_reading(fig, out, airfoil, **r))
    return fig, out


def draw_reading(fig, axes, airfoil, curve, re, x, n, value_label=None, dist=6.0):
    """A numbered reading drawn on a naca_chart(): a dashed construction line from the x axis up
    (or down) to the curve of Reynolds number `re` at abscissa x, a dot on the curve, and a dashed
    line across to the panel's left axis (the outer moment axis for a moment curve), with the
    numbered disc `n` at the start on the x axis, and a small arrowhead where the line reaches
    the scale it is read on. value_label: text written at the axis end of the horizontal line (for
    example the value read). Asserts that the drawn point lies on the drawn curve. Returns dict(x,
    y (the coefficient read), point (plotted coordinates))."""
    from chapter_1.style import INK, LW_THIN, text, FS_SMALL
    from chapter_3.drawing3 import disc, data_per_pt
    from figkit import arrow, rides_on
    ax = axes["left"] if curve in ("cl_alpha", "cm_alpha") else axes["right"]
    sy = {"cl_alpha": 1.0, "cm_alpha": 1.0 / CM_PER_CL, "cd_cl": 1.0, "cmac_cl": 1.0 / CMAC_PER_CD}[curve]
    y = read(airfoil, curve, re, x)
    yp = y * sy
    x0 = ax.get_xlim()[0]
    yb = ax.get_ylim()[0]
    kx, _ = data_per_pt(ax)
    xh = x0 + 1.5 * kx                                   # the head stops 1.5 points short of the axis line
    kw = dict(color=INK, lw=LW_THIN, ls=(0, (3.0, 2.0)), zorder=5)
    ax.plot([x, x], [yb, yp], **kw)
    ln = ax.plot([xh + 6.0 * kx, x], [yp, yp], **kw)[0]
    rides_on(arrow(ax, (xh + 7.0 * kx, yp), (xh, yp), color=INK, lw=LW_THIN, head="small", zorder=5), ln)
    ax.plot([x], [yp], "o", color=INK, ms=3.6, zorder=6)
    disc(ax, (x, yb), n, above=True)
    if value_label:
        text(ax, (x0, yp), value_label, direction=0, dist=dist, fs=FS_SMALL, va="bottom", offset=(0, 2))
    xc, yc = globals()["curve"](airfoil, curve, re, x=[x])
    assert abs(yc[0] * sy - yp) < 1e-12, "the reading lies on the drawn curve"
    return dict(x=x, y=y, point=(x, yp), curve=curve, re=re, n=n)


# ===================================================================== unit checks
def _close(a, b, tol, what):
    assert abs(a - b) <= tol, f"{what}: {a!r} vs {b!r} (tolerance {tol})"


if __name__ == "__main__":
    # 1. every curve is recorded at enough points, in increasing order
    for af in DATA:
        for c in CURVES:
            for Re in REYNOLDS:
                x, y = series(af, c, Re)
                assert len(x) >= 8 and np.all(np.diff(x) > 0), (af, c, Re)
    # 2. the a = 1.0 construction rebuilds the report's 64(3)-618 ordinates from the 64(3)-018 ones
    t = np.array(ORD_64_3_018, float)[1:-1] / 100.0
    yc, dyc = mean_line_a1(t[:, 0], 0.6)
    th = np.arctan(dyc)
    U = np.array(ORD_64_3_618_UPPER, float)[1:-1] / 100.0
    L = np.array(ORD_64_3_618_LOWER, float)[1:-1] / 100.0
    assert np.max(abs(t[:, 0] - t[:, 1] * np.sin(th) - U[:, 0])) < 3e-5 and np.max(abs(yc + t[:, 1] * np.cos(th) - U[:, 1])) < 3e-5
    assert np.max(abs(t[:, 0] + t[:, 1] * np.sin(th) - L[:, 0])) < 3e-5 and np.max(abs(yc - t[:, 1] * np.cos(th) - L[:, 1])) < 3e-5
    o = section_outline("64-018")
    _close(float(o[:, 1].max()), 0.0898, 2e-4, "64(3)-018 maximum half-thickness 8.98 percent at 35 percent chord")
    # 3. the curves against the report's own statements
    for af, meta in AIRFOILS.items():
        s = meta["summary"]
        a0, aL0 = lift_line(af, 6.0e6)
        assert s["slope_band"][0] <= a0 <= s["slope_band"][1], (af, a0)
        _close(aL0, s["alpha_L0"], 0.30, f"{af} zero-lift angle against Figure 37(c)")
        for Re in REYNOLDS:
            p = properties(af, Re)
            _close(p["cl_max"], s["clmax"][Re], 0.03, f"{af} cl_max at {Re:g} against Figure 41(d)")
        # larger Reynolds number: higher cl_max, lower minimum drag
        cm = [properties(af, Re)["cl_max"] for Re in REYNOLDS]
        cd = [properties(af, Re)["cd_min"] for Re in REYNOLDS]
        assert cm[0] < cm[1] < cm[2] and cd[0] > cd[1] >= cd[2], (af, cm, cd)
    # symmetric: zero lift at zero angle, c_m,ac about zero; cambered: negative c_m,ac
    _close(lift_line("64-018")[1], 0.0, 0.2, "symmetric section: zero lift at zero angle")
    assert abs(properties("64-018")["cm_ac"]) < 0.01 and -0.11 < properties("64-618")["cm_ac"] < -0.08
    # 4. the moment curves agree with each other through the report's a.c. position:
    #    c_m,c/4 = c_m,ac - (x_ac - 0.25) c_l (lift and normal force taken alike at these angles)
    for af in AIRFOILS:
        for Re in REYNOLDS:
            xac = AIRFOILS[af]["ac"][Re][0]
            for a in (-2.0, 0.0, 2.0, 4.0):   # inside the low-drag range, where c_m,ac is constant
                cl = read(af, "cl_alpha", Re, a)
                lhs = read(af, "cm_alpha", Re, a)
                rhs = read(af, "cmac_cl", Re, cl) - (xac - 0.25) * cl
                _close(lhs, rhs, 0.012, f"{af} {Re:g} moment transfer at {a} deg")
    # 5. the bucket of the cambered section is centered near its design lift coefficient
    assert 0.3 < properties("64-618", 9.0e6)["cl_cd_min"] < 0.9 and abs(properties("64-018", 9.0e6)["cl_cd_min"]) < 0.2
    print("airfoil_data.py: all unit checks passed")
    for af in AIRFOILS:
        p = properties(af)
        print(f"  {af}: a0 {p['a0']:.4f}/deg, alpha_L0 {p['alpha_L0']:.2f} deg, cl_max {p['cl_max']:.3f}, "
              f"cd_min {p['cd_min']:.5f} at cl {p['cl_cd_min']:.2f}, cm_ac {p['cm_ac']:.4f}")
