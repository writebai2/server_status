from thread import Thread
from config import config
from myssh import myssh
import pandas as pd


def print_execl(arrs, path):
    try:
        df = pd.json_normalize(arrs)
        # 创建二级标题
        df.columns = pd.MultiIndex.from_tuples([
            ('Basic', 'name'),
            ('Basic', 'host'),
            ('CPU', '核数'),
            ('Disk IO', '磁盘io'),
            ('进程数', 'process_number'),
            ('Network', '状态码'),
            ('CPU', 'cpu_us'),
            ('CPU', 'cpu_sys'),
            ('CPU', 'cpu_idea'),
            ('CPU Load', '1avg'),
            ('CPU Load', '5avg'),
            ('CPU Load', '15avg'),
            ('内存', '总内存'),
            ('内存', '空闲'),
            ('内存', '使用率'),
            ('/目录', '总空间'),
            ('/目录', '空闲'),
            ('/目录', '使用率'),
        ])
        df.to_excel(f"{path}/主机巡检.xlsx")
    except Exception as e:
        print(f'TO_ECEL ERROR,err: {e}')


def server_result(ssh: myssh.MyCmd, address):
    # 统计信息字典
    server_dict = {"name": ssh.server_name(),
                   "address": address,
                   "cpu_number": ssh.server_cpu_number(),
                   "cpu": ssh.server_cpu(),
                   "cpu_load": ssh.server_cpu_load(),
                   "mem": ssh.server_mem(),
                   "disk": ssh.server_disk(),
                   "disk_io": ssh.server_disk_io(),
                   "process_number": ssh.server_process_number(),
                   "network": ssh.server_network()
                   }
    return server_dict


def get_result(address, username, port, authentication):
    try:
        ssh = myssh.MyCmd(
            host=address,
            user=username,
            port=port,
            authentication=authentication
        )
        result = server_result(ssh, address)
        ssh.close_conn()
        return result
    except Exception as e:
        print(f'CONN ERROR,HOST: {address},err: {e}')


def pust_host():
    # 创建一个线程池
    pool = Thread.ThreadPool(60, 100)

    path = "./config/hosts"
    conf = config.Config(path)
    host_key, host_val = conf.obtain_arr()
    for host in host_key:
        try:
            port = host_val[f'{host}_ssh_port']
            username = host_val[f'{host}_ssh_user']
            passwd = host_val[f'{host}_ssh_rsa']
            authenticationkey = host_val[f'{host}_ssh_authentication']
            authentication = {
                'type': authenticationkey,
                'passwd': passwd
            }

            for address in host_val[f'{host}_host']:
                # 添加任务到线程池
                pool.add_task(
                    (get_result, address, username, port, authentication))
        except Exception as e:
            print(f"READ CONFIGURATION ERROR,HOST:{host}，err: {e}")
            continue

    # 等待所有任务完成
    pool.wait()
    # 获取所有任务的结果
    results = pool.get_results()
    print_execl(results, '.')


if __name__ == "__main__":
    pust_host()
