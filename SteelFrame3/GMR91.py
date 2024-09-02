import numpy as np
import pandas as pd
from PythonBase.Unit import G


def read_GMR(path: str):
    with open(path, 'r') as f:
        head = f.readline()
        content_head = head.split()
        dt, npts = float(content_head[0]), int(content_head[1])
    ag = np.loadtxt(GMR, skiprows=1)
    ag_ = ag * G
    return ag_, dt, npts


if __name__ == '__main__':
    GMR_path = 'F:/data_RSRP/GMR91/{0}_original.acc'
    save_path = 'F:/data_RSRP/GMR91_Uniform/{0}.txt'
    index_path = 'F:/data_RSRP/GMR91_Uniform/index_.csv'
    IDs, dts, nptss, ag_paths = [], [], [], []
    target = 0.3 * G
    for i in range(1, 92):
        GMR = GMR_path.format(i)
        ag, dt, npts = read_GMR(GMR)
        PGA = max(np.abs(ag))
        factor = target / PGA
        # factor = 1
        ag_ = ag * factor
        ag_path = save_path.format(i + 100)
        np.savetxt(ag_path, ag_)
        IDs.append(i + 100)
        dts.append(dt)
        nptss.append(npts)
        ag_paths.append(ag_path)
    df = pd.DataFrame(
        {
            'ID': IDs,
            'dt': dts,
            'npts': nptss,
            'path': ag_paths
        }
    )
    df.to_csv(index_path, index=False)
