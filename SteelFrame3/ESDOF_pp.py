from PythonBase.IO import read_json, write_json
from typing import NoReturn
import numpy as np
from PyOptimize.SDOF import Optimization
from PythonBase.Unit import t
import pandas as pd
from PythonBase.Basic import del_nan


def ESDOFpp(floor: int, disp: np.ndarray, force: np.ndarray, mass: float) -> NoReturn:
    pathESDOF = f'F:/data_RSRP/SteelFrame3/ShearModel/ESDOF{floor}.txt'
    save_path = f'F:/data_RSRP/SteelFrame3/ShearModel/floor{floor}.json'
    ESDOF = read_json(pathESDOF)
    x = [v for k, v in ESDOF.items()]
    opt = Optimization(disp, force, 'Hysteretic', 'ARO')
    result = {'x': list(x),
              'positive_peak': opt.positive_peak,
              'negative_peak': opt.negative_peak,
              'max_d_point': opt.max_d_point,
              'min_d_point': opt.min_d_point,
              'mass': mass}
    write_json(save_path, result)


if __name__ == '__main__':
    floors = 3
    mass_list = [95.57 * t * 5, 95.57 * t * 5, 103.4 * t * 5]
    data = pd.read_csv('F:/data_RSRP/SteelFrame3/SPO/results.csv')
    for f in range(floors):
        msg_list = []
        disp = del_nan(data[f'disp_{f + 1}'].values)
        force = del_nan(data[f'force_{f + 1}'].values)
        ESDOFpp(f + 1, disp, force, mass_list[f])
