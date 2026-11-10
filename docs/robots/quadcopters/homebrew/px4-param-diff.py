# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

"""
@title PX4 Parameter Multi-Way Comparison Utility
@author Claude
@date 2026-09-14
@updated 2026-10-21

This script compares an arbitrary bundle (2 or more) of PX4 .params files side by side
and reports every parameter whose value is not identical across all of them, writing
the result to a CSV table for manual review. It excludes the per-drone calibration
parameters (and the parameters the firmware writes itself) listed on the wiki page
"Calibration and Per-Drone Parameters", because those are expected to differ between
vehicles and do not represent configuration drift. Everything else is compared,
including the parameters that used to be skipped (SENS_, PWM_, CA_, MOT_, ...).
Keep the lists below in sync with that page.

Missing parameters (present in some files but not others) are also reported, with blank
cells for the files that don't have them.

This is not a complete solution; users must still verify and understand what's going on!
"""
import argparse
import csv
import math
import pathlib

CALIBRATION_PREFIXES = ('CAL_GYRO', 'CAL_ACC', 'CAL_MAG', 'CAL_BARO')
CALIBRATION_NAMES = {
    'SENS_BOARD_X_OFF', 'SENS_BOARD_Y_OFF',
    'BAT1_V_DIV', 'BAT1_A_PER_V',
    'LND_FLIGHT_T_HI', 'LND_FLIGHT_T_LO', 'COM_FLIGHT_UUID', 'EKF2_MAG_DECL',
} | {f'RC{n}_{field}' for n in range(1, 11) for field in ('MIN', 'TRIM', 'MAX')}


def is_excluded(name, extra_prefixes):
    return (name in CALIBRATION_NAMES
            or name.startswith(CALIBRATION_PREFIXES)
            or name.startswith(tuple(extra_prefixes)))


def load_file(path):
    data = {}
    p = pathlib.Path(path)
    if not p.exists():
        exit(f"Missing file: {path}")
    for line in p.read_text().splitlines():
        if line.startswith('#') or not line.strip(): continue
        parts = line.split()
        if len(parts) >= 4:
            data[parts[2]] = {'val': float(parts[3]), 'type': parts[4] if len(parts) > 4 else "9"}
    return data


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compare 2+ PX4 .params files and report every parameter that "
                    "differs (or is missing) across the bundle, excluding the per-drone "
                    "calibration parameters listed on the wiki."
    )
    parser.add_argument("--files", nargs='+', required=True,
                        help="Two or more .params files to compare, e.g. "
                             "--files astro1.params astro2.params astro3.params")
    parser.add_argument("--output_csv", required=True, help="Path to write the comparison CSV to")
    parser.add_argument("--ignore-prefix", nargs='*', default=[], metavar="PREFIX",
                        help="Optional extra parameter-name prefixes to leave out, e.g. "
                             "--ignore-prefix PWM_ CA_")
    return parser.parse_args()


def main():
    args = parse_args()
    if len(args.files) < 2:
        exit("Need at least 2 files to compare.")

    # Use each file's stem (filename without extension) as its column header.
    # Guard against collisions (e.g. two files both named "astro.params" in
    # different directories) since that would silently merge their columns.
    labels = [pathlib.Path(f).stem for f in args.files]
    if len(set(labels)) != len(labels):
        exit("Two or more input files share the same filename stem; rename them "
            "so each has a unique name.")

    datasets = [load_file(f) for f in args.files]

    all_names = sorted(set().union(*(d.keys() for d in datasets)))

    rows = []
    for name in all_names:
        if is_excluded(name, args.ignore_prefix):
            continue

        present_vals = [d[name]['val'] for d in datasets if name in d]
        # Skip params present in every file with identical values (rel tolerance,
        # matching the tolerance used elsewhere for this fleet's param diffing).
        if len(present_vals) == len(datasets) and all(
            math.isclose(v, present_vals[0], rel_tol=1e-5) for v in present_vals
        ):
            continue

        param_type = next(d[name]['type'] for d in datasets if name in d)
        row = {'name': name, 'type': param_type}
        for label, d in zip(labels, datasets):
            row[label] = d[name]['val'] if name in d else ''
        rows.append(row)

    out = pathlib.Path(args.output_csv)
    fieldnames = ['name', 'type'] + labels
    with out.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {out}. {len(rows)} differing/missing parameters found across {len(args.files)} files.")


if __name__ == "__main__":
    main()
