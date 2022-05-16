import bz2
import csv
import gzip
import json
import os
import pickle
import random
import sys
from pathlib import Path
from typing import Any, Generator, Union
from urllib.request import urlretrieve

import numpy as np
from tqdm import tqdm


def set_seeds(seed: int = 42):
    random.seed = seed
    np.random.seed = seed


def setup_logger(logger, dir: str, filename: str):
    os.makedirs(dir, exist_ok=True)

    logger.remove()
    logger.add(sys.stderr, level="TRACE")

    # Remove log file if exists
    try:
        os.remove(join_path(dir, filename))
    except:
        pass

    # Define logger output behaviour
    logger.add(
        join_path(dir, filename),
        enqueue=True,
        backtrace=True,
        diagnose=True,
        level="TRACE",
    )


# READ / WRITE =================================================================
def join_path(*args: str) -> str:
    return os.path.join(*args)


def write(x: str, path: Union[str, Path], encoding: str = "utf-8") -> None:
    with open(path, "w", encoding=encoding) as f:
        f.write(x)


def read(path: Union[str, Path], encoding: str = "utf-8") -> str:
    with open(path, "r", encoding=encoding) as f:
        x = f.read()
    return x


def write_list(
    x: list[str], path: Union[str, Path], encoding: str = "utf-8"
) -> None:
    with open(path, "w", encoding=encoding) as f:
        for y in x:
            f.write(y + "\n")


def read_list(path: Union[str, Path], encoding: str = "utf-8") -> list[str]:
    with open(path, "r", encoding=encoding) as f:
        x = f.read().splitlines()
    return x


def write_json(
    x: dict, path: Union[str, Path], encoding: str = "utf-8"
) -> None:
    with open(path, "w", encoding=encoding) as f:
        f.write(json.dumps(x, indent=4))


def read_json(path: Union[str, Path], encoding: str = "utf-8") -> dict:
    with open(path, "r", encoding=encoding) as f:
        x = json.loads(f.read())
    return x


def write_jsonl(
    x: list[dict], path: Union[str, Path], encoding: str = "utf-8"
) -> None:
    with open(path, "w", encoding=encoding) as f:
        for y in x:
            f.write(json.dumps(y) + "\n")


def read_jsonl(path: Union[str, Path], encoding: str = "utf-8") -> list[dict]:
    with open(path, "r", encoding=encoding) as f:
        x = [json.loads(line) for line in f]
    return x


def write_csv(
    x: list[dict],
    path: Union[str, Path],
    encoding: str = "utf-8",
    delimiter=",",
):
    with open(path, "w", encoding=encoding, newline="") as f:
        keys = list(x[0])
        dict_writer = csv.DictWriter(f, keys, delimiter=delimiter)
        dict_writer.writeheader()
        dict_writer.writerows(x)


def read_csv(
    path: Union[str, Path], encoding: str = "utf-8", delimiter=","
) -> list[dict]:
    csv.field_size_limit(sys.maxsize)
    with open(path, "r", encoding=encoding) as f:
        x = list(csv.DictReader(f, skipinitialspace=True, delimiter="\t"))
    return x


def write_pickle(x: list, path: Union[str, Path]) -> None:
    with open(path, "wb") as f:
        pickle.dump(x, f)


def read_pickle(path: Union[str, Path]) -> Any:
    with open(path, "rb") as f:
        x = pickle.load(f)
    return x


def write_numpy(x: np.ndarray, path: Union[str, Path]) -> None:
    with open(path, "wb") as f:
        np.save(file=f, arr=x)


def read_numpy(path: Union[str, Path]) -> np.ndarray:
    with open(path, "rb") as f:
        x = np.load(file=f)
    return x


def read_gzip(path: Union[str, Path]) -> str:
    with gzip.open(path, "rt") as f:
        x = f.read()
    return x


def read_gzip_list(path: Union[str, Path]) -> list[str]:
    with gzip.open(path, "rt") as f:
        x = f.read().splitlines()
    return x


# List Utils ===================================================================
def _flatten(x: list):
    for i in x:
        if not isinstance(i, (list, tuple)):
            return i
        for j in _flatten(i):
            return j


def flatten(x: list) -> list:
    return list(_flatten(x))


def chunk_by_size(x: list, n: int) -> list[list]:
    """Get n-sized chunks from x."""
    n = max(1, n)
    return [x[i : i + n] for i in range(0, len(x), n)]


def chunk_by_size_generator(x: list, n: int) -> Generator:
    """Yield successive n-sized chunks from x."""
    n = max(1, n)
    for i in range(0, len(x), n):
        yield x[i : i + n]


# OTHER ========================================================================
def count_lines(path: str, encoding: str="utf-8") -> int:
    """Counts the number of lines in a file."""
    if encoding == "utf-8":
        return sum(1 for _ in open(path))
    elif encoding == "bz2":
        return sum(1 for _ in bz2.open(path, "rt"))


def download(
    url: str, path: str, show_progress: bool = True, desc: str = "Download"
):
    if not show_progress:
        urlretrieve(url, path)
    else:
        pbar = tqdm(desc=desc, position=0, dynamic_ncols=True, mininterval=1.0,)

        previous_block_num = [0]

        def update_pbar(block_num=1, block_size=1, total_size=None):
            if total_size is not None:
                pbar.total = total_size
            pbar.update((block_num - previous_block_num[0]) * block_size)
            previous_block_num[0] = block_num

        urlretrieve(url, path, update_pbar)

        pbar.close()
