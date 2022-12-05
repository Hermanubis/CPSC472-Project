from img_detection import *

image = cv2.imread('./test2.jpg')
red = []
green = []
blue = []
gray = []
# for x in range(0,camera2.getWidth()):
#     for y in range(0,camera2.getHeight()):
#         red.append(image[x][y][0])
#         green.append(image[x][y][1])
#         blue.append(image[x][y][2])
#         gray.append((image[x][y][0] + image[x][y][1] + image[x][y][2]) / 3)
data = np.array(image, dtype = np.uint8) 
dimensions = image.shape
object_data = object_info(image, image.shape[0], image.shape[1])
print("object date\n",object_data)
for i in range(len(object_data)):
    x,y = object_data[i][0]
    print(x,y, image.shape[0], image.shape[1])
    
    B  = image[x][y][0]
    G = image[x][y][1]
    R  = image[x][y][2]
    color = getColorName(R,G,B)
    print(R,G,B,color)
    print("area",object_data[i][1])