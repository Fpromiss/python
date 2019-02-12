import src.my_calculate as test_calculate


def test_calculate_x1():
    result = test_calculate.calculate_x1(10, 8)
    print("test_result : " + str(result) + " except_result : 0.25")


def test_calculate_x2():
    result = test_calculate.calculate_x2(10, 8)
    print("test_result : " + str(result) + " except_result : 0.25")


def test_calculate_x3():
    result = test_calculate.calculate_x3(10, 8)
    print("test_result : " + str(result) + " except_result : 0.25")


def test_calculate_x4():
    result = test_calculate.calculate_x4(10, 8)
    print("test_result : " + str(result) + " except_result : 0.25")


def test_calculate_new_volume():
    result = test_calculate.calculate_new_volume(10, 10, 5)
    print("test_result : " + str(result) + " except_result : 20")


def test_calculate_x5():
    result = test_calculate.calculate_x5(10, 8)
    print("test_result : " + str(result) + " except_result : -0.2")


def test_calculate_yes_bo_dong_lv():
    yes_close_price = [1, 2, 3]
    result = test_calculate.calculate_yes_bo_dong_lv(yes_close_price)
    print("test_result : " + str(result) + " except_result : (根号)6/3（0.8....）")


def test_calculate_new_bo_dong_lv():
    new_close_price = [8.1, 8.2, 8.3]
    result = test_calculate.calculate_new_bo_dong_lv(new_close_price, 48, 12)
    print("test_result : " + str(result) + " except_result : 1.6....")


def test_calculate_x6():
    result = test_calculate.calculate_x6(8, 10)
    print("test_result : " + str(result) + " except_result : 0.25")


def test_calculate_x7():
    result = test_calculate.calculate_x7(10, 8)
    print("test_result : " + str(result) + " except_result : 0.25")


def test_calculate_x8():
    result = test_calculate.calculate_x8(8, 10)
    print("test_result : " + str(result) + " except_result : -0.2")


def test_calculate_x9():
    result = test_calculate.calculate_x8(8, 10)
    print("test_result : " + str(result) + " except_result : -0.2")