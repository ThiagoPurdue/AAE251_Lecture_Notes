"""Published numbers that the pages of Chapter 4 print or draw, each with its source, the page, table
or figure, and the date it was read (every source opened on 2026-11-24). Values are stored as the
source prints them (with its unit) and converted to SI in code. The invented values of the worked
examples stay in the page modules; what a document states is here. A number no opened source gave
is marked UNSOURCED and is not printed until an author opens a source for it.

Sources:
  [SNR81]  NASA, Space Shuttle News Reference (1981), NTRS 19810022734: p. 2-4 (the summary of the main
           engine), p. 2-18 ("Statistics for each booster").
  [HAER]   NASA, Historic American Engineering Record TX-116, Part III, Space Shuttle Main Engine,
           pp. 248 and 274 (throat and exit diameters).
  [FS-F1]  NASA, Saturn V News Reference, "F-1 Engine Fact Sheet", sheet R-1 (1968; NASA image MSFC-9264931).
  [FS-J2]  NASA, Saturn V News Reference, "J-2 Engine Fact Sheet", sheet R-16 (1968; NASA image 9264930).
  [SA503]  NASA MSFC, Saturn V Flight Manual SA-503, MSFC-MAN-503 (1968), NTRS 19750063889, Figure 1-3, p. 1-6.
  [BIGGS]  Biggs, R. E., "Rocketdyne F-1 Saturn V First Stage Engine", in Remembering the Giants (NASA
           SP-2009-4545, 2009), NTRS 20100027316, pp. 19 and 20.
  [SP4029] Orloff, R. W., Apollo by the Numbers, NASA SP-2000-4029: "Ground Ignition Weights" and
           "Launch Vehicle Propellant Usage", Apollo 11 column.
  [FER506] NASA MSFC, Saturn V Launch Vehicle Flight Evaluation Report AS-506, Apollo 11, MPR-SAT-FE-69-9
           (1969): Table 4-2, p. 4-8 (space-fixed velocity at cutoff); Table 5-1, p. 5-5 (F-1 specific
           impulse); p. 6-4 (S-II stage specific impulse); Table 7-1 (S-IVB).
  [A5UM]   Arianespace, Ariane 5 User's Manual, Issue 5 Revision 2 (2016): p. 1-7 (stage data); p. 2-9,
           Section 2.4.5 (Ariane 5 ES performance to the orbit of the International Space Station).
  [ESA123] Berkes, R., "The Ariane-5 ECA Heavy-Lift Launcher", ESA Bulletin 123 (2005), pp. 17 and 18.
  [VEGAUM] Arianespace, Vega User's Manual, Issue 4 (2014), Figure 1.5.1a, p. 1-6.
  [VEGACUM] Arianespace, Vega C User's Manual, Issue 0 Revision 0 (2018): Figure 1.4.1.a, p. 1-6; Table
           2.4.2.a, p. 2-10.  ESA, "Vega-C" web page (liftoff mass).
  [ELECTRON] Rocket Lab, Payload User's Guide, Version 7.0 (2022), pp. 11 to 13.
  [ISRO]   ISRO web pages "PSLV" and "LVM3"; ISRO, LVM3-M5 brochure (2025), p. 2.
  [ESA-A5ES] ESA, "Ariane 5 ES" web page (liftoff mass of Ariane 5 ES Galileo).
  [ESA-EAP] ESA, "Ariane 5 boosters (EAP)" web page (share of the liftoff thrust; thrust and specific impulse).
  [F9UG]   SpaceX, Falcon User's Guide (2025), pp. 6 to 9, Table 2-1.  [SPX2019] spacex.com Falcon 9 and
           Falcon Heavy pages as archived on 2019-12-15 (payload to low Earth orbit, mass, thrust).
  [ESA-STS] ESA, "Shuttle technical facts" web page.
  [SLSRG]  NASA, Space Launch System Reference Guide, Version 2 (2022), p. 8.
  [SP4206] Bilstein, R., Stages to Saturn, NASA SP-4206, p. 5.  [AS505] NASA MSFC, Technical Information
           Summary, Apollo-10 (AS-505) (1969), NTRS 19700015780, Figure 18, p. 33.
  [LPS]    McConnaughey, P. K., et al., "NASA's Launch Propulsion Systems Technology Roadmap", NTRS
           20120014957, Section 1, p. 2 (launch-vehicle classes by payload).
  [SP125]  Huzel and Huang, NASA SP-125 (1967, the edition opened): Tables 1-4 and 1-5 (propellant properties), pp. 22 to 24;
           Table 1-6 (monopropellants), p. 25; Tables 1-8 to 1-10 (theoretical performance), pp. 26 and 27,
           and the notes to them, p. 27.
  [NACA-CH4] Gordon, S., and Kastner, M. E., NACA RM E58B20 (1958): Table I, p. 11 (methane properties);
           Table II, p. 12 and Table VI, p. 27 (oxygen and methane, frozen composition).
  [SP8064] NASA SP-8064, Solid Propellant Selection and Characterization (1971), Table I, p. 8.
  [NIST]   NIST Chemistry WebBook, SRD 69, thermophysical properties of fluid systems, saturation at
           0.101325 MPa (oxygen C7782447, parahydrogen B5000001, methane C74828); the hydrogen values are
           parahydrogen's, and normal hydrogen's (C1333740, NIST_NORMAL_H2) differ by less than 1 percent.
  [PLACHTA] Plachta, D. W., Johnson, W. L., and Feller, J. R., "Cryogenic Boil-Off Reduction System
           Testing", AIAA Joint Propulsion Conference (2014), NTRS 20150000134, abstract: liquid oxygen
           "zero boil-off storage", liquid hydrogen "boil-off was reduced 60% by the cryocooler system
           operating at 90K".
  [SOA]    NASA Small Spacecraft Systems Virtual Institute, State-of-the-Art of Small Spacecraft
           Technology, Chapter 4, In-Space Propulsion, Table 4-1 (web page updated 2026).
  [JOHNSON] Johnson, L., et al., "Technology Area Roadmap for In-Space Propulsion Technologies", GLEX-2012,
           NTRS 20120015032, p. 4, Section 3.3 (nuclear thermal).  [TA02] NASA In-Space Propulsion
           roadmap (2010), NTRS 20110005503, p. 9 (ion and Hall thrusters).

Run this file for its unit checks:  python3 -B scripts/chapter_4/published.py
"""
import math
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from chapter_1.constants import LB_N, LB_KG, FT  # noqa: E402
from chapter_1.atmosphere import P_SL  # noqa: E402

