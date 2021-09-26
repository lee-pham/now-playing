from typing import List


def convert_24_bit_to_8_bit(pixel_list: List[List]) -> List[int]:
    compressed_colors = []
    for r, g, b in pixel_list:
        compressed_colors.append(((r // 32) << 5) + ((g // 32) << 2) + (b // 64))

    return compressed_colors
