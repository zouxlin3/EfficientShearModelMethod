from PythonBase.IO import log2file
from PythonBase.Basic import log
import subprocess


path_log = 'Logs.txt'

if __name__ == '__main__':
    msg_list = []
    command = f'opensees MainModal.tcl'
    msg_list.append(log('Start modal analysis'))
    ret = subprocess.run(command, stderr=subprocess.PIPE, shell=True, cwd='./')
    stderr = str(ret.stderr)
    if 'Successfully Finished!' in stderr:
        msg_list.append(log('Finish modal analysis'))
    else:
        msg_list.append(log('Failed when modal analysis', 'ERROR'))
        msg_list.append(log('Stderr: ' + stderr.split('\\r\\n')[-3], 'ERROR'))
    log2file(msg_list, path_log)
