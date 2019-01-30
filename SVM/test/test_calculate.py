import src.calculate as my_test


def test_calculate_x1():
    result = my_test.calculate_x1(10, 8)
    print("test_result : " + str(result) + " except_result : 0.25")


def test_calculate_x2():
    result = my_test.calculate_x2(10, 8)
    print("test_result : " + str(result) + " except_result : 0.25")


def test_calculate_x3():
    result = my_test.calculate_x3(10, 8)
    print("test_result : " + str(result) + " except_result : 0.25")


def test_calculate_x4():
    result = my_test.calculate_x4(10, 8)
    print("test_result : " + str(result) + " except_result : 0.25")


def test_calculate_x5():
    result = my_test.calculate_x5(10, 8)
    print("test_result : " + str(result) + " except_result : -0.2")


def test_calculate_yes_bo_dong_lv():
    yes_close_price = [1, 2, 3]
    result = my_test.calculate_yes_bo_dong_lv(yes_close_price)
    print("test_result : " + str(result) + " except_result : (根号)6/3（1.41）")


def test_calculate_new_bo_dong_lv():
    new_close_price = [1, 2, 3]
    result = my_test.calculate_new_bo_dong_lv(new_close_price, 9, 3)
    print("test_result : " + str(result) + " except_result : 2.4....")


def test_calculate_x6():
    result = my_test.calculate_x6(8, 10)
    print("test_result : " + str(result) + " except_result : 0.25")


def test_calculate_x7():
    result = my_test.calculate_x7(10, 8)
    print("test_result : " + str(result) + " except_result : 0.25")
