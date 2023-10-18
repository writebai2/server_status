import pandas as pd
from collections import OrderedDict

arrs = [
    OrderedDict(
        [('name', 'gearman02'),
         ('address', '107.170.74.34'),
         ('cpu_number', '2'),
         ('cpu', {'sys': '0', 'idea': '96', 'us': '3'}),
         ('cpu_load', {'5avg': '0.07', '15avg': '0.03', '1avg': '0.01'}),
         ('mem', {'mem_total': 3.86, 'mem_free': 1.11, 'percentage': '65.8%'}),
         ('disk', {'/': {'disk_free': 31.29, 'percentage': '17%', 'disk_total': 39.25}}),
         ('disk_io', '0'),
         ('process_number', 150),
         ('network', '200')])
]


def print_execl(arrs):
    df = pd.json_normalize(arrs)

    # 创建二级标题
    df.columns = pd.MultiIndex.from_tuples([
        ('Basic', 'name'),
        ('Basic', 'address'),
        ('CPU', 'cpu_number'),
        ('Disk IO', 'disk_io'),
        ('Process Number', 'process_number'),
        ('Network', 'network'),
        ('CPU', 'cpu_us'),
        ('CPU', 'cpu_sys'),
        ('CPU', 'cpu_idea'),
        ('CPU Load', '1avg'),
        ('CPU Load', '5avg'),
        ('CPU Load', '15avg'),
        ('Memory', 'mem_total'),
        ('Memory', 'mem_free'),
        ('Memory', 'percentage'),
        ('/', 'disk_total'),
        ('/', 'disk_free'),
        ('/', 'percentage'),
    ])
    df.to_excel("主机巡检_额外.xlsx")


if __name__ == "__main__":
    for val in arrs:
        print(dict(val))
    # print_execl(arrs)
