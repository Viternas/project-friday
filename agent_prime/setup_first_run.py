from build_utils.encode_config_json import JsonFormatter
from build_utils.create_config_class import CreateConfigClass
import os

def setup_first_run():
    ec = JsonFormatter(package_dir=os.path.dirname(__file__), config_file='unencoded_config_main.json', encode=True)
    cc = CreateConfigClass(package_dir=os.path.dirname(__file__), config_file_name='config_main_encoded.json').create_config_class()


if __name__ == '__main__':
    setup_first_run()