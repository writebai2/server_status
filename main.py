from ssh import MySSH
from config import config
import pandas as pd


def server_result(ssh: MySSH.MySSH, address):
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


def print_execl(arrs):
    df = pd.json_normalize(arrs)

    # 创建二级标题
    df.columns = pd.MultiIndex.from_tuples([
        ('Basic', 'name'),
        ('Basic', 'address'),
        ('CPU', '核数'),
        ('Disk IO', '磁盘io'),
        ('进程数', 'process_number'),
        ('Network', 'network'),
        ('CPU', 'cpu_us'),
        ('CPU', 'cpu_sys'),
        ('CPU', 'cpu_idea'),
        ('CPU Load', '1avg'),
        ('CPU Load', '5avg'),
        ('CPU Load', '15avg'),
        ('内存', '总内存(G)'),
        ('内存', '空闲'),
        ('内存', '使用率'),
        ('/目录', '总空间(G)'),
        ('/目录', '空闲'),
        ('/目录', '使用率'),
    ])
    df.to_excel("主机巡检.xlsx")


def test_host():
    path = "/develop/python/server_status/config/hosts"
    conf = config.Config(path)
    host_key, host_val = conf.obtain_arr()

    server_info = []

    for host in host_key:
        port = host_val[f'{host}_ssh_port']
        username = host_val[f'{host}_ssh_user']
        pkey = host_val[f'{host}_ssh_rsa']

        for address in host_val[f'{host}_host']:
            print(address)
            ssh = MySSH.MySSH(address,
                              username,
                              pkey,
                              port)
            bol = ssh.Init()
            if not bol:
                print(f'{address} 检测失败，请手动检测')
                continue
            result = server_result(ssh, address)
            server_info.append(result)
            ssh.ClostSSH()
    print_execl(server_info)


def main():
    test_host()


if __name__ == "__main__":
    main()
