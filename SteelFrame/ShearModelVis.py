import pandas as pd
from PythonBase.IO import read_json
from PythonBase.Figure import setFont, cycle_compare
from PythonBase.Unit import kN
import numpy as np
from typing import NoReturn
from PyOS3.SDOF import SDOF, static
from PyOS3.Material import Hysteretic


def simulation(ESDOF: dict, disp: np.ndarray) -> tuple:
    SDOF(Hysteretic, ESDOF['x'], ESDOF['positive_peak'], ESDOF['negative_peak'],
         ESDOF['max_d_point'], ESDOF['min_d_point'], ESDOF['mass'])
    disp_, force_ = static(disp)
    return disp_, force_


def visualization(floor: int, disp: np.ndarray, force: np.ndarray, disp_: np.ndarray, force_: np.ndarray) -> NoReturn:
    setFont('../TimesSong.ttf', 'TimesSong')
    save_path = f'F:/data_RSRP/SteelFrame/ShearModel/InterStory_{floor}.png'
    cycle_compare(disp, force / kN, disp_, force_ / kN, ['Fiber model', 'Shear model'], save_path)


if __name__ == '__main__':
    ESDOF1 = read_json('F:/data_RSRP/SteelFrame/ShearModel/floor1.json')
    ESDOF2 = read_json('F:/data_RSRP/SteelFrame/ShearModel/floor2.json')
    ESDOF3 = read_json('F:/data_RSRP/SteelFrame/ShearModel/floor3.json')
    ESDOF4 = read_json('F:/data_RSRP/SteelFrame/ShearModel/floor4.json')
    ESDOF5 = read_json('F:/data_RSRP/SteelFrame/ShearModel/floor5.json')
    ESDOF6 = read_json('F:/data_RSRP/SteelFrame/ShearModel/floor6.json')
    ESDOF7 = read_json('F:/data_RSRP/SteelFrame/ShearModel/floor7.json')
    ESDOF8 = read_json('F:/data_RSRP/SteelFrame/ShearModel/floor8.json')
    ESDOF9 = read_json('F:/data_RSRP/SteelFrame/ShearModel/floor9.json')
    ESDOF = [ESDOF1, ESDOF2, ESDOF3, ESDOF4, ESDOF5, ESDOF6, ESDOF7, ESDOF8, ESDOF9]
    data = pd.read_csv('F:/data_RSRP/SteelFrame/SPO/results.csv')
    res_save_path = f'F:/data_RSRP/SteelFrame/ShearModel/result.csv'
    floors = 9
    data_dict = {}
    for i in range(floors):
        disp = data[f'disp_{i + 1}'].values
        force = data[f'force_{i + 1}'].values
        disp_, force_ = simulation(ESDOF[i], disp)
        visualization(i + 1, disp, force, disp_, -force_)
        data_dict[f'disp_{i + 1}'] = disp_
        data_dict[f'force_{i + 1}'] = -force_
    res = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data_dict.items()]))
    res.to_csv(res_save_path, index=False)
