import numpy as np
from numpy import ndarray


#def calc_cyclic_matrix_af3(residue_index,
#                           head_to_tail: bool = False,
#                           list_cid_ss: list[list[int]] = [],
#                           token_wise=True,
#                           signal_bug_fix=True, ):
#  # m = np.arange(len(residue_index))
#  # offset = m[:, None] - m[None, :]
#  # mn = np.stack([m, m + len(residue_index)], -1)
#  # c_offset = np.abs(mn[:, None, :, None] - mn[None, :, None, :]).min((2, 3))
#  # if signal_bug_fix:
#  #   a = c_offset < np.abs(offset)
#  #   c_offset[a] = -c_offset[a]
#  # final_offset = c_offset * np.sign(offset)
#  # return final_offset  
#  if not head_to_tail and (list_cid_ss is None or list_cid_ss == [] or list_cid_ss == [[]]):
#    return [[0]]
#  index_residue_1 = np.where(residue_index == 1)[0]
#  index_cid = 0
#  for i in range(len(list_cid_ss)):
#    if list_cid_ss[i][0] > index_cid:
#      index_cid = list_cid_ss[i][0]
#  if index_cid == 0:
#    return [[0]]
#  if len(index_residue_1) < index_cid:
#    print('error input chain id in disulfide bridges information')
#    return [[0]]
#  m = np.arange(len(residue_index))
#  if index_cid < len(index_residue_1):
#    m = np.arange(index_residue_1[index_cid])
#  if not token_wise:
#    m = residue_index[:len(m)]
#  offset = m[:, None] - m[None, :]
#  for i in range(len(list_cid_ss)):
#    index_cid_ss = list_cid_ss[i]
#    res_index_0 = index_residue_1[index_cid_ss[0] - 1]
#    n_res = index_residue_1[index_cid_ss[0]] if len(index_residue_1) > index_cid_ss[0] else len(residue_index)
#    n_res -= res_index_0
#    c1 = [ind - 1 for ind in index_cid_ss[1::2]]
#    c2 = [ind - 1 for ind in index_cid_ss[2::2]]
#    matrix = calc_cyclic_matrix_monomer(n_res, c1, c2, head_to_tail=head_to_tail)
#    offset[res_index_0:res_index_0 + n_res, res_index_0:res_index_0 + n_res] = matrix
#  # print(offset)
#  return offset  

def calc_cyclic_matrix_af3(residue_index,
                           head_to_tail: bool = False,
                           list_cid_ss: list[list[int]] = [],
                           token_wise=True,
                           signal_bug_fix=True):
  if not head_to_tail and (list_cid_ss is None or list_cid_ss == [] or list_cid_ss == [[]]):
    return [[0]]
  if len(list_cid_ss) > 1:
    return [[0]]
  index_residue_1 = np.where(residue_index == 1)[0]
  n_res = index_residue_1[1] if len(index_residue_1) > 1 else len(residue_index)
  # m = np.arange(len(n_res))
  # offset = m[:, None] - m[None, :]
  c1 = []
  c2 = []
  if len(list_cid_ss) > 0:
    c1 = [ind - 1 for ind in list_cid_ss[0][1::2]]
    c2 = [ind - 1 for ind in list_cid_ss[0][2::2]]
  offset = calc_cyclic_matrix_monomer(n_res, c1, c2, head_to_tail=head_to_tail)
  return offset

def calc_cyclic_matrix_monomer(n_aa, c1, c2, head_to_tail=False):
  """
  :param n_aa: number of amino acid residues
  :param c1: list of Cys residues
  :param c2: list of the corresponding Cys residues to c1, the same length with c1
  :param head_to_tail:
  :return:
  """
  if len(c1) != len(c2):
    return []  
  # init adjacency matrix
  matrix = np.zeros((n_aa, n_aa)) + n_aa
  for i in range(n_aa):
    matrix[i][i] = 0  
  # linear peptide connection
  for i in range(n_aa - 1):
    matrix[i][i + 1] = 1
    matrix[i + 1][i] = 1  
  # nc connection
  if head_to_tail:
    matrix[0][n_aa - 1] = 1
    matrix[n_aa - 1][0] = 1  
  # ss connection
  for i in range(len(c1)):
    matrix[c1[i]][c2[i]] = 1
    matrix[c2[i]][c1[i]] = 1  
  # get the shortest path
  matrix = calc_shortest_path(matrix)  
  for i in range(matrix.shape[0]):
    for j in range(i + 1, matrix.shape[0], 1):
      matrix[i][j] *= -1  
  return matrix


def calc_shortest_path(matrix):
  """
  Floyd algorithm to find the shortest path
  :param matrix:
  :return:
  """
  path = np.zeros_like(matrix)
  for i in range(matrix.shape[0]):
    path[i] = [j for j in range(matrix.shape[0])]
  # print(path)
  # print()
  # print(matrix)  
  for m in range(matrix.shape[0]):
    for i in range(matrix.shape[0]):
      for j in range(matrix.shape[0]):
        if matrix[i][m] + matrix[m][j] < matrix[i][j]:
          matrix[i][j] = matrix[i][m] + matrix[m][j]
          path[i][j] = m
  # print()
  # print(path)
  # print()
  # print(matrix)  
  return matrix


def construct_cyclic_offset_matrix_v20250306(n_res, signal_bug_fix=True,):
  i = np.arange(n_res)
  offset = i[:, None] - i[None, :]
  ij = np.stack([i, i + n_res], -1)
  c_offset = np.abs(ij[:, None, :, None] - ij[None, :, None, :]).min((2, 3))
  if signal_bug_fix:
    a = c_offset < np.abs(offset)
    c_offset[a] = -c_offset[a]
  final_offset = c_offset * np.sign(offset)
  return final_offset

