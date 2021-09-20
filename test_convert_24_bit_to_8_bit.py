from convert_24_bit_to_8_bit import convert_24_bit_to_8_bit


def test_white_rgb_equal_white_8_bit():
    assert convert_24_bit_to_8_bit([[255, 255, 255]]) == [255]


def test_len_compressed_list_is_exactly_one_third_len_original_list():
    L = [[255, 255, 255]]
    assert len(convert_24_bit_to_8_bit(L)) == sum(len(x) for x in L) / 3
