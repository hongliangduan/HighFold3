**Accurate structure prediction of cyclic peptides containing unnatural amino acids using HighFold3**

<img width="804" height="299" alt="image" src="https://github.com/user-attachments/assets/42c44b13-f929-4082-9460-fcb86c415301" />

HighFold3 is an enhanced model developed on the basis of AlphaFold 3, designed to accurately predict the three-dimensional structures of peptides containing unnatural amino acids (unAAs), including both monomers and their protein complexes. It is capable of handling special topological features such as head-to-tail cyclization and disulfide bond constraints. The overall architecture of HighFold3 is illustrated in Figure . HighFold3 introduces the Cyclic Position Offset Encoding Matrix (CycPOEM) and employs an innovatively designed “Cyclization Switch” module to dynamically select either a linear or cyclic positional encoding matrix within the model.
When predicting cyclic peptide–protein complexes, the model explicitly divides the input distance matrix into two components: a linear positional encoding matrix for the target protein and a CycPOEM for the cyclic peptide ligand. This design enables the model to flexibly accommodate diverse conformational requirements and accurately model the binding of cyclic peptide ligands to protein receptors.

<img width="864" height="605" alt="image" src="https://github.com/user-attachments/assets/bef5e705-4215-45e8-9cce-884e2baba0c7" />

**Model Architecture and Innovations:**

HighFold3 is built upon the AlphaFold 3 framework, which is renowned for its accuracy in biomolecular structure prediction. The model introduces two key innovations:

Cyclic Position Offset Encoding Matrix (CycPOEM): This matrix adjusts positional encoding to account for the closed-loop structure of cyclic peptides, ensuring accurate representation of their topology.
Cyclization Switch Module: This module dynamically selects between linear and cyclic positional encoding matrices, allowing flexibility in modeling diverse peptide conformations.

The architecture includes two sub-models: HighFold3-Linear for linear peptides and HighFold3-Cyclic for cyclic peptides, enabling tailored predictions based on peptide type.

**Installation :**
Refer to the conda version of AlphaFold3 installation, and replace the feature files by highfold3/model.

**Usage :**

db_dir=af3_db_path

--model_dir=models_path

--json_path=json_path

--output_dir=output_path

--head_to_tail = 0   # or = 1

--disulfide_chain_res [[1,3,11]] # [[chain 1, Cys3, Cys11]]


**Description :**

1.	The parameter head_to_tail indicates whether the head and tail form a ring, a boolean type.
2.	The parameter disulfide_chain_res specifies the chain and positions where disulfide bonds are located.

