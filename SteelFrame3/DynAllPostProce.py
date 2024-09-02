import pandas as pd
from PythonBase.IO import readOSresult, processBar


def post_process(model: str, ID: int, PGA: float) -> pd.DataFrame:
    dir_results = f'F:/data_RSRP/{PGA}g/SteelFrame3/{model}DynAll/{ID}/'

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

    data = pd.DataFrame({
        f'time_{model}_{ID}': time,
        f'{model}_{ID}_disp_1': disp1, f'{model}_{ID}_vel_1': vel1, f'{model}_{ID}_accel_1': accel1,
        f'{model}_{ID}_disp_2': disp2, f'{model}_{ID}_vel_2': vel2, f'{model}_{ID}_accel_2': accel2,
        f'{model}_{ID}_disp_3': disp3, f'{model}_{ID}_vel_3': vel3, f'{model}_{ID}_accel_3': accel3,
    })
    return data


if __name__ == '__main__':
    targets = [0.1, 0.3, 0.5, 0.7, 0.9]
    for i, target in enumerate(targets):
        save_path = f'F:/data_RSRP/{target}g/SteelFrame3/DynResults.csv'
        data = []
        for t in ['', 'ShearModel']:
            for j in range(1, 135 + 1):
                data_ = post_process(t, j, target)
                data.append(data_)
                processBar(j, 135)
        df = pd.concat(data, axis=1)
        df.to_csv(save_path, index=False)
