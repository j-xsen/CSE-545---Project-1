from PIL import Image, ImageDraw

from TSP import TSP, read_tsp

# config
size = (100, 100)
scale = 10
city_radius = 5

img = Image.new('RGB', (size[0]*scale, size[1]*scale), color = 'white')

draw = ImageDraw.Draw(img)

imported_tsp = read_tsp('Random4.tsp')

for coord in imported_tsp.coords:
    bbox = [coord.x-city_radius, coord.y-city_radius, coord.x+city_radius, coord.y+city_radius]
    draw.ellipse(bbox, fill = 'black')
    draw.text((coord.x-(city_radius/2), coord.y-(city_radius*4)), str(coord.name), fill = 'black')

img.show()