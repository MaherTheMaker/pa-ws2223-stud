import math
from typing import Union
import numpy as np
import pandas as pd
import h5py
from statsmodels.base.data import handle_data_class_factory


def gen_path_for_multi_speeds(
        run_id: int, index: list[str], pump_speeds: list[float]
) -> list[str]:
    res = []
    for speed in pump_speeds:
        for deg in index:
            res.append("run{}/Kennlinie_ESP_c_{}_{}".format(run_id, speed, deg))

    return res


def read_dataframe_metadata(
        file: str, path: str, att_key: str
) -> Union[np.float64, np.int32, np.bytes_, None]:
    with pd.HDFStore(file) as store:
        group = store.get_node(path)
        try:
            metadata_value = group._v_attrs[att_key]
        except AttributeError:
            message = f"Metadata '{att_key}' not found in group '{path}'."
            print(message)
            raise KeyError(message)
        return metadata_value


def read_group_metadata(
        file: str, path: str, att_key: str
) -> Union[np.float64, np.int32, np.bytes_, None]:
    hd = h5py.File(file, "r+")
    hd_data = hd.get(path)
    try:

        return hd_data.attrs[att_key]
    except KeyError as e:
        print(e)


def get_df(file: str, path: str) -> pd.DataFrame:
    # TODO check for errors and use pandas
    try:
        with pd.HDFStore(file) as store:
            group = store.get_node(path + "/block0_values")
            group = pd.DataFrame(group)
            col_name = store.get_node(path + "/block0_items")
            col_name = [a.decode('utf-8') for a in col_name]
            group.columns = col_name
    except FileNotFoundError as e:
        print(e)
        exit()
    except TypeError as e:
        print(e)
        exit()
    return group


def check_col_signum(df: pd.DataFrame, col: str, threshold: int) -> None:
    col_values = df[col].values
    if not all(v >= threshold for v in col_values):
        message = f"Values of column '{col}' do not meet the criterion: all values must be greater than or equal to {threshold}."
        print(message)
        raise ValueError(message)


def check_number_of_measurements(
        df: pd.DataFrame, col: str, f: float, t: float
) -> None:
    """
    Check that the number of measurements is consistent with the sampling frequency and measuring period.

    Args:
        df (pd.DataFrame): DataFrame containing the data to check.
        col (str): Name of the column to check.
        f (float): Sampling frequency in Hz.
        t (float): Measuring period in s.

    Raises:
        ValueError: If the number of measurements is not consistent with the sampling frequency and measuring period.
    """

    expected_length = int(f * t)
    actual_length = len(df[col])
    if actual_length % expected_length != 0:
        raise ValueError(
            f"Number of measurements ({actual_length}) is not consistent with the sampling frequency and measuring period ({f} Hz, {t} s).")


def gen_plotdata(
        file_path: str,
        path_list: list,
        cols: list,
        output_size: tuple,
) -> np.ndarray:
    pass


def get_average_value(df: pd.DataFrame, col: str) -> float:
    return df[col].mean()


def get_std_deviation(df: pd.DataFrame, col: str) -> float:
    # TODO Rename var
    avg_x = get_average_value(df, col)
    N = len(df[col])
    SSS = [(x - avg_x) ** 2 for x in df[col]]
    std = math.sqrt(sum(SSS) / (N - 1))

    return std
    pass


def std_uniform_to_normal(std_uniform: float) -> float:
    return std_uniform / math.sqrt(3)


def total_uncertainty(stat: float, sys: float) -> float:
    res = math.sqrt(stat ** 2 + sys ** 2)
    return res


def convert_bar_to_pa(v: pd.Series) -> pd.Series:
    q = lambda a: a * 100000
    newV = [q(s) for s in v.values]
    v.update(newV)
    return v


def convert_lpm_to_qmps(v: pd.Series) -> pd.Series:
    q = lambda a: a / 60000
    newV = [q(s) for s in v.values]
    v.update(newV)
    return v


def dataframe_dedimension(
        plot_data: pd.DataFrame,
        pump_speeds: list,
        metadata: dict,
) -> pd.DataFrame:
    pass


def convert_rpm_to_hz(v: float) -> float:
    return v / 60


def calc_pressure_number(
        delta_p: float,
        n: float,
        d: float,
        rho: float,
) -> float:
    res = (2 * delta_p) - (n * n * d * d * rho)
    return res


def calc_flow_number(q: float, n: float, d: float) -> float:
    res = (4 * q) / (np.pi ** 2 * n * d ** 3)
    return res


def uncertainty_pressure_number(
        total_uncertainty_p: float,
        p: float,
        total_uncertainty_rho: float,
        rho: float,
        total_uncertainty_n: float,
        n: float,
        total_uncertainty_d: float,
        d: float,
        psi: float,
) -> float:
    r1 = (total_uncertainty_p / p) ** 2
    r2 = (total_uncertainty_rho / rho) ** 2
    r3 = (2 * total_uncertainty_n / n) ** 2
    r4 = (2 * total_uncertainty_d / d) ** 2

    res = psi * math.sqrt(r1 + r2 + r3 + r4)

    return res



def uncertainty_flow_number(
        total_uncertainty_q: float,
        q: float,
        total_uncertainty_n: float,
        n: float,
        total_uncertainty_d: float,
        d: float,
        phi: float,
) -> float:
    r1 = (total_uncertainty_q / q) ** 2
    r2 = (total_uncertainty_n / n) ** 2
    r3 = (3 * total_uncertainty_d / d) ** 2

    res = phi * math.sqrt(r1 + r2 + r3)
    return res


def main():

    pass


if __name__ == "__main__":
    main()
