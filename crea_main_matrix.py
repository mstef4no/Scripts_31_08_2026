from pathlib import Path
import flammkuchen as fl
import numpy as np


def build_main_matrix(yymmdd, cell, output_folder):
    """
    La matrice viene costruita mettendo input random su tutte le spine. Il numero delle spine viene preso
    dal dataset che viene caricato """
    inputs_folder = output_folder
    inputs_folder.mkdir(parents=True, exist_ok=True)

    # ----- path del dataset con assegnazione delle spine come dai dati sperimentali
    data_path = ("D:/test_save_old/" + yymmdd + "_" + cell + "_morph_and_spines.h5")

    data = fl.load(data_path)
    spine_numb = len(data['spines_df'])  # informazione sul numero di spine che viene presa dal dataset

    sim_duration_ms = 800
    exc_sparsity_level_range = [0.995, 0.999]

    X_exc = np.random.rand(spine_numb, sim_duration_ms) * 0.0007
    exc_sparsity_level = np.random.uniform(*exc_sparsity_level_range)
    X_exc[np.random.rand(spine_numb, sim_duration_ms) < exc_sparsity_level] = 0.0

    num_intervals = np.random.randint(1, 5)
    for _ in range(num_intervals):
        interval_duration_ms = np.random.randint(1, 11)

        # mult_factor = np.random.choice([0.0, 0.1, 0.2, 0.3, 1.0], p=[0.4, 0.1, 0.1, 0.1, 0.3])
        mult_factor = np.random.choice([0.0, 0.1, 0.2, 0.3, 0.5], p=[0.4, 0.2, 0.2, 0.1, 0.1])  # M3 test.
        # mult_factor = np.random.choice([0.0, 0.1, 0.2, 0.3, 1.0], p=[0.4, 0.1, 0.1, 0.1, 0.3])

        start_ind = np.random.randint(0, sim_duration_ms - interval_duration_ms)
        end_ind = start_ind + interval_duration_ms
        X_exc[:, start_ind:end_ind] = mult_factor * X_exc[:, start_ind:end_ind]

    # ----- qui i numeri sono in float64
    X_round = np.round(X_exc, 5)  # arrotondo gli elementi a 5 cifre decimali

    # ----- converto in uint8
    X_min = 0.0
    X_max = 0.0007

    # ----- converto gli elementi della matrice in uint8
    X_scaled = (X_round - X_min) / (X_max - X_min) * 255.0
    X_uint8 = np.round(X_scaled).astype(np.uint8)

    sample_filename = 'sim_0000000.npy'
    input_path = inputs_folder / sample_filename


    np.save(input_path, X_uint8)
    return input_path


