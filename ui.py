import pygame

def draw_text(screen: pygame.Surface, font_file: str, text: str, 
	font_size: int, color: tuple, pos: tuple, backg=None, bold=False, italic=False, underline=False):
	"""Draws text to the screen given a font file and text."""
	if ".ttf" in font_file:
		font = pygame.font.Font(font_file, font_size)
	else:
		font = pygame.font.SysFont(font_file, font_size)
	font.set_bold(bold)
	font.set_italic(italic)
	font.set_underline(underline)
	if backg == None:
		t = font.render(text, 1, color)
	t = font.render(text, 1, color, backg)
	textRect = t.get_rect()
	textRect.center = pos
	screen.blit(t, textRect)

def fill(surface, color):
    """Fill all pixels of the surface with color, preserve transparency."""
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

class Button():
	def __init__(self, x, y, image, scale, txt=None):
		width = image.get_width()
		self.x, self.y = x, y
		self.text = txt
		height = image.get_height()
		self.click_img = pygame.transform.scale(image, (int(width * (scale+0.3)), int(height * (scale+0.3))))
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.norm_img = self.image
		self.norm_font_size = self.text[3] if self.text != None else None
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.image = self.click_img
				self.rect = self.image.get_rect()
				self.rect.center = (self.x, self.y)
				if self.text != None:
					self.text[3] = self.norm_font_size*2
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.image = self.norm_img
			self.rect = self.image.get_rect()
			self.rect.center = (self.x, self.y)
			if self.text != None:
				self.text[3] = self.norm_font_size
			self.clicked = False

		#draw button
		surface.blit(self.image, (self.rect.x, self.rect.y))
		if self.text != None:
			draw_text(*self.text, (self.rect.centerx, self.rect.centery))

		return action