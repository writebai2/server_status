import configparser


class Config():
    """docstring for Config."""

    def __init__(self, path):
        self.path = path

    def obtain_arr(self):
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(self.path)
        host_key = []
        host_val = {}
        for name in config.sections():
            key = name.split(":")[0]
            if key not in host_key:
                host_key.append(key)
            match ":" in name:
                case True:
                    for val in config.items(name):
                        host_val[f'{key}_{val[0]}'] = val[1]
                case False:
                    tmp_arr = []
                    for val in config.options(name):
                        tmp_arr.append(val)
                    host_val[f"{name}_host"] = tmp_arr
        return host_key, host_val
