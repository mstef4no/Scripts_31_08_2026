'''
    Codice fatto dopo riunione del 26/08/2026
'''

# ----- importare librerie
import flammkuchen as fl
import numpy as np
from pathlib import Path
from datetime import datetime


""" 
Ritorna gli indici spine attivate e spine non attivate da un dataframe di spine. >>> Restituisce degli array numpy che contengono gli indici delle spine attivate e non attivate 
"""
def get_activated_spine_idx(spines_df, spine_type_condition):
    activated_spine_idx = spines_df.index[spines_df[spine_type_condition] == True].to_numpy()
    non_activated_spine_idx = spines_df.index[spines_df[spine_type_condition] == False].to_numpy()
    return activated_spine_idx, non_activated_spine_idx




# ----- inizio codice
def main(main_matrix_id, BLA_type, CA3_type, date_str, main_matrix_path, exp_data_path):
    yymmdd = '240813';
    cell = 'cell0001'
    spine_type_BLA = 'is_' + BLA_type
    spine_type_CA3 = 'is_' + CA3_type
    print('inizio creazione matrici', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))


    ''' MATRICE DI INPUT CON ELEMENTI IN FORMATO UINT8 '''
    X_exc_path = Path(main_matrix_path)/('sim_0000000.npy')


    # se uso il modo di salvare in uint8 devo fare la conversione in float64 prima di usarla
    X_min = 0.0
    X_max = 0.0007
    X_exc_uint8 = np.load(X_exc_path)

    X_conv = X_exc_uint8.astype(np.float64) / 255.0 * (X_max - X_min) + X_min
    X_exc = np.round(X_conv,5)

    for loop_numb in range(0,21):
        if (loop_numb == 0):
            # ----- carico il dataset speriment
            # +++++
            # +++++ quando devo fare il sanity check basta cambiare il path di questo file, e usarne uno di quelli simulati +++++
            # +++++


            exp_dataset = fl.load(exp_data_path)

            # ----- cartele di output del caso con assegnazioni sperimentali delle spine
            output_folder_BLA = Path("D:/") / f"{yymmdd}_{cell}_{BLA_type}_{main_matrix_id}_{date_str}_experiment"
            inputs_folder_BLA = output_folder_BLA / "inputs"
            inputs_folder_BLA.mkdir(parents=True, exist_ok=True)

            # ----- cartella di output
            output_folder_CA3 = Path("D:/") / f"{yymmdd}_{cell}_{CA3_type}_{main_matrix_id}_{date_str}_experiment"
            inputs_folder_CA3 = output_folder_CA3 / "inputs"
            inputs_folder_CA3.mkdir(parents=True, exist_ok=True)

        else:

            # --- dataset sperimentale di riferimento ---
            # carica il dataset e vede quali sono le spine attivate
            # ----- QUESTO MI SERVE PER FARE IN MODO CHE LE RIGHE DELLA MATRICE CHE CORRISPONDONO A SPINE DI TIPO BLA (CA3) VENGANO ASSOCIATE A SPINE BLA (CA3) ANCHE
            # ----- QUANDO SI USANO GLI ALTRI DATASETS



            exp_dataset = fl.load(exp_data_path)



            dataset_ind = int(loop_numb-1) # in questo modo prendo i dataset con indice del seed che va da 0 a 19
            # quindi sotto devo cambiare in dataset_ind



            # qua ricordarsi che i dataset li prende da quando loop_numb == 1 perche' lo 0 lo prende per il caso del dataset sperimentale
            # ----- carico il dataset con riassegnazione
            sim_data_path = f"D:/test_save/{yymmdd}_{cell}_morph_and_spines_permutation_seed_{dataset_ind}.h5"
            # file con info su riassegnazione spine // per come e' scritto adesso il codice parte da indice 1
            sim_dataset = fl.load(sim_data_path)

            # --- percorso delle cartelle di output dei casi con riassegnazione ---
            # in questa cartelle si salvano le matrici che vengono create con le permutazioni
            output_folder_BLA = Path("D:/") / f"{yymmdd}_{cell}_{BLA_type}_{main_matrix_id}_{date_str}"
            inputs_folder_BLA = output_folder_BLA / "inputs"
            inputs_folder_BLA.mkdir(parents=True, exist_ok=True)

            output_folder_CA3 = Path("D:/") / f"{yymmdd}_{cell}_{CA3_type}_{main_matrix_id}_{date_str}"
            inputs_folder_CA3 = output_folder_CA3 / "inputs"
            inputs_folder_CA3.mkdir(parents=True, exist_ok=True)

            BLA_activated_spine_idx_sim, BLA_non_activated_spine_idx_sim = get_activated_spine_idx(
                sim_dataset['spines_df'], spine_type_BLA)
            CA3_activated_spine_idx_sim, CA3_non_activated_spine_idx_sim = get_activated_spine_idx(
                sim_dataset['spines_df'], spine_type_CA3)




        # ----- qui metto tutte le operazioni che sono indipendenti
        # ----- dall'indice del loop

        # ----- trova quali sono le spine attivate da BLA e da CA3 nel dataset che e' stato considereato
        BLA_activated_spine_idx_exp, BLA_non_activated_spine_idx_exp = get_activated_spine_idx(
            exp_dataset['spines_df'], spine_type_BLA)

        CA3_activated_spine_idx_exp, CA3_non_activated_spine_idx_exp = get_activated_spine_idx(
            exp_dataset['spines_df'], spine_type_CA3)



        for perm_ind in range(0,50):

            rng = np.random.default_rng(seed=loop_numb*50 +perm_ind) # se metto solo perm ind ogni 20, loop ind fa permutazioni uguali
            X_aus = X_exc.copy()

            # ----- MATRICI VUOTE -----
            X_aus_BLA = np.zeros_like(X_exc)
            X_aus_CA3 = np.zeros_like(X_exc)

            BLA_ordine_activated_spine = rng.permutation(len(BLA_activated_spine_idx_exp))
            BLA_ordine_non_activated_spine = rng.permutation(len(BLA_non_activated_spine_idx_exp))
            CA3_ordine_activated_spine = rng.permutation(len(CA3_activated_spine_idx_exp))
            CA3_ordine_non_activated_spine = rng.permutation(len(CA3_non_activated_spine_idx_exp))

            if perm_ind == 0:
                if loop_numb == 0:


                    # vedere se va bene cosi' o se devo associare come ho fatto sotto
                    X_aus_BLA[BLA_activated_spine_idx_exp] = X_exc[BLA_activated_spine_idx_exp]
                    X_aus_BLA[BLA_non_activated_spine_idx_exp] = X_exc[BLA_non_activated_spine_idx_exp]

                    X_aus_CA3[CA3_activated_spine_idx_exp] = X_exc[CA3_activated_spine_idx_exp]
                    X_aus_CA3[CA3_non_activated_spine_idx_exp] = X_exc[CA3_non_activated_spine_idx_exp]

                    # ----- queste si potevano fare anche usando
                    # ----- X_aus_BLA = X_exc.copy()
                    # ----- X_aus_CA3 = X_exc.copy()
                    # ----- PENSO CHE VA BENE COME HO FATTO, SIA IL MODO SCRITTO SOPRA CHE QUELLO COMMENTATO DOVREBBERO ESSERE LA STESSA COSA
                else:
                    X_aus_BLA[BLA_activated_spine_idx_sim] = X_exc[BLA_activated_spine_idx_exp]
                    X_aus_BLA[BLA_non_activated_spine_idx_sim] = X_exc[BLA_non_activated_spine_idx_exp]

                    X_aus_CA3[CA3_activated_spine_idx_sim] = X_exc[CA3_activated_spine_idx_exp]
                    X_aus_CA3[CA3_non_activated_spine_idx_sim] = X_exc[CA3_non_activated_spine_idx_exp]


            else:

                if loop_numb == 0:
                    X_aus_BLA[BLA_activated_spine_idx_exp] = X_exc[BLA_activated_spine_idx_exp[BLA_ordine_activated_spine]]
                    X_aus_BLA[BLA_non_activated_spine_idx_exp] =X_exc[
                    BLA_non_activated_spine_idx_exp[BLA_ordine_non_activated_spine]]

                    X_aus_CA3[CA3_activated_spine_idx_exp] = X_exc[CA3_activated_spine_idx_exp[CA3_ordine_activated_spine]]
                    X_aus_CA3[CA3_non_activated_spine_idx_exp] = X_exc[
                    CA3_non_activated_spine_idx_exp[CA3_ordine_non_activated_spine]]


                else:
                    # qui assegno le righe della matrice che erano associate a spine di un certo tipo nel caso sperimentale
                    # alle spine (id) dello stesso tipo del caso in cui vengono riassegnate
                    # si fa anche la permutazione di quelle righe
                    # quindi da qui le righe associate a spine attivate, hanno come indici quelli del nuovo dataset
                    # dopo aver fatto le riassegnazioni delle spine

                    X_aus_BLA[BLA_activated_spine_idx_sim] = X_exc[BLA_activated_spine_idx_exp[BLA_ordine_activated_spine]]
                    X_aus_BLA[BLA_non_activated_spine_idx_sim] = X_exc[
                        BLA_non_activated_spine_idx_exp[BLA_ordine_non_activated_spine]]

                    X_aus_CA3[CA3_activated_spine_idx_sim] = X_exc[CA3_activated_spine_idx_exp[CA3_ordine_activated_spine]]
                    X_aus_CA3[CA3_non_activated_spine_idx_sim] = X_exc[
                        CA3_non_activated_spine_idx_exp[CA3_ordine_non_activated_spine]]


            if loop_numb == 0:
                in_m_ind = loop_numb * 50 + perm_ind  # quando sim_ind = 0 va da 0 a 49. quando e' =1 va da 50 a 99. quando = 2 va da 100 ... ok va bene
            else:
                in_m_ind = int(loop_numb-1) * 50 + perm_ind


            sample_filename = f'sim_{in_m_ind:07d}.npy'
            input_path_BLA = inputs_folder_BLA / sample_filename  # percorso in cui vanno a finire le matrici che si creano
            input_path_CA3 = inputs_folder_CA3 / sample_filename

            # l'arrotondamento a 5 cifre decimali, posso anche non metterlo perche' era gia' stato messo prima
            # le matrici quando arrivano qua sono solo permutate ma contengono gli stessi elementi di prima

            ''' Forse posso anche evitare di convertirle in float64, tanto qui si selezionano le righe e si permutano '''
            X_round_BLA = np.round(X_aus_BLA,5 )
            X_round_CA3 = np.round(X_aus_CA3,5 )

            X_scaled_BLA = (X_round_BLA - X_min) / (X_max - X_min) * 255.0
            X_scaled_CA3 = (X_round_CA3 - X_min) / (X_max - X_min) * 255.0

            X_uint8_BLA = np.round(X_scaled_BLA).astype(np.uint8)
            X_uint8_CA3 = np.round(X_scaled_CA3).astype(np.uint8)

            np.save(input_path_BLA, X_uint8_BLA)
            np.save(input_path_CA3, X_uint8_CA3)  # salva la matrice che ha creato

            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

