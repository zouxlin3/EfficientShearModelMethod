from PythonBase.IO import log2file
from PythonBase.Basic import log
import subprocess
from typing import NoReturn


def gen_SpoSettings(target_floor: int) -> NoReturn:
    iDmax = [
        '0.02 0.04 0.06 0.08',
        '0.02 0.04 0.06 0.08',
        '0.02 0.04 0.06 0.08',
        '0.02 0.04 0.06 0.08',
        '0.02 0.04 0.06 0.08',
        '0.02 0.04 0.06 0.08',
        '0.02 0.04 0.06 0.08',
        '0.02 0.04 0.06 0.08',
        '0.02 0.04 0.06 0.08',
    ]
    content = f'set dataDir F:/data_RSRP/SteelFrame/SPO;\n' \
              f'set TargetFloor {target_floor};\n' \
              f'set iDmax "{iDmax[target_floor - 1]}";\n'
    with open('SpoSettings.tcl', 'w') as f:
        f.write(content)
        f.flush()


def simulation(target_floor: int) -> list:
    msg_list = []
    gen_SpoSettings(target_floor)
    command = f'opensees MainStatic.tcl'
    msg_list.append(log(f'Start static pushover of floor {target_floor}'))
    ret = subprocess.run(command, stderr=subprocess.PIPE, shell=True)
    stderr = str(ret.stderr)
    if 'Successfully Finished!' in stderr:
        msg_list.append(log(f'Finish static pushover of floor {target_floor}'))
    else:
        msg_list.append(log(f'Failed when static pushover of floor {target_floor}', 'ERROR'))
        msg_list.append(log('Stderr: ' + stderr.split('\\r\\n')[-3], 'ERROR'))
    return msg_list


if __name__ == '__main__':
    path_log = 'Logs.txt'
    story = 9
    for i in range(1, story + 1):
        msg_list = simulation(i)
        log2file(msg_list, path_log)
