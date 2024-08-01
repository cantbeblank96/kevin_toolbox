from kevin_toolbox.patches.for_matplotlib.color import Color_Format, get_format, convert_format, generate_color_list
from kevin_toolbox.patches.for_test import check_consistency


def test_get_format():
    assert get_format(var=(255, 87, 51, 0.5)) == Color_Format.RGBA_ARRAY
    assert get_format(var=(255, 87, 51)) == Color_Format.RGBA_ARRAY
    assert get_format(var="#FF57337F") == Color_Format.HEX_STR
    assert get_format(var="#ff5733") == Color_Format.HEX_STR
    assert get_format(var="blue") == Color_Format.NATURAL_NAME


def test_convert_format():
    rgba = (255, 192, 203, 0.5)
    # rgba ==> hex
    hex_ = convert_format(var=rgba, output_format=Color_Format.HEX_STR)
    # hex ==> rgba
    rgba_1 = convert_format(var=hex_, input_format='hex_str', output_format='rgba_array')
    # rgba ==> natural_name
    name = convert_format(var=rgba, output_format="natural_name")
    # natural_name ==> rgba
    rgba_2 = convert_format(var=name, input_format=Color_Format.NATURAL_NAME, output_format='rgba_array')
    # hex ==> natural_name
    name_1 = convert_format(var=hex_, output_format=Color_Format.NATURAL_NAME)
    # natural_name ==> hex
    hex_1 = convert_format(var=name_1, input_format=Color_Format.NATURAL_NAME, output_format=Color_Format.HEX_STR)

    check_consistency(rgba, rgba_1, tolerance=1 / 255)
    check_consistency(rgba[:3], rgba_2)
    check_consistency("#FFC0CB7F", hex_)
    check_consistency("#FFC0CB", hex_1)
    check_consistency("pink", name, name_1)


def test_generate_color_list():
    # 测试指定 seed 是否能固定生成的颜色列表
    for output_format in [Color_Format.RGBA_ARRAY, Color_Format.HEX_STR]:
        temp_ls = []
        for _ in range(5):
            temp_ls.append(generate_color_list(nums=15, seed=114514, output_format=output_format))
        check_consistency(*temp_ls)

    # 测试能否通过 exclude_ls 排除指定颜色
    for exclude_ls in [['blue', *temp_ls[-1][-2:]],
                       ['#0000FF', *temp_ls[0][-2:]]]:
        temp = generate_color_list(nums=15, seed=114, exclude_ls=exclude_ls)
        temp = set(convert_format(var=i, output_format=Color_Format.HEX_STR) for i in temp)
        for i in exclude_ls:
            assert convert_format(var=i, output_format=Color_Format.HEX_STR) not in temp
