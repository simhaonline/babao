"""
TODO
"""

from functools import partial
import pandas as pd

import babao.inputs.inputBase as inputBase
import babao.config as conf


def resampleSerie(s):
    """
    Call Serie.resample on s with preset parameters
    (the serie's index must be datetime)
    """
    # TODO: would be nice to do the base init once for all features
    # (ensure sync and save some computing)
    # also don't convert date or do it in utils.date
    base = pd.to_datetime(inputBase.LAST_WRITE, unit="ns")
    base = (base.minute + (base.second + 1) / 60) % 60
    return s.resample(
        str(conf.TIME_INTERVAL) + "Min",
        closed="right",
        label="right",
        base=base
    )


def readInputs(input_list, since=None, till=None):
    """TODO"""

    def _renamer(prefix, s):
        """TODO"""
        return prefix + "_" + s

    def _restorer(prefix, s):
        """TODO"""
        return s.replace(prefix + "_", "")

    # TODO: opt memory usage / lock once
    data_list = [inp.read(since, till) for inp in input_list]

    # TODO: ensure resample base is correct (use till, or?)
    for i, inp in enumerate(input_list):
        data_list[i] = inp.resample(data_list[i])
        data_list[i].rename(
            partial(_renamer, inp.__class__.__name__),
            axis="columns",
            inplace=True
        )

    df = data_list[0].join(data_list[1:], how="outer")

    for inp in input_list:
        partial_renamer = partial(_renamer, inp.__class__.__name__)
        inp._fillMissing(
            df[
                [partial_renamer(col) for col in inp.resampled_columns]
            ].rename(
                partial(_restorer, inp.__class__.__name__),
                axis="columns"
            )
        )

    return df
