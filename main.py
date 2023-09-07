from pathlib import Path
import numpy as np
import time
from time import strftime, localtime
from typing import NoReturn, Callable
from sklearn.metrics import mean_squared_error
import openseespy.opensees as ops


def readOSresult(pth: str, names: list) -> pd.DataFrame:
    f = open(pth, 'r')
    content = []
    for line in f.readlines():
        content.append(list(map(float, line.split())))
    content = np.array(content).T
    names.extend(['unknown'] * abs(len(content) - len(names)))

    data = {}
    for i, c in enumerate(content):
        data[names[i]] = c
    df = pd.DataFrame(data)
    f.close()
    return df


def read_json(pth: str) -> dict or list:
    with open(pth, 'r') as f:
        content = json.loads(f.read())
    return content


def write_json(pth: str, content: dict or list) -> NoReturn:
    with open(pth, 'w') as f:
        f.write(json.dumps(content, indent=4, separators=(',', ': ')))


def log2file(msg_list: list, pth: str) -> NoReturn:
    with open(pth, 'a') as f:
        for msg in msg_list:
            f.write(msg + '\n')


def aro(x0: np.ndarray, object_func: Callable, bounds: list, config: dict = None) -> tuple:
    if config:
        pop_size, epoch = config['pop_size'], config['epoch']
    else:
        pop_size, epoch = 10, 200

    LB, UB = [], []
    for bound in bounds:
        LB.append(bound[0])
        UB.append(bound[1])
    LB, UB = np.array(LB), np.array(UB)

    problem_dict = {
        'fit_func': object_func,
        'lb': LB,
        'ub': UB,
        'minmax': 'min',
    }

    model = OriginalARO(epoch, pop_size)
    x, fitness = model.solve(problem_dict)
    return x, fitness


def SDOF(material: Callable, params_mat: list, positive_peak: list, negative_peak: list,
         max_d_point: list, min_d_point: list, mass: float) -> NoReturn:
    ops.wipe()
    ops.model('BasicBuilder', '-ndm', 1, '-ndf', 1)
    ops.node(0, 0)
    ops.node(1, 0)
    ops.fix(0, 1)
    ops.mass(1, mass)
    material(1, params_mat, positive_peak, negative_peak, max_d_point, min_d_point)
    ops.element('twoNodeLink', 1, 0, 1, '-mat', 1, '-dir', 1)


def static(disp: np.ndarray) -> tuple:
    ops.timeSeries('Linear', 1)
    ops.pattern('Plain', 1, 1)
    ops.load(1, 1)
    ops.constraints('Plain')
    ops.numberer('Plain')
    ops.system('BandGeneral')
    ops.test('EnergyIncr', 1.0e-6, 20)
    ops.algorithm('Newton')
    Dincr = disp[1:] - disp[:-1]
    Dincr = np.insert(Dincr, 0, disp[0])
    disp_, force_ = [], []
    for incr in Dincr:
        ops.integrator('DisplacementControl', 1, 1, incr)
        ops.analysis('Static')
        ops.analyze(1)
        disp_.append(ops.nodeDisp(1, 1))
        ops.reactions()
        force_.append(ops.nodeReaction(0, 1))
    disp_, force_ = np.array(disp_), np.array(force_)
    force_[np.isnan(force_)] = 0.
    return disp_, force_


def SA_NMsimplex(x0: np.ndarray, object_func: Callable, bounds: list, config: dict = None) -> tuple:
    DA = dual_annealing(object_func, bounds=bounds, no_local_search=True, x0=x0)
    NMsimplex = minimize(object_func, x0=DA['x'], bounds=bounds, method='Nelder-Mead')
    return NMsimplex['x'], NMsimplex['fun']
  

