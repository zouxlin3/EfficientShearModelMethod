import pandas as pd
from typing import NoReturn
from PythonBase.Figure import setFont, timeHis_compare
from pathlib import Path
from PythonBase.IO import readOSresult


def post_process(model: str) -> pd.DataFrame:
    dir_results = f'F:/data_RSRP/SteelFrame/{model}DynElcentro/'

    time = readOSresult(dir_results + 'Dyn_1_disp.out', ['time', 'disp'])['time'].values

    disp1 = readOSresult(dir_results + 'Dyn_1_disp.out', ['time', 'disp'])['disp'].values
    disp2 = readOSresult(dir_results + 'Dyn_2_disp.out', ['time', 'disp'])['disp'].values
    disp3 = readOSresult(dir_results + 'Dyn_3_disp.out', ['time', 'disp'])['disp'].values
    disp4 = readOSresult(dir_results + 'Dyn_4_disp.out', ['time', 'disp'])['disp'].values
    disp5 = readOSresult(dir_results + 'Dyn_5_disp.out', ['time', 'disp'])['disp'].values
    disp6 = readOSresult(dir_results + 'Dyn_6_disp.out', ['time', 'disp'])['disp'].values
    disp7 = readOSresult(dir_results + 'Dyn_7_disp.out', ['time', 'disp'])['disp'].values
    disp8 = readOSresult(dir_results + 'Dyn_8_disp.out', ['time', 'disp'])['disp'].values
    disp9 = readOSresult(dir_results + 'Dyn_9_disp.out', ['time', 'disp'])['disp'].values

    vel1 = readOSresult(dir_results + 'Dyn_1_vel.out', ['time', 'vel'])['vel'].values
    vel2 = readOSresult(dir_results + 'Dyn_2_vel.out', ['time', 'vel'])['vel'].values
    vel3 = readOSresult(dir_results + 'Dyn_3_vel.out', ['time', 'vel'])['vel'].values
    vel4 = readOSresult(dir_results + 'Dyn_4_vel.out', ['time', 'vel'])['vel'].values
    vel5 = readOSresult(dir_results + 'Dyn_5_vel.out', ['time', 'vel'])['vel'].values
    vel6 = readOSresult(dir_results + 'Dyn_6_vel.out', ['time', 'vel'])['vel'].values
    vel7 = readOSresult(dir_results + 'Dyn_7_vel.out', ['time', 'vel'])['vel'].values
    vel8 = readOSresult(dir_results + 'Dyn_8_vel.out', ['time', 'vel'])['vel'].values
    vel9 = readOSresult(dir_results + 'Dyn_9_vel.out', ['time', 'vel'])['vel'].values

    accel1 = readOSresult(dir_results + 'Dyn_1_accel.out', ['time', 'accel'])['accel'].values
    accel2 = readOSresult(dir_results + 'Dyn_2_accel.out', ['time', 'accel'])['accel'].values
    accel3 = readOSresult(dir_results + 'Dyn_3_accel.out', ['time', 'accel'])['accel'].values
    accel4 = readOSresult(dir_results + 'Dyn_4_accel.out', ['time', 'accel'])['accel'].values
    accel5 = readOSresult(dir_results + 'Dyn_5_accel.out', ['time', 'accel'])['accel'].values
    accel6 = readOSresult(dir_results + 'Dyn_6_accel.out', ['time', 'accel'])['accel'].values
    accel7 = readOSresult(dir_results + 'Dyn_7_accel.out', ['time', 'accel'])['accel'].values
    accel8 = readOSresult(dir_results + 'Dyn_8_accel.out', ['time', 'accel'])['accel'].values
    accel9 = readOSresult(dir_results + 'Dyn_9_accel.out', ['time', 'accel'])['accel'].values

    data = pd.DataFrame({f'time_{model}': time,
                         f'{model}_disp_1': disp1,
                         f'{model}_vel_1': vel1,
                         f'{model}_accel_1': accel1,
                         f'{model}_disp_2': disp2,
                         f'{model}_vel_2': vel2,
                         f'{model}_accel_2': accel2,
                         f'{model}_disp_3': disp3,
                         f'{model}_vel_3': vel3,
                         f'{model}_accel_3': accel3,
                         f'{model}_disp_4': disp4,
                         f'{model}_vel_4': vel4,
                         f'{model}_accel_4': accel4,
                         f'{model}_disp_5': disp5,
                         f'{model}_vel_5': vel5,
                         f'{model}_accel_5': accel5,
                         f'{model}_disp_6': disp6,
                         f'{model}_vel_6': vel6,
                         f'{model}_accel_6': accel6,
                         f'{model}_disp_7': disp7,
                         f'{model}_vel_7': vel7,
                         f'{model}_accel_7': accel7,
                         f'{model}_disp_8': disp8,
                         f'{model}_vel_8': vel8,
                         f'{model}_accel_8': accel8,
                         f'{model}_disp_9': disp9,
                         f'{model}_vel_9': vel9,
                         f'{model}_accel_9': accel9,
                         })
    return data


def visualization(fiber: pd.DataFrame, shear: pd.DataFrame, model: str) -> NoReturn:
    setFont('../TimesSong.ttf', 'TimesSong')
    story = 9
    save_path = 'F:/data_RSRP/SteelFrame/{0}DynElcentro/{1}_{2}.png'
    Path(f'F:/data_RSRP/SteelFrame/{model}DynElcentro').mkdir(parents=True, exist_ok=True)
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
    fiber_path = 'F:/data_RSRP/SteelFrame/DynElcentro/results.csv'
    shear_path = 'F:/data_RSRP/SteelFrame/{0}DynElcentro/results.csv'
    fiber = post_process('')
    fiber.to_csv(fiber_path, index=False)
    for t in ['ShearModel']:
        shear_ = post_process(t)
        shear_.to_csv(shear_path.format(t), index=False)
        visualization(fiber, shear_, t)