IN = 0.0254                 # m per inch
PSI = 6894.757              # Pa per psi (NIST SP 811)


def f_to_k(deg_f):
    """Kelvin from degrees Fahrenheit. Example: f_to_k(-297.4) -> 90.15"""
    return (deg_f - 32.0) * 5.0 / 9.0 + 273.15


# ===================================================================== engines
# Each engine: what the source prints (with its unit) and SI values. "checked": the sea-level and vacuum
# thrusts give an exit area, (F_vac - F_sl)/p_a, that agrees with the published exit diameter.
RS25 = dict(                    # Space Shuttle Main Engine at rated (100 percent) power, [SNR81] p. 2-4
    name="RS-25 (Space Shuttle Main Engine)",
    F_sl_lbf=375000.0, F_vac_lbf=470000.0,          # "Sea level: 1670 kilonewtons (375 000 pounds) Vacuum: 2100 kilonewtons (470 000 pounds)"
    isp_sl=363.2, isp_vac=455.2,                     # s ("363.2 lbf/s/lbm", "455.2 lbf/s/lbm")
    area_ratio=77.5,                                 # "Nozzle exit to throat area 77.5 to 1"
    pc_psia=2970.0,                                  # "20 480 kN/m2 (2970 psia)"
    mass_kg=3000.0,                                  # "Approximately 3000 kilograms (6700 pounds)"
    exit_d_in=90.7, throat_d_in=10.3,                # [HAER] p. 274: "10.3" in diameter at the throat, and 90.7" at the nozzle exit"
    propellants="liquid oxygen and liquid hydrogen",
    source="SNR81, p. 2-4; HAER, p. 274",
)
F1 = dict(                      # [FS-F1] unless marked
    name="F-1",
    F_sl_lbf=1522000.0,          # "THRUST (sea level) 1,500,000 lb", "uprated to 1,522,000 lb. thrust for Vehicle 504 and
                                 # all subsequent"; [SA503] Figure 1-3: 1,522,000 each
    F_vac_lbf=None,              # UNSOURCED: no NASA source opened gives the F-1's vacuum thrust
    isp_sl=265.0,                # [BIGGS] p. 20: "The specific impulse ... was 265 seconds" ([FS-F1]: 260 s minimum)
    isp_vac=None,                # UNSOURCED
    area_ratio=16.0,             # "EXPANSION AREA RATIO 16:1 with nozzle extension"
    pc_psia=965.0,               # "CHAMBER PRESSURE 965 psia" ([BIGGS]: "designed at 1,100 psi")
    exit_d_ft_in=(11, 7),        # "MAXIMUM NOZZLE EXIT DIAMETER 11 ft. 7 in."
    mass_lb=18500.0,             # "WEIGHT FLIGHT CONFIGURATION 18,500 lb. maximum"
    mixture_ratio=2.27,          # "MIXTURE RATIO 2.27:1"
    propellants="liquid oxygen and kerosene (RP-1)",
    source="NASA F-1 Engine Fact Sheet (Saturn V News Reference); Biggs (2009)",
)
J2 = dict(                      # [FS-J2]
    name="J-2",
    F_vac_lbf=225000.0,          # "THRUST (altitude) 225,000 lb."
    isp_vac=424.0,               # "SPECIFIC IMPULSE 424 sec."
    area_ratio=27.5,             # "EXPANSION AREA RATIO 27.5:1"
    pc_psia=763.0,               # "CHAMBER PRESSURE (Pc) 763 psia"
    exit_d_ft_in=(6, 5),         # "NOZZLE EXIT DIAMETER 6 ft. 5 in."
    mass_lb=3480.0,              # "WEIGHT, DRY, FLIGHT CONFIGURATION 3,480 lb."
    mixture_ratio=5.5,
    propellants="liquid oxygen and liquid hydrogen",
    source="NASA J-2 Engine Fact Sheet (Saturn V News Reference)",
)
VULCAIN2 = dict(                # [A5UM] p. 1-7, main stage (EPC)
    name="Vulcain 2",
    F_sl_kN=960.0, F_vac_kN=1390.0,      # "Thrust 960 kN (SL) 1390 kN (Vacuum)" ([ESA123]: 1350 kN)
    isp_sl=310.0, isp_vac=432.0,         # "Isp ~310 s (SL) 432 s (Vacuum)"
    area_ratio=58.2,                     # chapter_1.launchers.ARIANE5 (AIAA vehicle guide), as page 1.3 draws it
    propellants="liquid oxygen and liquid hydrogen",
    source="Ariane 5 User's Manual (2016), p. 1-7",
)