def Hysteretic(matID: int, params: list, positive_peak: list, negative_peak: list, max_d_point: list, min_d_point: list) -> NoReturn:
    ops.uniaxialMaterial('Hysteretic', matID,
                         params[0], params[1],
                         positive_peak[0], positive_peak[1],
                         params[2], params[3],
                         params[4], params[5],
                         negative_peak[0], negative_peak[1],
                         params[6], params[7],
                         params[8], params[9],
                         params[10], params[11],
                         params[12])


def Pinching4(matID: int, params: list, positive_peak: list, negative_peak: list, max_d_point: list, min_d_point: list) -> NoReturn:
    ops.uniaxialMaterial('Pinching4', matID,
                         params[0], params[1],
                         positive_peak[0], positive_peak[1],
                         params[2], params[3],
                         max_d_point[0], max_d_point[1],
                         params[4], params[5],
                         negative_peak[0], negative_peak[1],
                         params[6], params[7],
                         min_d_point[0], min_d_point[1],
                         params[8], params[9],
                         params[10], params[11],
                         params[12], params[13],
                         params[14], params[15],
                         params[16], params[17],
                         params[18],  params[19],
                         params[20], params[21],
                         params[22], params[23],
                         params[24], params[25],
                         params[26], params[27],
                         params[28], params[29],
                         'energy')


class Optimization:
    def __init__(self, disp: np.ndarray, force: np.ndarray, material: str, algorithm: str):
        self.positive_peak = [np.max(force), disp[np.argmax(force)]]
        self.negative_peak = [np.min(force), disp[np.argmin(force)]]
        self.max_d_point = [force[np.argmax(disp)], np.max(disp)]
        self.min_d_point = [force[np.argmin(disp)], np.min(disp)]
        self.disp = disp
        self.force = force
        self.bounds, self.x0, self.mat_model, self.method, self.config = self.__settings(material, algorithm)

    def __settings(self, material: str, algorithm: str) -> tuple:
        bounds, x0, mat_model, method, config = [], [], None, None, {}
        if material == 'Hysteretic':
            bounds = [[0., self.positive_peak[0]],
                      [0.001, self.positive_peak[1] * 0.999],
                      [0., self.positive_peak[0]],
                      [self.positive_peak[1] * 1.001, self.max_d_point[1] * 1.002],
                      [self.negative_peak[0], 0.],
                      [self.negative_peak[1] * 0.999, -0.001],
                      [self.negative_peak[0], 0.],
                      [np.min(self.disp) * 1.002, self.negative_peak[1] * 1.001],
                      [0.001, 1.], [0.001, 1.],
                      [0.001, 1.], [0.001, 1.],
                      [0.001, 1.]]
            x0 = []
            for i in bounds[:8]:
                x0.append((i[1] + i[0]) / 2)
            x0.extend([0.999, 0.999, 0.001, 0.001, 0.001])
            x0 = np.array(x0)
            mat_model = Hysteretic
        if material == 'Pinching4':
            bounds = [[0., self.positive_peak[0]],
                      [0.001, self.positive_peak[1] * 0.999],
                      [self.max_d_point[0], self.positive_peak[0]],
                      [self.positive_peak[1] * 1.001, self.max_d_point[1] * 0.999],
                      [self.negative_peak[0], 0.],
                      [self.negative_peak[1] * 0.999, -0.001],
                      [self.negative_peak[0], self.min_d_point[0]],
                      [self.min_d_point[1] * 0.999, self.negative_peak[1] * 1.001],
                      [0.001, 1.], [0.001, 1.],
                      [0.001, 1.], [0.001, 1.],
                      [0.001, 1.], [0.001, 1.],
                      [0.001, 1.], [0.001, 1.],
                      [0.001, 1.], [0.001, 1.],
                      [0.001, 1.], [0.001, 1.],
                      [0.001, 1.], [0.001, 1.],
                      [0.001, 1.], [0.001, 1.],
                      [0.001, 1.], [0.001, 1.],
                      [0.001, 1.], [0.001, 1.],
                      [0.001, 1.], [1, 100]]
            x0 = []
            for i in bounds[:8]:
                x0.append((i[1] + i[0]) / 2)
            x0.extend([0.5, 0.25, 0.05, 0.5, 0.25, 0.05,
                       1.0, 0.2, 0.3, 0.2, 0.9,
                       0.5, 0.5, 2.0, 2.0, 0.5,
                       1.0, 0.0, 1.0, 1.0, 0.9,
                       10])
            x0 = np.array(x0)
            mat_model = Pinching4

        if algorithm == 'ARO':
            method = aro
            config = {'pop_size': 40, 'epoch': 200}
        if algorithm == 'SA + NM-simplex':
            method = SA_NMsimplex
        return bounds, x0, mat_model, method, config

    def solve(self) -> tuple:
        x, metric = self.method(self.x0, self.__objective, self.bounds, self.config)
        return x, metric

    def simulation(self, x: list) -> tuple:
        SDOF(self.mat_model, x, self.positive_peak, self.negative_peak, self.max_d_point, self.min_d_point, 1)
        disp, force = static(self.disp)
        force = -force
        return disp, force

    def __objective(self, x: list) -> float:
        disp, force = self.simulation(x)
        rmse = np.sqrt(mean_squared_error(self.force, force))
        return rmse


