import cv2
import numpy as np

class Transform:

    def __init__(self, img, path, destination, db, name):
        self.img = img
        self.width, self.height = (self.img).shape[:2]
        self.path = path
        self.destination = destination
        self.db = db
        self.name = name
    
    def cal(self,mean):
        noise = self.db/10
        x = 10**(noise)
        #print("Value :", c)
        return (mean/x)**2

    def resize(self, wid, heigh):
        image = self.img
        self.img = self.image_resize(image, wid,heigh)

        mean = 10
        var = self.cal(np.mean(image))
        sigma = var ** 0.5                                
        gaussian = np.random.normal(mean, sigma, (self.img.shape[:2])) # Error counter [np.zeros((224, 224), np.float32)]

        noisy_image = np.zeros(self.img.shape, np.float32)

        if len(self.img.shape) == 2:
            noisy_image = self.img + gaussian
        else:
            noisy_image[:, :, 0] = self.img[:, :, 0] + gaussian
            noisy_image[:, :, 1] = self.img[:, :, 1] + gaussian
            noisy_image[:, :, 2] = self.img[:, :, 2] + gaussian

        cv2.normalize(noisy_image, noisy_image, 0, 255, cv2.NORM_MINMAX, dtype=-1)
        noisy_image = noisy_image.astype(np.uint8)

        # Reshape noisy image 100x50
        noisy1 = cv2.resize(noisy_image, (100, 50), interpolation = cv2.INTER_AREA)
        print("Shape: ", noisy1.shape)
        print("SNR: ")
        print(10*np.log10(np.mean(img)/sigma), "dB")
        print("Shape of transformed Image: ", self.img.shape)

        # Save results 
        #cv2.imwrite(self.destination + self.name, noisy1)
            
        #Visualise images
        #cv2.imshow('Noise Image', noisy1)
        #cv2.imshow('Actual Image', image)
        #cv2.waitKey(0)

    def image_resize(self, image, width = None, height = None, inter = cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation = inter)

        # return the resized image
        return resized

dbs = ['_Noise_-3_db.png', '_Noise_0_db.png', '_Noise_3_db.png', '_Noise_7_db.png', '_Noise_20_db.png']
deci = [-3, 0, 3, 7, 20]
resolutions = ['12', '15', '20', '25', '35', '45', '55']
intres = [int(x) for x in resolutions]

# Path of origin
imagePath = 'C:\\Users\\nanda\\select31.png'
img = cv2.imread(imagePath, 1)

# Path of destination
destination = "C:\\Users\\nanda\\Data"
name = "\\license_HR26BH3864_Resolution_"

print(intres)

#print(destination+name)
# Change Noise level
count = 0
for i in resolutions:
    for j in range(len(dbs)):
        sizing = Transform(img, imagePath, destination, deci[j], name+i+dbs[j])
        sizing.resize(int(i), (int(i))*2)
        count+=1

print("*******************")
print(count)
print("*******************")
# Change resolution
#sizing.resize(15, 30)

"""
for x in resolutions:
    for y in dbs:"""

# Reference (self, img, path, destination, db, name)