def _ft_in(ft, inch):
    return ft * FT + inch * IN


def engine_si(E):
    """SI values of an engine dict: F_sl, F_vac (N), isp_sl, isp_vac (s), area_ratio, pc (Pa), exit_d,
    throat_d (m), mass (kg); None where the source gives nothing. Example: engine_si(RS25)["F_vac"] -> 2,090,664"""
    out = dict(name=E["name"], area_ratio=E.get("area_ratio"), isp_sl=E.get("isp_sl"), isp_vac=E.get("isp_vac"),
               propellants=E.get("propellants"), source=E.get("source"))
    if "F_sl_lbf" in E or "F_vac_lbf" in E:
        out["F_sl"] = E["F_sl_lbf"] * LB_N if E.get("F_sl_lbf") else None
        out["F_vac"] = E["F_vac_lbf"] * LB_N if E.get("F_vac_lbf") else None
    else:
        out["F_sl"] = E["F_sl_kN"] * 1e3 if E.get("F_sl_kN") else None
        out["F_vac"] = E["F_vac_kN"] * 1e3 if E.get("F_vac_kN") else None
    out["pc"] = E["pc_psia"] * PSI if E.get("pc_psia") else None
    if "exit_d_in" in E:
        out["exit_d"] = E["exit_d_in"] * IN
    elif "exit_d_ft_in" in E:
        out["exit_d"] = _ft_in(*E["exit_d_ft_in"])
    else:
        out["exit_d"] = None
    if "throat_d_in" in E:
        out["throat_d"] = E["throat_d_in"] * IN
    elif out["exit_d"] and out["area_ratio"]:
        out["throat_d"] = out["exit_d"] / math.sqrt(out["area_ratio"])      # from the published ratio
    else:
        out["throat_d"] = None
    out["mass"] = E.get("mass_kg") or (E["mass_lb"] * LB_KG if E.get("mass_lb") else None)
    return out


def engine_check(E, p_a=P_SL):
    """The consistency check of a sea-level engine: the exit diameter that (F_vac - F_sl)/p_a gives against
    the published one. Returns (computed, published, relative difference), or None when the source lacks
    a vacuum thrust or an exit diameter. Example: engine_check(RS25) -> (2.304, 2.304, 0.0003)"""
    s = engine_si(E)
    if not (s.get("F_sl") and s.get("F_vac") and s.get("exit_d")):
        return None
    d = math.sqrt(4.0 * (s["F_vac"] - s["F_sl"]) / p_a / math.pi)
    return d, s["exit_d"], (d - s["exit_d"]) / s["exit_d"]


ENGINES = {"RS-25": RS25, "F-1": F1, "J-2": J2, "Vulcain 2": VULCAIN2}

# ===================================================================== stages (inert mass fractions, Saturn V)
# Saturn V, Apollo 11 (AS-506), [SP4029] "Ground Ignition Weights", lbm: dry, oxidizer, fuel, other.
SATURN_V_AS506 = {
    "S-IC":  dict(dry_lb=287531.0, ox_lb=3305786.0, fuel_lb=1424889.0, other_lb=5442.0,
                  isp=265.0,            # [FER506] Table 5-1: 263.5 to 265.0 s per engine, reduced to sea level
                  isp_kind="sea level, per engine (263.5 to 265.0 s)",
                  burn_s=168.03,        # [SP4029] propellant usage: -6.4 s to 161.63 s
                  v_cutoff=2764.1,      # [FER506] Table 4-2, space-fixed, m/s
                  engines="five F-1", propellants="liquid oxygen and kerosene (RP-1)"),
    "S-II":  dict(dry_lb=79714.0, ox_lb=819050.0, fuel_lb=158116.0, other_lb=1260.0,
                  isp=423.2, isp_kind="stage, vacuum ([FER506] p. 6-4)", burn_s=384.22, v_cutoff=6916.1,
                  engines="five J-2", propellants="liquid oxygen and liquid hydrogen"),
    "S-IVB": dict(dry_lb=24852.0, ox_lb=192497.0, fuel_lb=43608.0, other_lb=1656.0,
                  isp=428.7, isp_kind="stage, vacuum ([FER506] Table 7-1)", burn_s=147.13 + 346.83,
                  burn_parts_s=(147.13, 346.83), v_cutoff=7791.2,     # first cutoff (Earth parking orbit)
                  engines="one J-2", propellants="liquid oxygen and liquid hydrogen"),
}
SATURN_V_AS506_INTERSTAGES_LB = {"S-IC/S-II": 11477.0, "S-II/S-IVB": 8076.0}     # [SP4029]
SATURN_V_AS506_TOTAL_LB = 6477875.0                                                # [SP4029] total vehicle at ignition


def saturn_stage_kg(name):
    """Dry and propellant mass (kg) of a Saturn V stage of Apollo 11 (propellant = oxidizer + fuel).
    Example: saturn_stage_kg("S-II") -> (36,158, 443,235)"""
    s = SATURN_V_AS506[name]
    return s["dry_lb"] * LB_KG, (s["ox_lb"] + s["fuel_lb"]) * LB_KG


