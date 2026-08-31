
'''
   Run delle simulazioni con le riassegnazioni delle spine BLA e CA3 simulate
'''
import subprocess
import time
from datetime import datetime
# main_matrix_ids = ['M3'] # ,'mm4', 'mm5', 'mm6', 'mm7']
spine_types = ['BLA', 'CA3']
main_matrix_ids = []

date_str = '30_08_2026'

# ---- qui creo le label delle main matrix
for i in range(4,11):
    id_str = str(i)
    if i == 3:
        continue
    main_matrix_id = 'M' + str(i)
    main_matrix_ids.append(main_matrix_id)


script = 'Run_model_25_08_2026.py'

# run delle simulazioni prendendo le matrici create in precedenza
start_time = time.perf_counter()
print('orario inizio script:', datetime.now())
for mm_id in main_matrix_ids:

    for spine_type in spine_types:
        print(f"Avvio {script} con main_matrix_id = {mm_id} e spine_type {spine_type}")
        subprocess.run(
        ["python", script, "--main_matrix_id", mm_id, "--spine_type", spine_type, "--date_str", date_str],
        check=True
    )
    end_time = time.perf_counter()
    print('orario fine script:', datetime.now())
    print(f"Terminato {script} con main_matrix_id = {mm_id}\n e spine_type = {spine_type}")

    durata_sec = end_time - start_time
    minuti, secondi = divmod(durata_sec, 60)
    ore, minuti = divmod(minuti, 60)
    print(f"Durata: {int(ore)}h {int(minuti)}m {secondi:.2f}s (totale: {durata_sec:.2f} s)")

