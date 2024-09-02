from PythonBase.IO import read_json
from typing import NoReturn


def genTcl(ESDOF: list, content: list, height: list) -> NoReturn:
    s1p, e1p, s2p, e2p, s3p, e3p = [], [], [], [], [], []
    s1n, e1n, s2n, e2n, s3n, e3n = [], [], [], [], [], []
    pinchX, pinchY, damage1, damage2, beta, mass = [], [], [], [], [], []
    for i in ESDOF:
        s1p.append(i['x'][0])
        e1p.append(i['x'][1])
        s2p.append(i['positive_peak'][0])
        e2p.append(i['positive_peak'][1])
        s3p.append(i['x'][2])
        e3p.append(i['x'][3])
        s1n.append(i['x'][4])
        e1n.append(i['x'][5])
        s2n.append(i['negative_peak'][0])
        e2n.append(i['negative_peak'][1])
        s3n.append(i['x'][6])
        e3n.append(i['x'][7])
        pinchX.append(i['x'][8])
        pinchY.append(i['x'][9])
        damage1.append(i['x'][10])
        damage2.append(i['x'][11])
        beta.append(i['x'][12])
        mass.append(i['mass'])
    content[3][2] = '9;'
    content[6][2] = f'{{{str(mass)[1:-1].replace(",", "")}}}'
    content[7][2] = f'{{{str(s1p)[1:-1].replace(",", "")}}}'
    content[8][2] = f'{{{str(e1p)[1:-1].replace(",", "")}}}'
    content[9][2] = f'{{{str(s2p)[1:-1].replace(",", "")}}}'
    content[10][2] = f'{{{str(e2p)[1:-1].replace(",", "")}}}'
    content[11][2] = f'{{{str(s3p)[1:-1].replace(",", "")}}}'
    content[12][2] = f'{{{str(e3p)[1:-1].replace(",", "")}}}'
    content[13][2] = f'{{{str(s1n)[1:-1].replace(",", "")}}}'
    content[14][2] = f'{{{str(e1n)[1:-1].replace(",", "")}}}'
    content[15][2] = f'{{{str(s2n)[1:-1].replace(",", "")}}}'
    content[16][2] = f'{{{str(e2n)[1:-1].replace(",", "")}}}'
    content[17][2] = f'{{{str(s3n)[1:-1].replace(",", "")}}}'
    content[18][2] = f'{{{str(e3n)[1:-1].replace(",", "")}}}'
    content[19][2] = f'{{{str(pinchX)[1:-1].replace(",", "")}}}'
    content[20][2] = f'{{{str(pinchY)[1:-1].replace(",", "")}}}'
    content[21][2] = f'{{{str(damage1)[1:-1].replace(",", "")}}}'
    content[22][2] = f'{{{str(damage2)[1:-1].replace(",", "")}}}'
    content[23][2] = f'{{{str(beta)[1:-1].replace(",", "")}}}'
    content[24][2] = f'{{{str(height)[1:-1].replace(",", "")}}}'
    with open('MainShearModelDyn.tcl', 'w') as f:
        for line in content:
            f.writelines(' '.join(line))
            f.write('\n')
            f.flush()


if __name__ == '__main__':
    ESDOF1 = read_json('F:/data_RSRP/SteelFrame/ShearModel/floor1.json')
    ESDOF2 = read_json('F:/data_RSRP/SteelFrame/ShearModel/floor2.json')
    ESDOF3 = read_json('F:/data_RSRP/SteelFrame/ShearModel/floor3.json')
    ESDOF4 = read_json('F:/data_RSRP/SteelFrame/ShearModel/floor4.json')
    ESDOF5 = read_json('F:/data_RSRP/SteelFrame/ShearModel/floor5.json')
    ESDOF6 = read_json('F:/data_RSRP/SteelFrame/ShearModel/floor6.json')
    ESDOF7 = read_json('F:/data_RSRP/SteelFrame/ShearModel/floor7.json')
    ESDOF8 = read_json('F:/data_RSRP/SteelFrame/ShearModel/floor8.json')
    ESDOF9 = read_json('F:/data_RSRP/SteelFrame/ShearModel/floor9.json')
    content = []
    heighti = [5486.4] + [3962.4] * 8
    height, summ = [], 0
    for i in range(9):
        summ = summ + heighti[i]
        height.append(summ)
    with open('MainShearModelDynTemp.tcl', 'r') as f:
        for line in f.readlines():
            content.append(line.split())
    genTcl([ESDOF1, ESDOF2, ESDOF3, ESDOF4, ESDOF5, ESDOF6, ESDOF7, ESDOF8, ESDOF9], content, height)