# Real stages with published dry and propellant masses: (name, vehicle, kind, dry kg, propellant kg, source).
# "dry" is the source's dry, empty or inert mass; where the source prints only the gross mass, dry is gross
# minus propellant and the note says so.
STAGES = [
    ("S-IC", "Saturn V", "liquid, first stage", *saturn_stage_kg("S-IC"), "SP-2000-4029, Apollo 11"),
    ("S-II", "Saturn V", "liquid, second stage", *saturn_stage_kg("S-II"), "SP-2000-4029, Apollo 11"),
    ("S-IVB", "Saturn V", "liquid, upper stage", *saturn_stage_kg("S-IVB"), "SP-2000-4029, Apollo 11"),
    ("EPC", "Ariane 5", "liquid, core stage", 14700.0, 170000.0, "Ariane 5 User's Manual, p. 1-7 (as page 1.3)"),
    ("ESC-A", "Ariane 5", "liquid, upper stage", 4540.0, 14900.0, "Ariane 5 User's Manual, p. 1-7"),
    ("EAP", "Ariane 5", "solid booster", 280000.0 - 240000.0, 240000.0,
     "ESA Bulletin 123, p. 17: 280 t including 240 t of propellant (dry = the difference)"),
    ("Shuttle SRB", "Space Shuttle", "solid booster", 87550.0, 502125.0, "Space Shuttle News Reference, p. 2-18"),
    ("P80", "Vega", "solid, first stage", 96243.0 - 87710.0, 87710.0, "Vega User's Manual, p. 1-6 (gross 96,243 kg)"),
    ("Zefiro 23", "Vega", "solid, second stage", 26300.0 - 23814.0, 23814.0, "Vega User's Manual, p. 1-6 (gross 26,300 kg)"),
    ("Zefiro 9", "Vega", "solid, third stage", 12000.0 - 10567.0, 10567.0, "Vega User's Manual, p. 1-6 (gross 12,000 kg)"),
    ("AVUM", "Vega", "liquid, small upper stage (carries the launcher's avionics)", 688.0, 381.0 + 196.0,
     "Vega User's Manual, p. 1-6"),
]
STAGE_ISP_VAC = {"P80": 280.0, "Zefiro 23": 287.5, "Zefiro 9": 295.9, "AVUM": 314.6,     # [VEGAUM] p. 1-6
                 "ESC-A": 446.0, "EAP": 274.5}                                            # [A5UM] p. 1-7

# ===================================================================== launch vehicles
# name, payload to low Earth orbit (kg), the orbit it is quoted for, liftoff mass (kg), liftoff thrust (as
# printed), stages, boosters, propellants, source. Payload values exactly as the source prints them.
LAUNCH_VEHICLES = [
    dict(name="Electron", payload=200.0, orbit="500 km sun-synchronous orbit", liftoff=13000.0,
         thrust="9 engines of 5,600 lbf (24 kN) each at sea level", stages="2 and a kick stage", boosters="none",
         propellants="liquid oxygen and kerosene", source="Rocket Lab Payload User's Guide 7.0, p. 12"),
    dict(name="PSLV-XL", payload=1750.0, orbit="600 km sun-synchronous polar orbit", liftoff=320000.0,
         thrust=None, stages="4", boosters="6 solid strap-ons",
         propellants="solid; UDMH and nitrogen tetroxide; solid; MMH and MON", source="ISRO, PSLV page"),
    dict(name="Vega C", payload=2250.0, orbit="500 km, 88 deg", liftoff=210000.0,
         thrust="P120C, 4,323 kN maximum in vacuum", stages="3 solid and the AVUM+ upper stage", boosters="none",
         propellants="solid; NTO and UDMH (AVUM+)", source="Vega C User's Manual, Table 2.4.2.a; ESA, Vega-C page"),
    dict(name="LVM3", payload=8000.0, orbit="600 km", liftoff=640000.0, thrust=None, stages="3",
         boosters="2 solid (S200)", propellants="solid; UH25 and nitrogen tetroxide; liquid oxygen and hydrogen",
         source="ISRO, LVM3 page; LVM3-M5 brochure, p. 2"),
    dict(name="Ariane 5 ES", payload=19000.0, payload_hi=21000.0,
         orbit="International Space Station orbit, 200 to 400 km, 51.6 deg", liftoff=760000.0,
         thrust="Vulcain 2, 960 kN at sea level; two boosters, 7,000 kN each in vacuum", stages="core and upper stage",
         boosters="2 solid (EAP)", propellants="liquid oxygen and hydrogen; MMH and nitrogen tetroxide; solid",
         source="Ariane 5 User's Manual, p. 2-9 and p. 1-7; ESA, Ariane 5 ES page"),
    dict(name="Falcon 9", payload=22800.0, orbit="not stated", liftoff=549054.0, thrust="7,607 kN at sea level",
         stages="2", boosters="none", propellants="liquid oxygen and kerosene",
         source="spacex.com (archived 2019); Falcon User's Guide (2025), Table 2-1: 7,686 kN"),
    dict(name="Space Shuttle", payload=24310.0, orbit="low Earth orbit (operational 190 to 960 km)",
         liftoff=2000000.0, thrust="30.16 MN", stages="orbiter with external tank", boosters="2 solid",
         propellants="liquid oxygen and hydrogen; solid", source="ESA, Shuttle technical facts"),
    dict(name="Falcon Heavy", payload=63800.0, orbit="not stated", liftoff=1420788.0, thrust="22,819 kN at sea level",
         stages="2", boosters="2 (Falcon 9 first stages)", propellants="liquid oxygen and kerosene",
         source="spacex.com (archived 2019); Falcon User's Guide (2025), p. 7"),
    dict(name="SLS Block 1", payload=95000.0, orbit="not stated", liftoff=2603000.0, thrust="36,786 kN at launch",
         stages="core stage and ICPS", boosters="2 solid", propellants="liquid oxygen and hydrogen; solid (PBAN)",
         source="NASA SLS Reference Guide (2022), p. 8"),
    dict(name="Saturn V", payload=113400.0, orbit="190 km", liftoff=6407000.0 * LB_KG,
         thrust="33,360,000 N (7,500,000 lb, before the F-1 uprate; LIFTOFF_THRUST uses 5 x 1,522,000 lbf)",
         stages="3", boosters="none",
         propellants="liquid oxygen and kerosene; liquid oxygen and hydrogen (two stages)",
         source="SP-4206, p. 5 (payload, thrust); AS-505 Technical Information Summary, Figure 18 (liftoff mass)",
         note="SP-4206 does not say whether the 113,400 kg includes the S-IVB stage"),
]
# [LPS] p. 2: "Small: 0-2 t payloads; Medium: 2-20 t; Heavy: 20-50 t; Super Heavy: > 50 t" (to low Earth orbit)
LV_CLASSES = [("small", 0.0, 2000.0), ("medium", 2000.0, 20000.0), ("heavy", 20000.0, 50000.0),
              ("super heavy", 50000.0, float("inf"))]


