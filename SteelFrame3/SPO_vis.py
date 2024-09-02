import pandas as pd
from PythonBase.IO import readOSresult
from typing import NoReturn
from PythonBase.Figure import setFont, cycle
from PythonBase.Unit import kN
from PythonBase.Basic import del_nan


def post_process() -> pd.DataFrame:
    dir_results = 'F:/data_RSRP/SteelFrame3/SPO/'
    save_path = 'F:/data_RSRP/SteelFrame3/SPO/results.csv'

    columns = [str(i) for i in range(1, 6)]
    Fcol1 = readOSresult(dir_results + 'SPO_1_force.out', columns)
    Fcol2 = readOSresult(dir_results + 'SPO_2_force.out', columns)
    Fcol3 = readOSresult(dir_results + 'SPO_3_force.out', columns)
    force1 = - Fcol1.sum(axis=1).values
    force2 = - Fcol2.sum(axis=1).values
    force3 = - Fcol3.sum(axis=1).values

    disp1 = readOSresult(dir_results + 'SPO_1_disp.out', ['disp'])['disp'].values
    disp2 = readOSresult(dir_results + 'SPO_2_disp.out', ['disp'])['disp'].values
    disp3 = readOSresult(dir_results + 'SPO_3_disp.out', ['disp'])['disp'].values

    data_dict = {
        'disp_1': disp1, 'force_1': force1,
        'disp_2': disp2, 'force_2': force2,
        'disp_3': disp3, 'force_3': force3,
    }
    data = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data_dict.items()]))
    data.to_csv(save_path, index=False)
    return data


def visualization(data: pd.DataFrame) -> NoReturn:
    setFont('../TimesSong.ttf', 'TimesSong')
    story = 3
    save_path = 'F:/data_RSRP/SteelFrame3/SPO/InterStory_{0}.png'
    for i in range(story):
        disp = del_nan(data[f'disp_{i + 1}'].values)
        force = del_nan(data[f'force_{i + 1}'].values) / kN
        cycle(disp, force, saveName=save_path.format(i + 1))


if __name__ == '__main__':
    data = post_process()
    visualization(data)
