# ----- richiama il codice che crea tutte le matrici di input con le rispettive permutazioni

from pathlib import Path
from Test_function_26_08_2026 import main

yymmdd = '240813'
cell = 'cell0001'
main_matrix_ids = []
date_str = ('30_08_2026')

for i in range(4,11):
    id_str  = str(i)
    main_matrix_id = 'M' + id_str
    main_matrix_ids.append(main_matrix_id)
    main_matrix_path = Path("D:/") / ('inputs') / f"{yymmdd}_{cell}_{main_matrix_id}_input_matrix"

    exp_data_path = ("D:/test_save_old/" + yymmdd + "_" + cell + "_morph_and_spines.h5")

    # ----- quando si fa il sanity check
    # exp_data_path = f"D:/test_save/{yymmdd}_{cell}_morph_and_spines_permutation_seed_23.h5"  # file con info su riassegnazione spine // per come e' scritto adesso il codice parte da indice 1

    main(main_matrix_id,
         'BLA',
         'CA3',
         date_str,
         main_matrix_path,
         exp_data_path)