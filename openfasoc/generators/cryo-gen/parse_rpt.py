import sys
import json
import os
import re, subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common.check_gen_files import check_gen_files

sys.stdout.flush()

if (len(sys.argv) > 1) and (sys.argv[1] == "sky130hd_cryo"):
    drc_filename = "flow/reports/sky130hd/cryo/6_final_drc.rpt"
    lvs_filename = "flow/reports/sky130hd/cyro/6_final_lvs.rpt"
elif (len(sys.argv) == 1) or (sys.argv[1] == "sky130hvl_ldo"):
    drc_filename = "work/6_final_drc.rpt"
    lvs_filename = "work/6_final_lvs.rpt"
else:
    drc_filename = "work/"+sys.argv[1]+"/6_final_drc.rpt"
    lvs_filename = "work/"+sys.argv[1]+"/6_final_lvs.rpt"

# using full because sims disabled for LDO for now
if (len(sys.argv) > 1) and ((sys.argv[1] == "sky130hvl_ldo") or (sys.argv[1] == "sky130hvl_ldo_full")):
    with open(drc_filename, 'r') as f1, open("../../../.github/scripts/expected_drc_reports/expected_ldo_drc.rpt", 'r') as f2:
        content1 = f1.readlines()
        content2 = f2.readlines()
        if content1 == content2:
            print("DRC is clean!")
        else:
            raise ValueError("DRC failed!")
elif sum(1 for line in open(drc_filename)) > 3:
    raise ValueError("DRC failed!")
else:
    print("DRC is clean!")

# cryo LVS check 
if (len(sys.argv) > 1) and (sys.argv[1] == "sky130hd_cryo"):
    lvs_line = subprocess.check_output(["tail", "-1", lvs_filename]).decode(
        sys.stdout.encoding
    )
    regex = r"failed"
    match = re.search(regex, lvs_line)
    
    if match != None:
        raise ValueError("LVS failed!")
    else:
        print("LVS is clean!")
else:        
    with open(lvs_filename) as f:
        f1 = f.read()
    
        if "failed" in f1:
            raise ValueError("LVS failed!")
        else:
            print("LVS is clean!")

if ((len(sys.argv) > 1) and ((sys.argv[1] == "sky130hvl_ldo") or (sys.argv[1] == "sky130hvl_ldo_full"))) or ((len(sys.argv) > 1) and (sys.argv[1] == "sky130hd_cryo")):
    print("Flow check is clean!")
else:
    json_filename = "test.json"

    if os.path.exists(json_filename):
        if check_gen_files():
            print("Flow check is clean!")
        else:
            print("Flow check failed!")
    else:
        raise ValueError(".json config file not found!")
