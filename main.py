from PIL import Image
image = Image.open("album.PNG")
resized_image = image.resize((8, 8))
resized_image.show(resized_image)
