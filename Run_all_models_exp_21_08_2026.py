'''
questo fa il run di Run_model_exp_assign_21_08_2026.py in parallelo, per le diverse main_matrix
e per i casi BLA e CA3
Il codice di cui viene fatto il run è il codice principale
dove all'interno si prende la matrice main, si fanno le permutazioni in base alle spine
e si usa per le simulazioni
'''
import subprocess
from pathlib import Path


spine_types = ['BLA', 'CA3']
main_matrix_ids = []
date_str = '30_08_2026'
date_strs = []
for i in range(4,11):
    id_str = str(i)
    if i == 3:
        continue
    main_matrix_id = 'M' + str(i)
    main_matrix_ids.append(main_matrix_id)
    date_strs.append(date_str)
yymmdd = '240813';
cell = 'cell0001'


''' 1. '''
# ----- dataset con assegnazione spine sperimentali
data_path = ("D:/test_save_old/" + yymmdd + "_" + cell + "_morph_and_spines.h5")

''' 2. '''
# ----- dataset con assegnazione spine simulata ---> serve per il SanityCheck
#data_path = f"D:/test_save/{yymmdd}_{cell}_morph_and_spines_permutation_seed_23.h5"
# file con info su riassegnazione spine // per come e' scritto adesso il codice parte da indice 1

for mm_id in main_matrix_ids:
    for sp_type in spine_types:
        print(f"Avvio con main_matrix_id={mm_id}, spine_type={sp_type}")
        subprocess.run(
            # ["python", "Run_model_exp_sanity_check_26_08_2026.py",
            ["python", "Run_model_exp_assign_21_08_2026.py",
             "--main_matrix_id", mm_id,
             "--spine_type", sp_type,
             "--date_str", date_str,
             "--data_path", data_path],
            check=True
        )
        print(f"Terminato main_matrix_id={mm_id}, spine_type={sp_type}\n")