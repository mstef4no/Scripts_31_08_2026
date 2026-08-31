
# Run di crea matrici

from crea_main_matrix import build_main_matrix
from pathlib import Path
yymmdd = '240813'
cell = 'cell0001'
main_matrix_ids = []

for i in range(10,11):
    id_str  = str(i)
    main_matrix_id = 'M' + id_str
    main_matrix_ids.append(main_matrix_id)
    output_folder = Path("D:/") / ('inputs') / f"{yymmdd}_{cell}_{main_matrix_id}_input_matrix"

    build_main_matrix(yymmdd, cell, output_folder)

