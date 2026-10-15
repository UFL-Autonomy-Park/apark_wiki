"""
@title PX4 Parameter Migration Utility
@date 2025-12-21
@author Max Gardenswartz

This script automates the migration of flight parameters between PX4 firmware versions for 
the Homebrew fleet. It identifies differences between a known-working configuration 
and a fresh firmware default set, filtering out hardware-specific or safety-critical 
parameters that require manual recalibration (e.g., sensors, motor ordering). 

The tool was specifically developed to addresss the 1.15.4 to 1.16.0 transition, where PX4 
often fails to port parameters due to name changes and internal logic shifts. It serves 
as a robust starting point for future upgrades (e.g., 1.16.0 to 1.17.0) by ensuring 
working configurations are matched against valid parameter names in the new firmware.

This is not a complete solution; users must still verify and understand what's going on!
"""
import math
import pathlib

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

def main():
    old_file = input("Working param file [working.params]: ").strip() or "working.params"
    new_file = input("Fresh default file [fresh.params]: ").strip() or "fresh.params"
    old_data = load_file(old_file)
    new_data = load_file(new_file)

    # COM_ parameters are preserved to maintain shared safety/threshold/transmitter logic across the fleet
    # User must manually check if other parameters' names have changed
    # Otherwise, the default logic will be used
    ignore = ('CAL_', 'SENS_', 'TCAL_', 'CTR_', 'SYS_CTRL_ALLOC', 'SYS_AUTOSTART', 
              'SYS_AUTOCONFIG', 'PWM_', 'DSHOT_', 'MOT_', 'CA_')

    merged = []
    for name, info in new_data.items():
        if name in old_data and not name.startswith(ignore):
            ov, nv, pt = old_data[name]['val'], info['val'], info['type']
            if not math.isclose(ov, nv, rel_tol=1e-5):
                vs = str(int(ov)) if pt == "6" else f"{ov:.9f}".rstrip('0').rstrip('.')
                if pt != "6" and "." not in vs: vs += ".0"
                merged.append(f"1\t1\t{name}\t{vs}\t{pt}\n")

    out = pathlib.Path("new_template.params")
    out.write_text("# Vehicle-Id Component-Id Name Value Type\n" + "".join(merged))
    print(f"Generated {out}. {len(merged)} parameters migrated.")

if __name__ == "__main__":
    main()