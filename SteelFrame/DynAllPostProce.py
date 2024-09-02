import pandas as pd
from PythonBase.IO import readOSresult, processBar


def post_process(model: str, ID: int, PGA: float) -> pd.DataFrame:
    dir_results = f'F:/data_RSRP/{PGA}g/SteelFrame/{model}DynAll/{ID}/'

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

    data = pd.DataFrame({
        f'time_{model}_{ID}': time,
        f'{model}_{ID}_disp_1': disp1, f'{model}_{ID}_vel_1': vel1, f'{model}_{ID}_accel_1': accel1,
        f'{model}_{ID}_disp_2': disp2, f'{model}_{ID}_vel_2': vel2, f'{model}_{ID}_accel_2': accel2,
        f'{model}_{ID}_disp_3': disp3, f'{model}_{ID}_vel_3': vel3, f'{model}_{ID}_accel_3': accel3,
        f'{model}_{ID}_disp_4': disp4, f'{model}_{ID}_vel_4': vel4, f'{model}_{ID}_accel_4': accel4,
        f'{model}_{ID}_disp_5': disp5, f'{model}_{ID}_vel_5': vel5, f'{model}_{ID}_accel_5': accel5,
        f'{model}_{ID}_disp_6': disp6, f'{model}_{ID}_vel_6': vel6, f'{model}_{ID}_accel_6': accel6,
        f'{model}_{ID}_disp_7': disp7, f'{model}_{ID}_vel_7': vel7, f'{model}_{ID}_accel_7': accel7,
        f'{model}_{ID}_disp_8': disp8, f'{model}_{ID}_vel_8': vel8, f'{model}_{ID}_accel_8': accel8,
        f'{model}_{ID}_disp_9': disp9, f'{model}_{ID}_vel_9': vel9, f'{model}_{ID}_accel_9': accel9,
    })
    return data


if __name__ == '__main__':
    targets = [0.1, 0.3, 0.5, 0.7, 0.9]
    for i, target in enumerate(targets):
        save_path = f'F:/data_RSRP/{target}g/SteelFrame/DynResults.csv'
        data = []
        for t in ['', 'ShearModel']:
            for j in range(1, 135 + 1):
                data_ = post_process(t, j, target)
                data.append(data_)
                processBar(j, 135)
        df = pd.concat(data, axis=1)
        df.to_csv(save_path, index=False)
