
import os
import typing

import pandas as pd


_file_path = "brain_networks.csv"
_dir_path = os.path.dirname(os.path.realpath(__file__))
_path = os.path.join(_dir_path, _file_path)

# public variable
brain_data = pd.read_csv(_path)
