from PythonBase.IO import log2file
from PythonBase.Basic import log
import subprocess
import pandas as pd


def gen_DynSettings(Row: pd.Series, PGA: float) -> None:
    content = f'set dataDir F:/data_RSRP/{PGA}g/SteelFrame/ShearModelDynAll/{Row["ID"]};\n' \
              f'set path_GMR {Row["path"]};\n' \
              f'set dt {Row["dt"]};\n' \
              f'set npts {int(Row["npts"])};\n' \
              f'set factor 1;\n'
    with open('DynSettings.tcl', 'w') as f:
        f.write(content)
        f.flush()


def simulation(Row: pd.Series, PGA: float) -> list:
    msg_list = []
    gen_DynSettings(Row, PGA)
    command = f'opensees MainShearModelDyn.tcl'
    msg_list.append(log(f'Start time history analysis with GMR {Row["ID"]} at {PGA}g of shear model'))
    ret = subprocess.run(command, stderr=subprocess.PIPE, shell=True)
    stderr = str(ret.stderr)
    if 'Successfully finished!' in stderr:
        msg_list.append(log(f'Finish time history analysis with GMR {Row["ID"]} at {PGA}g of shear model'))
    else:
        msg_list.append(log(f'Failed when time history analysis with GMR {Row["ID"]} at {PGA}g of shear model', 'ERROR'))
        msg_list.append(log('Stderr: ' + stderr.split('\\r\\n')[-3], 'ERROR'))
    return msg_list


if __name__ == '__main__':
    path_log = 'Logs.txt'
    targets = [0.1, 0.3, 0.5, 0.7, 0.9]
    for target in targets:
        path_GMR44_index = f'F:/data_RSRP/{target}g/GMR44.csv'
        GMR44_index = pd.read_csv(path_GMR44_index)
        for index, row in GMR44_index.iterrows():
            msg_list = simulation(row, target)
            log2file(msg_list, path_log)

        path_GMR91_index = f'F:/data_RSRP/{target}g/GMR91.csv'
        GMR91_index = pd.read_csv(path_GMR91_index)
        for index, row in GMR91_index.iterrows():
            msg_list = simulation(row, target)
            log2file(msg_list, path_log)
