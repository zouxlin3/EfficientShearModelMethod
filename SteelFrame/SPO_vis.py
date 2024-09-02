import pandas as pd
from PythonBase.IO import readOSresult
from typing import NoReturn
from PythonBase.Figure import setFont, cycle
from PythonBase.Unit import kN
from PythonBase.Basic import del_nan


def post_process() -> pd.DataFrame:
    dir_results = 'F:/data_RSRP/SteelFrame/SPO/'
    save_path = 'F:/data_RSRP/SteelFrame/SPO/results.csv'

    columns = [str(i) for i in range(1, 7)]
    Fcol1 = readOSresult(dir_results + 'SPO_1_force.out', columns)
    Fcol2 = readOSresult(dir_results + 'SPO_2_force.out', columns)
    Fcol3 = readOSresult(dir_results + 'SPO_3_force.out', columns)
    Fcol4 = readOSresult(dir_results + 'SPO_4_force.out', columns)
    Fcol5 = readOSresult(dir_results + 'SPO_5_force.out', columns)
    Fcol6 = readOSresult(dir_results + 'SPO_6_force.out', columns)
    Fcol7 = readOSresult(dir_results + 'SPO_7_force.out', columns)
    Fcol8 = readOSresult(dir_results + 'SPO_8_force.out', columns)
    Fcol9 = readOSresult(dir_results + 'SPO_9_force.out', columns)
    force1 = - Fcol1.sum(axis=1).values
    force2 = - Fcol2.sum(axis=1).values
    force3 = - Fcol3.sum(axis=1).values
    force4 = - Fcol4.sum(axis=1).values
    force5 = - Fcol5.sum(axis=1).values
    force6 = - Fcol6.sum(axis=1).values
    force7 = - Fcol7.sum(axis=1).values
    force8 = - Fcol8.sum(axis=1).values
    force9 = - Fcol9.sum(axis=1).values

    disp1 = readOSresult(dir_results + 'SPO_1_disp.out', ['disp'])['disp'].values
    disp2 = readOSresult(dir_results + 'SPO_2_disp.out', ['disp'])['disp'].values
    disp3 = readOSresult(dir_results + 'SPO_3_disp.out', ['disp'])['disp'].values
    disp4 = readOSresult(dir_results + 'SPO_4_disp.out', ['disp'])['disp'].values
    disp5 = readOSresult(dir_results + 'SPO_5_disp.out', ['disp'])['disp'].values
    disp6 = readOSresult(dir_results + 'SPO_6_disp.out', ['disp'])['disp'].values
    disp7 = readOSresult(dir_results + 'SPO_7_disp.out', ['disp'])['disp'].values
    disp8 = readOSresult(dir_results + 'SPO_8_disp.out', ['disp'])['disp'].values
    disp9 = readOSresult(dir_results + 'SPO_9_disp.out', ['disp'])['disp'].values

    data_dict = {
        'disp_1': disp1, 'force_1': force1,
        'disp_2': disp2, 'force_2': force2,
        'disp_3': disp3, 'force_3': force3,
        'disp_4': disp4, 'force_4': force4,
        'disp_5': disp5, 'force_5': force5,
        'disp_6': disp6, 'force_6': force6,
        'disp_7': disp7, 'force_7': force7,
        'disp_8': disp8, 'force_8': force8,
        'disp_9': disp9, 'force_9': force9,
    }
    data = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data_dict.items()]))
    data.to_csv(save_path, index=False)
    return data


def visualization(data: pd.DataFrame) -> NoReturn:
    setFont('../TimesSong.ttf', 'TimesSong')
    story = 9
    save_path = 'F:/data_RSRP/SteelFrame/SPO/InterStory_{0}.png'
    for i in range(story):
        disp = del_nan(data[f'disp_{i + 1}'].values)
        force = del_nan(data[f'force_{i + 1}'].values) / kN
        cycle(disp, force, saveName=save_path.format(i + 1))


if __name__ == '__main__':
    data = post_process()
    visualization(data)
