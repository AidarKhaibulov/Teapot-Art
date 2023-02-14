import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as image

# creates teapot array by using Bresenham's line algorithm
def Create_teapot_array(face_coordinates, x_coordinates, y_coordinates):
    # finding appropriate coordinates and shifting&scaling logic
    for i in range(0, len(face_coordinates), 3):
        for j in range(3):
            x1 = int(x_coordinates[int(face_coordinates[i + j])] * x_scale_coef + picture_x_center + 1)
            x2 = int(x_coordinates[int(face_coordinates[i + ((j + 1) % 3)])] * x_scale_coef + picture_x_center + 1)
            y1 = int(y_coordinates[int(face_coordinates[i + j])] * y_scale_coef + picture_y_center)
            y2 = int(y_coordinates[int(face_coordinates[i + ((j + 1) % 3)])] * y_scale_coef + picture_y_center)
            # Bresenham's algorithm
            delta_x = x2 - x1
            delta_y = y2 - y1

            sign_x = 1 if delta_x > 0 else -1 if delta_x < 0 else 0
            sign_y = 1 if delta_y > 0 else -1 if delta_y < 0 else 0

            if delta_x < 0: delta_x = -delta_x
            if delta_y < 0: delta_y = -delta_y

            if delta_x > delta_y:
                pdx, pdy = sign_x, 0
                es, el = delta_y, delta_x
            else:
                pdx, pdy = 0, sign_y
                es, el = delta_x, delta_y

            x, y = x1, y1

            error, t = el / 2, 0

            teapot_array[y, x, (0, 1, 2)] = 255

            while t < el:
                error -= es
                if error < 0:
                    error += el
                    y += sign_y
                    x += sign_x
                else:
                    y += pdy
                    x += pdx
                t += 1
                teapot_array[y, x, (0, 1, 2)] = 255


# create gradient painted circle within specified rectangle
def Draw_gradient(x1, x2, y1, y2):
    for i in range(y1, y2):
        for j in range(x1, x2):
            center_to_point_distance = int(((y2 - y1 // 2 - i) ** 2 + (x1 * 2 - j) ** 2) ** 0.5)
            if center_to_point_distance < (y2 - y1 // 2 - y1):
                teapot_array[i, j] = [255 +i, 255+j, 45]


x_coordinates, y_coordinates, face_coordinates = [np.array([]), np.array([]), np.array([])]

with open('teapot.obj', 'r', encoding='utf-8') as f:  # extracting data logic
    for current_line in f:
        match current_line[0]:
            case 'v':
                x_coordinates = np.append(x_coordinates, float(current_line[1:20].split()[0]))
                y_coordinates = np.append(y_coordinates, float(current_line[1:20].split()[1]))
            case 'f':
                for i in current_line[1:].split():
                    face_coordinates = np.append(face_coordinates, int(i) - 1)
picture_width = 1920
picture_height = 1020
teapot_array = np.zeros((picture_height // 3, picture_width // 3, 3), dtype=np.uint8)
picture_x_center = picture_width // 6
picture_y_center = picture_height // 6
# evaluating width and height source teapot
teapot_true_height = (max(y_coordinates) - min(y_coordinates))
teapot_true_width = (max(x_coordinates) - min(x_coordinates))
# evaluating scale coefficient for source size teapot
x_scale_coef = int(picture_x_center / teapot_true_width)
y_scale_coef = int(picture_y_center / teapot_true_height)

Draw_gradient(picture_x_center // 2, picture_width // 3 - picture_x_center // 2, picture_y_center, picture_height // 3)

Create_teapot_array(face_coordinates, x_coordinates, y_coordinates)

# image drawing
plt.imshow(teapot_array, origin='lower')
image.imsave('teapot.png', teapot_array, origin='lower')
plt.show()
