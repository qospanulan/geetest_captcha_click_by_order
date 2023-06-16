from geetest_captcha_solver import OrderedCaptchaSolver

if __name__ == '__main__':
    main_image_path = 'images/main.png'

    small_image_path_1 = 'images/small_0.png'
    small_image_path_2 = 'images/small_1.png'
    small_image_path_3 = 'images/small_2.png'

    result_image_path = 'images/result.png'

    solver = OrderedCaptchaSolver(
        main_image_path,
        small_image_path_1,
        small_image_path_2,
        small_image_path_3,
        result_image_path
    )

    p = solver.get_points_coordinates()
