import numpy as np
from PythonBase.IO import log2file, read_AT2
from PythonBase.Basic import log
from PythonBase.Unit import G
import subprocess
from typing import NoReturn


def gen_DynSettings() -> NoReturn:
    content = f'set dataDir F:/data_RSRP/SteelFrame3/DynElcentro;\n' \
              f'set path_GMR F:/data_RSRP/SteelFrame3/DynElcentro/GMR.txt;\n' \
              f'set dt {dt};\n' \
              f'set npts {npts};\n' \
              f'set factor {factor};\n' \
              f'set TargetFloor 0;\n'
    with open('DynSettings.tcl', 'w') as f:
        f.write(content)
        f.flush()


def simulation() -> list:
    msg_list = []
    gen_DynSettings()
    command = f'opensees MainDynamic.tcl'
    msg_list.append(log(f'Start time history analysis'))
    ret = subprocess.run(command, stderr=subprocess.PIPE, shell=True)
    stderr = str(ret.stderr)
    if 'Successfully finished!' in stderr:
        msg_list.append(log(f'Finish time history analysis'))
    else:
        msg_list.append(log(f'Failed when time history analysis', 'ERROR'))
        msg_list.append(log('Stderr: ' + stderr.split('\\r\\n')[-3], 'ERROR'))
    return msg_list


if __name__ == '__main__':
    path_log = 'Logs.txt'
    path_GMR = 'F:/data_RSRP/SteelFrame3/DynElcentro/RSN6_IMPVALL.I_I-ELC180.AT2'
    ag, npts, dt = read_AT2(path_GMR)
    PGA = max(ag)
    # factor = 0.7 * G / PGA
    factor = 1
    np.savetxt('F:/data_RSRP/SteelFrame3/DynElcentro/GMR.txt', ag)
    msg_list = simulation()
    # log2file(msg_list, path_log)