def lv_class(payload_kg):
    """The class of a launch vehicle from its payload to low Earth orbit, by [LPS]. Example: lv_class(22800.0) -> "heavy" """
    for name, lo, hi in LV_CLASSES:
        if lo <= payload_kg < hi:
            return name
    raise ValueError(payload_kg)


# ===================================================================== propellants
# Theoretical performance, [SP125] Tables 1-8 to 1-10 (notes p. 27): chamber 1000 psia, expanded to
# 14.7 psia (optimum at sea level), shifting equilibrium, infinite contraction ratio. Columns as printed:
# mixture ratio by weight, bulk density g/cc, Tc deg F, molecular weight, c* ft/s, C_f, I_s s.
# [NACA-CH4]: oxygen and methane, FROZEN composition, chamber 600 psia, expanded to 1 atm (other conditions:
# say so wherever it is printed beside the SP-125 rows); Tc in K; no bulk density (computed from NIST densities).
PROPELLANTS = {
    "LOX/LH2":  dict(name="liquid oxygen and liquid hydrogen", r=4.02, d=0.28, Tc_F=4935.0, M=10.0, cstar_fps=7980.0,
                     Cf=1.578, Is=391.0, source="SP-125, Table 1-10, p. 27", kind="cryogenic"),
    "LOX/RP-1": dict(name="liquid oxygen and kerosene (RP-1)", r=2.56, d=1.02, Tc_F=6150.0, M=23.3, cstar_fps=5920.0,
                     Cf=1.632, Is=300.0, source="SP-125, Table 1-9, p. 27", kind="cryogenic oxidizer, storable fuel"),
    "NTO/MMH":  dict(name="nitrogen tetroxide and monomethylhydrazine (MMH)", r=2.16, d=1.20, Tc_F=5635.0, M=None,
                     cstar_fps=5720.0, Cf=1.621, Is=288.0, source="SP-125, Table 1-8, p. 26 (molecular weight blank)",
                     kind="storable, hypergolic"),
    "NTO/A-50": dict(name="nitrogen tetroxide and Aerozine 50 (50% UDMH, 50% hydrazine)", r=2.00, d=1.21, Tc_F=5590.0,
                     M=22.6, cstar_fps=5725.0, Cf=1.620, Is=288.0, source="SP-125, Table 1-8, p. 26",
                     kind="storable, hypergolic"),
    "LOX/CH4":  dict(name="liquid oxygen and liquid methane", r=2.660, d=None, Tc_K=3272.0, M=19.08, cstar_fps=6011.0,
                     Cf=1.514, Is=282.8, source="NACA RM E58B20, Tables II and VI (frozen, 600 psia)",
                     kind="cryogenic", frozen=True, pc_psia=600.0),
}
HYDRAZINE_MONO = dict(Is=205.0, source="SP-125, Table 1-6, p. 25: theoretical, 300 psia, sea-level optimum expansion, "
                                       "frozen composition")
SOLID_AP_AL = dict(name="ammonium perchlorate, aluminum and HTPB binder", Is=(260.0, 265.0), Tc_F=(5600.0, 5800.0),
                   density_lb_in3=0.064, metal_pct=(4.0, 17.0),
                   source="SP-8064, Table I, p. 8: theoretical at 1000 psia exhausting to 14.7 psia")
IN3_M3 = IN ** 3

# NIST WebBook, saturation at 0.101325 MPa: normal boiling point K, saturated liquid density kg/m^3, heat of
# vaporization kJ/kg (vapor minus liquid enthalpy)
NIST = {"oxygen": dict(Tb=90.1878, rho=1141.17, h_vap=213.06),
        "hydrogen": dict(Tb=20.2713, rho=70.8281, h_vap=446.065, form="parahydrogen"),
        "methane": dict(Tb=111.667, rho=422.356, h_vap=510.83)}
