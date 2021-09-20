from math import ceil

from split_list_into_list_of_len_n_lists import split_list_into_list_of_len_n_lists


def test_len_of_split_lists_equal_to_len_original_list():
    L = list(range(82))
    n = 24
    assert len(L) == sum(len(chunk) for chunk in split_list_into_list_of_len_n_lists(L, n))


def test_len_of_chunk_does_not_exceed_n():
    L = list(range(82))
    n = 24
    assert max(len(chunk) for chunk in split_list_into_list_of_len_n_lists(L, n)) <= n


def test_num_chunks_equal_to_ceil_len_L_divided_by_n():
    L = list(range(82))
    n = 24
    assert len(split_list_into_list_of_len_n_lists(L, n)) == ceil(len(L) / n)
