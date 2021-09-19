from PIL import Image

img = Image.open("sample.png")
img.show()
a = img.crop((0, 9, 30, 21))
a.show()
a = a.resize((15, 6))
b = list(a.getdata())
print(len(b))
