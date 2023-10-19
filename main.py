from config import config
from ssh import MyCmd
import pandas as pd
import os


def server_result(conn, host):
    # 统计信息字典
    server_dict = {"name": conn.server_name(),
                   "host": host,
                   "cpu_number": conn.server_cpu_number(),
                   "cpu": conn.server_cpu(),
                   "cpu_load": conn.server_cpu_load(),
                   "mem": conn.server_mem(),
                   "disk": conn.server_disk(),
                   "disk_io": conn.server_disk_io(),
                   "process_number": conn.server_process_number(),
                   "network": conn.server_network()
                   }
    conn.close_conn()
    return server_dict


def print_execl(arrs, path):
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


def main():
    script_path = os.path.abspath(__file__)
    exec_path = os.path.dirname(script_path)
    path = f"{exec_path}/config/hosts"
    conf = config.Config(path)
    host_key, host_val = conf.obtain_arr()

    server_info = []

    for host in host_key:
        port = host_val[f'{host}_ssh_port']
        username = host_val[f'{host}_ssh_user']
        passwd = host_val[f'{host}_ssh_rsa']
        authenticationkey = host_val[f'{host}_ssh_authentication']
        authentication = {
            'type': authenticationkey,
            'passwd': passwd
        }

        for host in host_val[f'{host}_host']:
            try:
                print(host)
                conn = MyCmd.MyCmd(
                    host=host,
                    user=username,
                    port=port,
                    authentication=authentication
                )
                server_info.append(server_result(conn, host))
            except Exception as e:
                print(f'host is err: {e},Skip this time')
                continue
    print_execl(server_info, exec_path)


if __name__ == "__main__":
    main()