# NIST WebBook, normal hydrogen (C1333740), saturation at 0.101325 MPa, interpolated between the table's rows at
# 0.100850 and 0.101807 MPa (read 2026-11-24): the same quantities, to compare with parahydrogen's
NIST_NORMAL_H2 = dict(Tb=20.369, rho=70.848, h_vap=448.71)
# [PLACHTA] abstract: the liquid hydrogen boil-off cut by a 90 K cryocooler in a NASA test (fraction)
PLACHTA_LH2_CUT = 0.60
# [SP125] Table 1-4 (storable, density at 68 deg F) and Table 1-5 (cryogenic, density at the boiling point):
# freezing point deg F, boiling point deg F, density g/cc
SP125_PROPERTIES = {
    "hydrazine": (34.5, 235.4, 1.01), "MMH": (-63.0, 187.0, 0.878), "UDMH": (-72.0, 146.0, 0.789),
    "nitrogen tetroxide": (11.0, 70.0, 1.44), "RP-1": ((-64.0, -47.0), (342.0, 507.0), (0.80, 0.82)),
    "liquid oxygen": (-362.0, -297.4, 1.142), "liquid hydrogen": (-434.6, -422.9, 0.071),
}


def propellant_si(key):
    """SI values of a propellant pair: r, rho_bulk (kg/m^3; None when the source gives none), Tc (K),
    M (kg/kmol), cstar (m/s), Cf, isp (s), source. Example: propellant_si("LOX/RP-1")["cstar"] -> 1,804"""
    P = PROPELLANTS[key]
    Tc = P["Tc_K"] if "Tc_K" in P else f_to_k(P["Tc_F"])
    return dict(name=P["name"], r=P["r"], rho_bulk=P["d"] * 1000.0 if P["d"] else None, Tc=Tc, M=P["M"],
                cstar=P["cstar_fps"] * FT, Cf=P["Cf"], isp=P["Is"], source=P["source"], kind=P["kind"],
                frozen=P.get("frozen", False))


def bulk_density(r, rho_ox, rho_fuel):
    """Bulk density (kg/m^3) of a propellant pair at mixture ratio r (oxidizer over fuel mass):
    (1 + r) / (r / rho_ox + 1 / rho_fuel). Example: bulk_density(2.66, 1141.17, 422.356) -> 778.9"""
    return (1.0 + r) / (r / rho_ox + 1.0 / rho_fuel)


# ===================================================================== kinds of propulsion
# No open source opened gives one table for all kinds (Sutton and Biblarz, Table 2-1, is the model but
# was not opened). Each range below names its own source; "small" ranges are for small-spacecraft
# devices only ([SOA] says so), "large" ranges come from the engines and motors recorded above.
# (kind, I_sp low s, I_sp high s, thrust low N, thrust high N, source)
PROPULSION_KINDS = [
    ("cold gas", 40.0, 110.0, 10e-6, 3.6, "SOA Table 4-1"),
    ("monopropellant", 180.0, 285.0, 0.25, 28.0, "SOA Table 4-1 (hydrazine; small devices)"),
    ("bipropellant", 288.0, 455.2, 50e-3, 1522000.0 * LB_N,
     "SOA Table 4-1 (small, 50 mN); SP-125 Table 1-8 (288 s); RS-25 455.2 s and F-1 1,522,000 lbf"),
    ("solid", 187.0, 295.9, 37.0, 11790e3, "SOA Table 4-1 (small); Vega User's Manual (Zefiro 9, 295.9 s); "
                                            "Shuttle SRB, 11,790 kN (Space Shuttle News Reference, p. 2-18)"),
    ("hybrid", 215.0, 300.0, 8.0, 222.0, "SOA Table 4-1 (small devices only; large hybrids UNSOURCED)"),
    ("nuclear thermal", 800.0, 900.0, 7500.0 * LB_N, 250000.0 * LB_N, "Johnson et al. (2012), Section 3.3 (NERVA)"),
    ("electric", 200.0, 10000.0, 0.1e-3, 55e-3, "SOA Table 4-1 (gridded ion, Hall, small); TA02 (2010), p. 9 "
                                                 "(ion to over 10,000 s)"),
]


