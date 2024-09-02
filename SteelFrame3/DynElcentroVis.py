import pandas as pd
from typing import NoReturn
from PythonBase.Figure import setFont, timeHis_compare
from pathlib import Path
from PythonBase.IO import readOSresult


def post_process(model: str) -> pd.DataFrame:
    dir_results = f'F:/data_RSRP/SteelFrame3/{model}DynElcentro/'

    time = readOSresult(dir_results + 'Dyn_1_disp.out', ['time', 'disp'])['time'].values

    disp1 = readOSresult(dir_results + 'Dyn_1_disp.out', ['time', 'disp'])['disp'].values
    disp2 = readOSresult(dir_results + 'Dyn_2_disp.out', ['time', 'disp'])['disp'].values
    disp3 = readOSresult(dir_results + 'Dyn_3_disp.out', ['time', 'disp'])['disp'].values

    vel1 = readOSresult(dir_results + 'Dyn_1_vel.out', ['time', 'vel'])['vel'].values
    vel2 = readOSresult(dir_results + 'Dyn_2_vel.out', ['time', 'vel'])['vel'].values
    vel3 = readOSresult(dir_results + 'Dyn_3_vel.out', ['time', 'vel'])['vel'].values

    accel1 = readOSresult(dir_results + 'Dyn_1_accel.out', ['time', 'accel'])['accel'].values
    accel2 = readOSresult(dir_results + 'Dyn_2_accel.out', ['time', 'accel'])['accel'].values
    accel3 = readOSresult(dir_results + 'Dyn_3_accel.out', ['time', 'accel'])['accel'].values

    data = pd.DataFrame({f'time_{model}': time,
                         f'{model}_disp_1': disp1,
                         f'{model}_vel_1': vel1,
                         f'{model}_accel_1': accel1,
                         f'{model}_disp_2': disp2,
                         f'{model}_vel_2': vel2,
                         f'{model}_accel_2': accel2,
                         f'{model}_disp_3': disp3,
                         f'{model}_vel_3': vel3,
                         f'{model}_accel_3': accel3})
    return data


def visualization(fiber: pd.DataFrame, shear: pd.DataFrame, model: str) -> NoReturn:
    setFont('../TimesSong.ttf', 'TimesSong')
    story = 3
    save_path = 'F:/data_RSRP/SteelFrame3/{0}DynElcentro/{1}_{2}.png'
    Path(f'F:/data_RSRP/SteelFrame3/{model}DynElcentro').mkdir(parents=True, exist_ok=True)
    labels = ['Fiber model', 'Shear model']
    for i in range(story):
        timeHis_compare(fiber[f'time_'].values, fiber[f'_disp_{i + 1}'].values,
                        shear[f'time_{model}'].values, shear[f'{model}_disp_{i + 1}'].values,
                        labels, 'Disp. / $\\mathrm{mm}$',
                        saveName=save_path.format(t, 'disp', i + 1))
        timeHis_compare(fiber[f'time_'].values, fiber[f'_vel_{i + 1}'].values,
                        shear[f'time_{model}'].values, shear[f'{model}_vel_{i + 1}'].values,
                        labels, 'Vel. / $\\mathrm{mm\\cdot s^{-1}}$',
                        saveName=save_path.format(t, 'vel', i + 1))
        timeHis_compare(fiber[f'time_'].values, fiber[f'_accel_{i + 1}'].values,
                        shear[f'time_{model}'].values, shear[f'{model}_accel_{i + 1}'].values,
                        labels, 'Accel. / $\\mathrm{mm\\cdot s^{-2}}$',
                        saveName=save_path.format(t, 'accel', i + 1))


if __name__ == '__main__':
    fiber_path = 'F:/data_RSRP/SteelFrame3/DynElcentro/results.csv'
    shear_path = 'F:/data_RSRP/SteelFrame3/{0}DynElcentro/results.csv'
    fiber = post_process('')
    fiber.to_csv(fiber_path, index=False)
    for t in ['ShearModel']:
        shear_ = post_process(t)
        shear_.to_csv(shear_path.format(t), index=False)
        visualization(fiber, shear_, t)