def log(content: str, level: str = 'INFO') -> str:
    host_name = socket.gethostname()
    now = strftime('%Y-%m-%d %H:%M:%S', localtime())
    file_name = Path(sys.argv[0]).name
    stdout = f'[DEVICE:{host_name}][{now}][{file_name}][{level}]: {content}'
    print(stdout)
    return stdout


def sec2hms(sec: int) -> tuple:
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return h, m, s


NT = 1.
mm = 1.
sec = 1.

kN = 1000 * NT
MPa = 1 * NT / mm ** 2
meter = 1000 * mm
mm2 = mm * mm
cm = 10 * mm
kg = NT / (meter / sec ** 2)
gram = kg / 1000
inch = 25.4 * mm
kips = 4.4482216 * kN
GPa = 1000 * MPa
t = 1000 * kg

G = 9.80665 * meter / sec ** 2
density_concrete = 2.4 * gram / cm ** 3


config = read_json('config.json')

path_roof_disp = config['path_project'] + '/static/roof_disp.out'
path_base_reac = config['path_project'] + '/static/base_reac.out'
path_result = Path(config['path_project']) / 'sdof' / 'result.json'
path_sdof = Path(config['path_project']) / 'sdof' / 'sdof.json'
path_eigen = Path(config['path_project']) / 'modal' / 'eigen1_prototype.eig'
path_log = 'log/optimize.log'
length = 1000
np.random.seed(config['random_seed'])
mas1 = 50 * t
mas2 = 50 * t


if __name__ == '__main__':
    with open(path_eigen, 'r') as f:
        for line in f.readlines():
            shape = line.split()
    shape = list(map(float, shape))
    shape1 = shape[1] / shape[2]
    shape2 = 1
    mass_eq = mas1 * shape1 + mas2 * shape2
    factor = mass_eq / (mas1 * shape1 ** 2 + mas2 * shape2 ** 2)
    write_json(path_sdof, {'equivalent mass': mass_eq, 'modal participation factor': factor})

    start = time.time()
    msg_list = [log('Start optimizing.')]

    disp = readOSresult(path_roof_disp, ['disp'])['disp'].values
    base_reac = readOSresult(path_base_reac, ['1', '2', '3', '4', '5', '6'])
    force = base_reac.sum(axis=1).values
    force = -force

    disp_, force_ = disp / factor, force / factor
    optimization = Optimization(disp_, force_, 'Hysteretic', 'ARO')
    x, rmse = optimization.solve()

    end = time.time()
    h, m, s = sec2hms(int(end - start))
    msg_list.append(log(f'Finish in {h}h {m}m {s}s.'))
    write_json(path_result, {'x': list(x), 'rmse': rmse})
    log2file(msg_list, path_log)