# ===================================================================== data first printed on one page
# Moved from the page modules, each with the source it was read from (opened 2026-11-24).
# --- page 4.3: the Saturn V of Apollo 11
# The launch escape tower, dropped early in the second-stage burn: "Total Launch Escape System", Apollo 11
# column of the ground ignition weights (Orloff, Apollo by the Numbers, SP-2000-4029), lb.
SATURN_V_AS506_LES_LB = 8910.0
# Space-fixed velocity at the end of the S-IVB's second burn (translunar injection), m/s:
# AS-506 flight evaluation report, Table 4-2, p. 4-8 ("S-IVB 2nd guidance cutoff signal", actual).
SATURN_V_AS506_TLI_V = 10841.0
# --- page 4.4: propellant selection
# Vega User's Manual, Issue 4 (2014), p. 1-6: AVUM upper stage, "381 kg/196 kg of NTO/UDMH", "Regulated
# pressure-fed", "2.45 kN - Vacuum", "314.6 s - Vacuum"; p. 2-5: "a restartable upper stage (up to 5 times)".
# Zefiro 9 third stage: "317 kN - Max Vac thrust", "295.9 s - Vac"; P80: "3015 kN Max Vac thrust", "280 s - Vac".
AVUM_NTO_KG, AVUM_UDMH_KG = 381.0, 196.0
AVUM_F_VAC = 2.45e3
Z9_F_VAC, P80_F_VAC = 317e3, 3015e3
# SP-125 Table 1-8, p. 26: nitrogen tetroxide and UDMH: r_w 2.61, d 1.18 g/cc, Tc 5685 deg F, M 23.6, I_s 285 s
NTO_UDMH = dict(r=2.61, d=1.18, Tc_F=5685.0, M=23.6, Is=285.0)
# SP-125 Table 1-6, p. 25: hydrazine, density impulse 207 lb-sec/... with density 1.01 (Table 1-4) and I_s 205
# (300 psia, sea-level optimum, frozen); Table 1-4, p. 22: densities at 68 deg F (SP125_PROPERTIES).
# Ariane 5 User's Manual (2016), p. 1-7: ESC-A "Thrust 67 kN", "Isp 446 s", dry 4540 kg, 14.9 t propellant;
# EAP "Mean thrust 7000 kN (Vacuum)", "Isp 274.5 s".
ESCA_F, EAP_F = 67e3, 7000e3
# Section 2.4.1, p. 2-3: the standard geostationary transfer orbit: i = 6 deg, perigee 250 km, apogee 35,786 km
# at first apogee.
GTO_HP, GTO_HA, GTO_INC = 250.0, 35786.0, 6.0
# Space Shuttle News Reference (1981), p. 2-18: each solid booster, "THRUST AT LIFT-OFF 11 790 kilonewtons".
SRB_F = 11790e3
# Liftoff thrust in N. Falcon 9 and SLS Block 1 as LAUNCH_VEHICLES gives them. Saturn V: five F-1 engines at the
# uprated sea-level thrust of [FS-F1] (1,522,000 lbf each, "Vehicle 504 and all subsequent"; the liftoff mass is
# that of AS-505), not SP-4206's 7,500,000 lb, the rating before the uprate. Space Shuttle: two boosters at
# liftoff ([SNR81] p. 2-18) and three RS-25 at rated power at sea level ([SNR81] p. 2-4), so the row agrees with
# the booster and engine values the chapter prints (ESA's 30.16 MN counts 12.5 MN for each booster).
LIFTOFF_THRUST = {"Saturn V": 5 * F1["F_sl_lbf"] * LB_N, "Falcon 9": 7607e3, "SLS Block 1": 36786e3,
                  "Space Shuttle": 2 * SRB_F + 3 * RS25["F_sl_lbf"] * LB_N}
# ESA, "Ariane 5 boosters (EAP)" web page (opened 2026-11-24): "Ariane 5 boosters provided 1100 tonnes of
# thrust, roughly 92% of the total thrust at liftoff." The manual's "Mean thrust 7000 kN (Vacuum)" above cannot
# be a mean (about 240 t of propellant at 274.5 s over about 130 s gives near 5,000 kN), and no opened source
# calls it a peak, so page 4.4 does not draw it. The same ESA page, on the motor: "Specific impulse was 262 sec.,
# maximum pressure 64 bar and thrust 5400 kN." It does not say where the 5,400 kN applies, but it agrees with the
# 1,100 tonnes of thrust of the two boosters at liftoff (550 t times g0 is 5,396 kN, asserted below), so page 4.4
# draws the booster at liftoff with ESA's pair, 5,400 kN and 262 s.
EAP_LIFTOFF_SHARE_PCT = 92.0
EAP_LIFTOFF_F, EAP_LIFTOFF_ISP = 5400e3, 262.0
EAP_LIFTOFF_PAIR_T = 1100.0
assert abs(EAP_LIFTOFF_PAIR_T / 2 * 1e3 * 9.81 / EAP_LIFTOFF_F - 1.0) < 0.002
# NASA SOA, State of the Art of Small Spacecraft Technology, Chapter 4, Table 4-1 (small-spacecraft devices only):
SOA = {"cold gas": (40.0, 110.0, 10e-6, 3.6), "hydrazine monopropellant": (180.0, 285.0, 0.25, 28.0),
       "hybrid": (215.0, 300.0, 8.0, 222.0), "gridded ion": (500.0, 3000.0, 0.1e-3, 20e-3),
       "Hall-effect": (200.0, 1920.0, 0.25e-3, 55e-3)}
SOA_MN_PER_KW, SOA_500W_MN = 75.0, 38.0          # "below 75 mN/kW ... 500 W ... no more than 38 mN"
# Meyer et al. (2012), NASA/TM-2012-217641, p. 7: NERVA "7,500 to 250,000 lbf of thrust with specific impulses
# of 800 to 900 seconds"; Meyer et al. (2010) roadmap TA02, p. 9: ion thrusters "2000 to over 10,000 sec".
NERVA = (800.0, 900.0, 7500.0 * LB_N, 250000.0 * LB_N)
ION_MAX = 10000.0
# SP-125 p. 18: cryogenic propellants boil below -230 deg F at ambient pressure; p. 21: test results usually
# 5 to 12 percent below the theoretical values.
CRYO_LIMIT_F = -230.0
TEST_LOW_PCT = (5.0, 12.0)
ROOM_F = 68.0                                    # the temperature of SP-125 Table 1-4's densities
# --- page "Engines and tanks": [SNR81] pp. 2-4, 2-5 and 2-34; [SP125] Sections 2.1, 8.1 and 8.2,
# Table 1-4, Sample Calculations 8-1 and 8-2
SHUTTLE_ET_PROP_KG = 719112.0            # SNR81 p. 2-34, "Total: 719 112 kilograms"
SHUTTLE_ET_LOX_KG = 616493.0             # SNR81 p. 2-34
SHUTTLE_ET_LH2_KG = 102618.0             # SNR81 p. 2-34
SHUTTLE_MAIN_ENGINES = 3                 # SNR81 p. 2-5, "A cluster of three Space Shuttle Main Engines"
SHUTTLE_BURN_MIN = 8.5                   # SNR81 p. 2-4, "approximately the first 8.5 minutes of flight"
RS25_MIXTURE = 6.0                       # SNR81 p. 2-4
SP125_ENGINE_FW = (75.0, 125.0)          # SP-125 Section 2.1: lbf of thrust per lb of engine, larger modern engines
SP125_PROP_FRACTION = dict(pump=0.94, pressure=0.89)   # SP-125 Section 2.1, "propellant fraction"
TANK_PSIA = dict(pump=(30.0, 100.0), pressure=(100.0, 400.0))   # SP-125 Section 8.1
RP1_RHO_RANGE = (800.0, 820.0)           # SP-125 Table 1-4, 0.8 to 0.82 g/cc at 68 F
# The kerosene density of the chapter (pages 4.4 and "Engines and tanks"): the low end of that range, which
# gives the larger tank and agrees with SP-125's own bulk density of oxygen and kerosene at a mixture ratio
# of 2.56 (1.02 g/cc, Table 1-9) with the NIST oxygen density.
RP1_RHO = RP1_RHO_RANGE[0]
RP1_BOIL_F = 342.0                       # SP-125 Table 1-4, boiling 342 to 507 F
AL_RHO = 0.1 * LB_KG / IN ** 3           # SP-125 Section 8.2, aluminum alloys, average density 0.1 lb/in^3
AL_SW_PSI = 31800.0                      # SP-125 Sample Calculation 8-2, 6061-T6, mainstage
AL_MIN_WALL_IN = 0.020                   # SP-125 Section 8.2, lowest wall stock for aluminum alloys
SP125_ULLAGE = 0.025                     # SP-125 Sample Calculation 8-1


