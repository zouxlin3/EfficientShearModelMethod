import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error
from scipy import interpolate


def metrics(fiber: np.ndarray, shear: np.ndarray):
    rmse = np.sqrt(mean_squared_error(fiber, shear)) / (np.max(fiber) - np.min(fiber))
    mae = mean_absolute_error(fiber, shear) / (np.max(fiber) - np.min(fiber))
    return rmse, mae


def Interpolate(Time: np.ndarray, Res: np.ndarray, TargetTime: np.ndarray):
    Res_f = interpolate.interp1d(Time, Res)
    Res_ = Res_f(TargetTime)
    return Res_


if __name__ == '__main__':
    result_path = 'F:/data_RSRP/SteelFrame3/ShearModelDyn22/results.csv'
    save_path = 'F:/data_RSRP/SteelFrame3/ShearModelDyn22/ErrorMetrics.csv'
    # avg_path = 'F:/data_RSRP/SteelFrame3/ShearModelDyn22/ErrorAvg.csv'
    # std_path = 'F:/data_RSRP/SteelFrame3/ShearModelDyn22/ErrorStd.csv'
    data = pd.read_csv(result_path)
    story = 3
    IDs = [i * 2 + 2 for i in range(22)] + [i + 100 for i in range(1, 92)]
    result = {}
    for model in ['ShearModel']:
        for r in ['accel', 'vel', 'disp']:
            for f in range(1, story + 1):
                fiber_res_, shear_res_ = 0, 0
                rmse_list, mae_list = [], []
                for ID in IDs:
                    fiber_time = data[f'time__{ID}'].values
                    shear_time = data[f'time_{model}_{ID}'].values
                    fiber_time = fiber_time[~np.isnan(fiber_time)]
                    shear_time = shear_time[~np.isnan(shear_time)]
                    target_time = np.arange(fiber_time[0], min(fiber_time[-1], shear_time[-1]), fiber_time[1] - fiber_time[0])

                    fiber_res = data[f'_{ID}_{r}_{f}'].values
                    shear_res = data[f'{model}_{ID}_{r}_{f}'].values
                    fiber_res = fiber_res[~np.isnan(fiber_res)]
                    shear_res = shear_res[~np.isnan(shear_res)]
                    fiber_res_ = Interpolate(fiber_time, fiber_res, target_time)
                    shear_res_ = Interpolate(shear_time, shear_res, target_time)
                    rmse, mae = metrics(fiber_res_, shear_res_)
                    rmse_list.append(rmse)
                    # mae_list.append(mae)
                result[f'{model}_{r}_{f}'] = rmse_list
                # result[f'{model}_{r}_mae'] = mae_list
    df = pd.DataFrame(result)
    df.to_csv(save_path, index=False)
    # df.mean().to_csv(avg_path, index=True)
    # df.std().to_csv(std_path, index=True)
