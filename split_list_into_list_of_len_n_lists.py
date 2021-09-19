from typing import List


def split_list_into_list_of_len_n_lists(L: List, n: int) -> List[List]:
    return [L[i:i + n] for i in range(0, len(L), n)]