# ===================================================================== unit checks
if __name__ == "__main__":
    def close(a, b, tol, what):
        assert abs(a - b) <= tol * abs(b), f"{what}: {a!r} vs {b!r}"

    G0 = 9.81
    # RS-25: the exit diameter from the two thrusts against HAER's 90.7 in (and SNR81's "2.3 m")
    d, dp, rel = engine_check(RS25)
    assert abs(rel) < 0.03, (d, dp, rel)
    s = engine_si(RS25)
    # one flow at both points: F/(I_sp g0) the same at sea level and in vacuum (SNR81 is self-consistent)
    close(s["F_sl"] / (s["isp_sl"] * G0), s["F_vac"] / (s["isp_vac"] * G0), 1e-3, "RS-25 one mass flow")
    close((RS25["exit_d_in"] / RS25["throat_d_in"]) ** 2, RS25["area_ratio"], 2e-3, "RS-25 area ratio from HAER diameters")
    # F-1: no NASA vacuum thrust, so no check (kept only for its area ratio and exit diameter)
    assert engine_check(F1) is None
    # Vulcain 2: the manual's rounded sea-level values do not pass (mass flows differ by 4 percent)
    v = engine_si(VULCAIN2)
    assert abs(v["F_sl"] / (v["isp_sl"] * G0) / (v["F_vac"] / (v["isp_vac"] * G0)) - 1.0) > 0.03
    # SP-125: I_s = c* C_f / g (Eq. 1-31c) holds on every row, in the table's own units (g = 32.174 ft/s^2)
    for k, P in PROPELLANTS.items():
        close(P["cstar_fps"] * P["Cf"] / 32.174, P["Is"], 3e-3, f"{k}: c* C_f / g = I_s")
    # Saturn V: SP-4029's propellant at ignition (4,730,675 lb for the S-IC) is oxidizer plus fuel
    close(SATURN_V_AS506["S-IC"]["ox_lb"] + SATURN_V_AS506["S-IC"]["fuel_lb"], 4730675.0, 1e-12, "S-IC propellant")
    tot = sum(sum(v[k] for k in ("dry_lb", "ox_lb", "fuel_lb", "other_lb")) for v in SATURN_V_AS506.values())
    assert tot < SATURN_V_AS506_TOTAL_LB, "stages are part of the vehicle total"
    # inert mass fractions of real stages: 4 to 25 percent for every stage but the avionics-carrying AVUM
    for name, veh, kind, dry, prop, src in STAGES:
        f = dry / (dry + prop)
        assert 0.04 < f < (0.6 if name == "AVUM" else 0.25), (name, f)
    # NIST and SP-125 agree on the cryogens (boiling point within 0.1 K, density within 0.3 percent)
    close(f_to_k(SP125_PROPERTIES["liquid oxygen"][1]), NIST["oxygen"]["Tb"], 2e-3, "LOX boiling point")
    close(SP125_PROPERTIES["liquid oxygen"][2] * 1000.0, NIST["oxygen"]["rho"], 3e-3, "LOX density")
    close(SP125_PROPERTIES["liquid hydrogen"][2] * 1000.0, NIST["hydrogen"]["rho"], 3e-3, "LH2 density")
    # bulk density: SP-125's LOX/LH2 row from its own component densities
    close(bulk_density(4.02, 1142.0, 71.0), 280.0, 0.02, "bulk density of LOX/LH2 at 4.02")
    # classes of launch vehicles
    assert [lv_class(v["payload"]) for v in LAUNCH_VEHICLES][:2] == ["small", "small"]
    assert lv_class(95000.0) == "super heavy" and lv_class(2250.0) == "medium"
    assert all(lo < hi for _, lo, hi, *_ in [(k[0], k[1], k[2]) for k in PROPULSION_KINDS])
    print("published.py: all unit checks passed")
    print(f"  RS-25 exit diameter from the thrusts {d:.4f} m against {dp:.4f} m published ({100 * rel:+.2f}%)")
