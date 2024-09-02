import pandas as pd
import numpy as np


if __name__ == '__main__':
    story_heights = [5486.4] + [3962.4] * 8
    story = 9

    targets = [0.1, 0.3, 0.5, 0.7, 0.9]
    for n, target in enumerate(targets):
        IDs = []
        for j in range(1, 135 + 1):
            IDs.append(j)
        df = pd.DataFrame({
            'ID': IDs,
        })

        data_path = f'F:/data_RSRP/{target}g/SteelFrame/DynResults.csv'
        max_save_path = f'F:/data_RSRP/{target}g/SteelFrame/MaxRes.csv'
        avg_save_path = f'F:/data_RSRP/{target}g/SteelFrame/AvgRes.csv'
        data = pd.read_csv(data_path)

        for model in ['', 'ShearModel']:
            for i in range(len(IDs)):
                ID = IDs[i]
                for r in ['accel', 'vel']:
                    max_res_f = []
                    for f in range(1, story + 1):
                        res = data[f'{model}_{ID}_{r}_{f}'].values
                        max_res = np.nanmax(np.abs(res))
                        df.loc[i, f'{model}_{r}_{f}'] = max_res
                for f in range(1, story + 1):
                    if f == 1:
                        disp = data[f'{model}_{ID}_disp_{f}'].values
                        IDR = disp / story_heights[f - 1]
                        max_IDR = np.nanmax(np.abs(IDR))
                    else:
                        disp1 = data[f'{model}_{ID}_disp_{f - 1}'].values
                        disp2 = data[f'{model}_{ID}_disp_{f}'].values
                        IDR = (disp2 - disp1) / story_heights[f - 1]
                        max_IDR = np.nanmax(np.abs(IDR))
                    df.loc[i, f'{model}_IDR_{f}'] = max_IDR
        df.to_csv(max_save_path, index=False)
        df.mean().to_csv(avg_save_path)
