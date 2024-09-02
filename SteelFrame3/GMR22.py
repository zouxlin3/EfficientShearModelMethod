import pandas as pd
from PythonBase.IO import read_AT2
from PythonBase.Unit import G
import numpy as np


if __name__ == '__main__':
    path_GMR_index = 'F:/data_RSRP/GMR/index.csv'
    GMR_index = pd.read_csv(path_GMR_index)
    target = 0.3 * G
    for index, row in GMR_index.iterrows():
        ag, npts, dt = read_AT2(row['path'])
        PGA = max(np.abs(ag))
        factor = target / PGA
        # factor = 1
        ag_ = ag * factor
        np.savetxt(f'F:/data_RSRP/GMR_Uniform/{row["ID"]}.txt', ag_)
