import cv2 as cv


class OrderedCaptchaSolver:
    def __init__(self, main_image_path, small_image_path_1, small_image_path_2, small_image_path_3, result_image_path):
        self.__main_image_path = main_image_path
        self.__result_image_path = result_image_path
        self.__small_images_paths = [small_image_path_1, small_image_path_2, small_image_path_3]

    def get_points_coordinates(self):
        self.__main_image = self.__get_processed_main_image()
        self.__small_images = self.__get_processed_small_images()

        coordinates = self.__match_and_get_coordinates()

        self.__paint_points(coordinates)

        return coordinates

    def __get_processed_main_image(self):
        img = cv.imread(self.__main_image_path)

        lab = cv.cvtColor(img, cv.COLOR_BGR2LAB)
        lab_gray = cv.cvtColor(lab, cv.COLOR_BGR2GRAY)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        (thresh, binary_img) = cv.threshold(lab_gray, 127, 255, cv.THRESH_BINARY)

        (thresh2, binary_img_unnecessary_part) = cv.threshold(gray, 200, 255, cv.THRESH_BINARY)

        binary_result = cv.bitwise_xor(binary_img, binary_img_unnecessary_part)

        bgr_result = cv.cvtColor(binary_result, cv.COLOR_GRAY2BGR)

        return bgr_result

    def __get_processed_small_images(self):
        small_images = []
        for small_image_path in self.__small_images_paths:
            small_image = cv.imread(small_image_path, cv.IMREAD_UNCHANGED)[:, :, 3]
            small_image = cv.cvtColor(small_image, cv.COLOR_GRAY2BGR)
            small_images.append(small_image)

        return small_images

    def __match_and_get_coordinates(self):

        coordinates = []

        for small_image in self.__small_images:
            result = cv.matchTemplate(self.__main_image, small_image, cv.TM_CCOEFF_NORMED)

            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

            top_left = max_loc
            center_point = (top_left[0] + small_image.shape[1] // 2, top_left[1] + small_image.shape[0] // 2)

            coordinates.append(center_point)

        return coordinates

    def __paint_points(self, coordinates):
        circle_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for i, center_point in enumerate(coordinates):
            cv.circle(self.__main_image, center_point, 5, circle_colors[i], thickness=3)

        cv.imwrite(self.__result_image_path, self.__main_image)
