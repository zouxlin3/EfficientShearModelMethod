import pandas as pd


if __name__ == '__main__':
    targets = [0.1, 0.3, 0.5, 0.7, 0.9]
    rmse_acc, rmse_vel, rmse_disp = [], [], []
    mae_acc, mae_vel, mae_disp = [], [], []
    for target in targets:
        avg_path = f'F:/data_RSRP/{target}g/SteelFrame3/TimeErrorAvg.csv'
        avg = pd.read_csv(avg_path, index_col=0).squeeze()

        rmse_acc.append(avg['ShearModel_accel_rmse'])
        rmse_vel.append(avg['ShearModel_vel_rmse'])
        rmse_disp.append(avg['ShearModel_disp_rmse'])
        mae_acc.append(avg['ShearModel_accel_mae'])
        mae_vel.append(avg['ShearModel_vel_mae'])
        mae_disp.append(avg['ShearModel_disp_mae'])
    
    df = {'PGA': targets, 
          'rmse_acc': rmse_acc, 'rmse_vel': rmse_vel, 'rmse_disp': rmse_disp, 
          'mae_acc': mae_acc, 'mae_vel': mae_vel, 'mae_disp': mae_disp}
    df = pd.DataFrame(df)
    path_save = 'F:/data_RSRP/SteelFrame3/PGAvsMetric.csv'
    df.to_csv(path_save, index=False)
