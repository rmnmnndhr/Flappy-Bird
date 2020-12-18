import pygame
from os import path

img_dir = path.join(path.dirname(__file__), 'letter_img')

# loading image
# numbers
img0 = pygame.image.load(path.join(img_dir, '0.png'))
img1 = pygame.image.load(path.join(img_dir, '1.png'))
img2 = pygame.image.load(path.join(img_dir, '2.png'))
img3 = pygame.image.load(path.join(img_dir, '3.png'))
img4 = pygame.image.load(path.join(img_dir, '4.png'))
img5 = pygame.image.load(path.join(img_dir, '5.png'))
img6 = pygame.image.load(path.join(img_dir, '6.png'))
img7 = pygame.image.load(path.join(img_dir, '7.png'))
img8 = pygame.image.load(path.join(img_dir, '8.png'))
img9 = pygame.image.load(path.join(img_dir, '9.png'))

img_dict = {'0': img0, '1': img1, '2': img2, '3': img3, '4': img4, 
			'5': img5, '6': img6, '7': img7, '8': img8, '9': img9,
			}

def draw_text(text, size, screen, x, y):
	img_list = []
	for let in text.lower():
		img = img_dict[let]
		img_list.append(img)

	length = 0
	for img in img_list:
		rect = img.get_rect()
		rect.width = int(rect.width * size/100)
		rect.height = int(rect.height * size/100)
		length += rect.width

	for img in img_list:
		rect = img.get_rect()
		rect.width = int(rect.width * size/100)
		rect.height = int(rect.height * size/100)
		img = pygame.transform.scale(img, (rect.width, rect.height))
		screen.blit(img, (x - length / 2, y))
		x += rect.width + 1


