This project reads an image and based on the dimensions of a reference object; it finds the 
dimensions of other objects in a scene. The reference object must be the leftmost, topmost
object in the scene. In this case, a box of dimension 2cm x 2cm is taken as a reference object.
For any other reference object, we can provide the actual width of the object. 

**Prerequisites:**

1. Python 3 
2. OpenCV 
3. NumPy
4. SciPy
5. VS Code, Google Colab (Any IDE)

**Constraints**

1. Shadows can cause incorrect prediction. This can be avoided by making sure there is 
enough light.
2. To get accurate object boundary, dark background is used.

**Algorithm**

**1. Image pre-processing**
• Read an image and convert it to grayscale
• Blur the image using Gaussian Kernel to remove unnecessary edges/ reduce noises.
• Edge detection using Canny edge detector is performed on the blurred image using a 
threshold value.
• Create a kernel for morphological operations (dilation and erosion) using NumPy.
• Dilate the edges obtained from Canny edge detection to make them more contiguous.
• Erode the dilated image to further refine the edges.

**2. Reference object**
• Calculate how many pixels are there per metric (centimeter is used here)

**3. Compute results**
• Draw bounding boxes around each object and calculate its height and width
