from PIL import Image

img = Image.open("mysite/static/images/maps/Desktop_-_1_6.png")
r, g, b, a = img.getpixel((1, 1))

print(r, g, b, a)