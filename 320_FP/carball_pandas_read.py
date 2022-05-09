import numpy as np
import pandas as pd
import struct, io

# https://github.com/SaltieRL/carball/blob/master/carball/analysis/utils/numpy_manager.py#L40
def get_array(file, chunk):
  """
  Gets a compressed numpy array from a file.
  Throws an EOFError if it has problems loading the data.
  :param file: The file that is being read
  :param chunk: A chunk representing a single number, this will be the number of bytes the array takes up.
  :return: A numpy array
  """
  try:
    starting_byte = struct.unpack('i', chunk)[0]
  except struct.error:
    raise EOFError('Struct error')
  numpy_bytes = file.read(starting_byte)
  fake_file = io.BytesIO(numpy_bytes)
  try:
    # explicitly allow pickle loading. thanks numpy for changing this without telling anyone
    result = np.load(fake_file, fix_imports=False, allow_pickle=True)
  except OSError:
    raise EOFError('NumPy parsing error')
  return result, starting_byte

# https://github.com/SaltieRL/carball/blob/master/carball/analysis/utils/numpy_manager.py#L34
def read_array_from_file(file):
  chunk = file.read(4)
  numpy_array, num_bytes = get_array(file, chunk)
  return numpy_array

# https://github.com/SaltieRL/carball/blob/master/carball/analysis/utils/pandas_manager.py#L39
def read_numpy_from_memory(buffer):
  array = read_array_from_file(buffer)
  dataframe = pd.DataFrame.from_records(array)
  dataframe.set_index('index', drop=True, inplace=True)
  columns = []
  for tuple_str in dataframe.columns.values:
    columns.append(eval(tuple_str))
  dataframe.columns = pd.MultiIndex.from_tuples(columns)
  return dataframe