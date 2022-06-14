import pygame, time, random, ui, math
pygame.init()
pygame.font.init()
pygame.mixer.init()

screen = pygame.display.set_mode((700, 500))
sw, sh = 700, 500
pygame.display.set_caption("Space Drift")
fps = 240
timer = 0 
vel_y = 0
jump = False
in_air = False
GRAVITY = 0.15
clock = pygame.time.Clock()
prev_time = time.time()
flip_gravity = False
dt = 0
run = True
speedBoost = 0.10  # 10 meters / second
level = 1
decor_objs = ["blueyellowstar.png", "purpleyellowstar.png", "spark.png", "spark2.png"]
add_decor = pygame.time.set_timer(pygame.USEREVENT+1, 1000)
stars = []
destroyObj = pygame.transform.scale(pygame.image.load("destroy.png"), (40, 40))
distance_txt = pygame.image.load("distance-text.png")
time_txt = pygame.image.load("time-text.png")
banner = pygame.image.load("spacedrift-logo.png")
spark = pygame.image.load("spark.png")

lose_sound = pygame.mixer.Sound("lose.wav")
lose_sound.set_volume(0.5)

speedX0Portal = pygame.image.load("speedx0portal.png")
speedX1Portal = pygame.image.load("speedx1portal.png")
speedX2Portal = pygame.image.load("speedx2portal.png")
speedX5Portal = pygame.image.load("speedx5portal.png")
speedX8Portal = pygame.image.load("speedx8portal.png")
speedX12Portal = pygame.image.load("speedx12portal.png")
invertPortal = pygame.image.load("invertportal.png")
normalPortal = pygame.image.load("normalportal.png")

showHitboxes = False
disableCollisions = False



PORTALS = {
	"x0":speedX0Portal,
	"x1":speedX1Portal,
	"x2":speedX2Portal,
	"x5":speedX5Portal,
	"x8":speedX8Portal,
	"x12":speedX12Portal,
	"inverted":invertPortal,
	'normal':normalPortal
}

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


def get_text_rect(font_file, text, font_size, pos) -> pygame.Rect:
    """Returns the bounding rectangle of a text object drawn to the screen."""
    font = pygame.font.Font(font_file, font_size)
    t = font.render(text, 1, (0,0,0))
    textRect = t.get_rect()
    textRect.center = pos
    return textRect

def get_text_width(font_file, text, font_size):
	font = pygame.font.Font(font_file, font_size)
	t = font.render(text, 1, (0,0,0))
	textRect = t.get_rect()
	return textRect.width


normSpeed = 200
speed = normSpeed
normPlayerSpeed = 50
destroyObjects = []
speedPortals = []
addSpeedPortal = pygame.time.set_timer(pygame.USEREVENT+3, 5000)
addDestroyObject = pygame.time.set_timer(pygame.USEREVENT+4, 3000)
addDestroyObject2 = pygame.time.set_timer(pygame.USEREVENT+5, 3000)
addDestroyObject3 = pygame.time.set_timer(pygame.USEREVENT+6, 6000)

# speedPortals.append({"x":730, "y":250,"atDst":200, "type":"x2"})
# speedPortals.append({"x":730, "y":250,"atDst":1000, "type":"x3"})
# speedPortals.append({"x":730, "y":250, "atDst":2100, "type":"inverted"}) # flips gravity
# speedPortals.append({"x":730, "y":250, "atDst":3000, "type":"normal"}) # flips gravity
# for x in range(10):
# 	destroyObjects.append({"x":730+(300*x), "y":random.randint(50, 400), "atDst":200}) # atDist is the distance
# for x in range(10):
# 	destroyObjects.append({"x":730+(300*x), "y":random.randint(50, 400), "atDst":400}) # atDist is the distance
# for x in range(10):
# 	destroyObjects.append({"x":730+(300*x), "y":random.randint(50, 400), "atDst":800}) # atDist is the distance
# for x in range(10):
# 	destroyObjects.append({"x":730+(300*x), "y":random.randint(50, 400), "atDst":1000}) # atDist is the distance

		
class Drifter:
	def __init__(self, x, y):
		self.img = pygame.transform.scale(pygame.image.load("drifter.png"), (70, 70))
		self.rect = self.img.get_rect()
		self.rect.x = x
		self.rect.y = y
	
	def draw(self, screen):
		screen.blit(self.img, self.rect)


player = Drifter(50, sh/2-25)
start_ticks=pygame.time.get_ticks()
playerX = 0
bg = pygame.image.load("gamebg.png").convert()
bg_lose = pygame.image.load("losebg.png").convert()
bg_width = bg.get_width()
bg_rect = bg.get_rect()
scroll = 0
tiles = math.ceil(sw  / bg_width) + 1


play_btn = ui.Button(banner.get_rect().centerx*2, sh/2, pygame.image.load("play_btn.png"), 1.5)
restart_btn = ui.Button(bg_lose.get_rect().centerx-100, sh/2+130, pygame.image.load("restartbtn.png"), 1.5)
menu_btn = ui.Button(bg_lose.get_rect().centerx+100, sh/2+130, pygame.image.load("menubtn.png"), 1.5)
player_dead = pygame.USEREVENT+2
screens = ["playScreen", "startScreen", "endScreen"]
activeScreen = screens[1]

randomPortalTypes = [p for p in PORTALS.keys()]


while run:
	clock.tick(fps)
	
	if activeScreen == "playScreen": # runs the game
        # Compute delta time
		dy = 0
		now = time.time()
		dt = now - prev_time
		prev_time = now
		seconds=(pygame.time.get_ticks()-start_ticks)/1000
		timer += dt
		playerX += (speed*dt)*(speedBoost)
		#scroll background
		scroll -= (speed*dt)
	
	    #reset scroll
		if abs(scroll) > bg_width:
			scroll = 0
    
		for star in stars: 
			star[1][0] -= (speed+20)*dt # update x position
			if star[1][0] < star[0].get_rect().width * -1:
				stars.pop(stars.index(star))
				
		for obj in destroyObjects: 
			obj["x"] -= (speed+20)*dt # update x position
			if obj["x"] < pygame.image.load("destroy.png").get_rect().width * -1: # If our obstacle is off the screen we will remove it
				destroyObjects.pop(destroyObjects.index(obj))

		for portal in speedPortals:
			portal["x"] -= (speed+20)*dt
			if portal["x"] < PORTALS[portal["type"]].get_rect().width * -1:
				speedPortals.pop(speedPortals.index(portal))

		if flip_gravity == False:
			if jump == True and player.rect.top > 10:
				vel_y = -6
				jump = False
			if vel_y == 3 and jump == True:
				vel_y = -6
				jump = False
			if disableCollisions == False:
				if player.rect.top > 420:
					pygame.event.post(pygame.event.Event(player_dead))
				if player.rect.top < 22:
					pygame.event.post(pygame.event.Event(player_dead))

			vel_y += GRAVITY * 2
			if vel_y > 3:
				vel_y = 3
			dy += vel_y

			player.rect.y += dy
		elif flip_gravity == True:
			if jump == True and player.rect.top > 10:
				vel_y = -6
				jump = False
			if vel_y == 3 and jump == True:
				vel_y = -6
				jump = False
			if disableCollisions == False:
				if player.rect.top > 420:
					pygame.event.post(pygame.event.Event(player_dead))
				if player.rect.top < 22:
					pygame.event.post(pygame.event.Event(player_dead))

			vel_y += GRAVITY * 2
			if vel_y > 3:
				vel_y = 3
			dy += vel_y

			player.rect.y -= dy

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			pygame.quit()
			
		if activeScreen == "startScreen":
			pass
			
		if activeScreen == "playScreen":
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE or event.key == pygame.K_w:
					jump = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				jump = True
			if pygame.mouse.get_pressed()[0]:
				jump = True
			if event.type == pygame.USEREVENT+1:
				r = random.randrange(0,8)
				if r == 0:
					img = pygame.transform.scale2x(pygame.image.load(decor_objs[0]))
					stars.append([img, [730, 50]])
				if r == 1:
					img = pygame.transform.scale2x(pygame.image.load(decor_objs[0]))
					stars.append([img, [730, 400]])
				if r == 2:
					img = pygame.transform.scale2x(pygame.image.load(decor_objs[1]))
					stars.append([img, [730, 50]])
				if r == 3:
					img = pygame.transform.scale2x(pygame.image.load(decor_objs[1]))
					stars.append([img, [730, 400]])
				if r == 4:
					img = pygame.image.load(decor_objs[2])
					stars.append([img, [730, 50]])
				if r == 5:
					img = pygame.image.load(decor_objs[2])
					stars.append([img, [730, 400]])
				if r == 6:
					img = pygame.image.load(decor_objs[3])
					stars.append([img, [730, 50]])
				if r == 7:
					img = pygame.image.load(decor_objs[3])
					stars.append([img, [730, 400]])
			
			if event.type == player_dead:
				lose_sound.play()
				player.img = pygame.transform.scale(pygame.image.load("drifter-dead.png"), (60, 60))
				screen.fill((0,0,0))
				activeScreen = "endScreen"

			if event.type == pygame.USEREVENT+3:
				speedPortals.append({"x":730, "y":250, "type":random.choice(randomPortalTypes)})

			if event.type == pygame.USEREVENT+4:
				for x in range(8):
					t = random.choice([50, 100, 130])
					destroyObjects.append({"x":730+(600*x), "y":t})
					
			if event.type == pygame.USEREVENT+5:
				for x in range(8):
					t = random.choice([350, 400, 340])
					destroyObjects.append({"x":730+(600*x), "y":t})

            

	if activeScreen == "playScreen":
        # drawing background
		for i in range(0, tiles):
		    screen.blit(bg, (i * bg_width + scroll, 0))
		    bg_rect.x = i * bg_width + scroll
        # generating star decoration
		for star in stars:
			screen.blit(star[0], star[1])
        # collidables
		if disableCollisions == False:
			for object in destroyObjects:
				if player.rect.colliderect(pygame.Rect(object["x"], object["y"], destroyObj.get_rect().width, destroyObj.get_rect().height)):
					pygame.event.post(pygame.event.Event(player_dead))
		for object in destroyObjects:
			screen.blit(destroyObj, (object["x"], object["y"]))
		for portal in speedPortals:
			if player.rect.colliderect(pygame.Rect(portal["x"], portal["y"], PORTALS[portal["type"]].get_rect().width, PORTALS[portal["type"]].get_rect().height)):
				if portal["type"] == "x2":
					speed = 300
					speedBoost = 0.20 
				if portal["type"] == "x1":
					speed = normSpeed
					speedBoost = 0.10
				if portal["type"] == "x0":
					speed = normSpeed/2
					speedBoost = 0.05
				if portal["type"] == "x5":
					speed = 400
					speedBoost = 0.30
				if portal["type"] == "x8":
					speed = 600
					speedBoost = 0.40
				if portal["type"] == "x12":
					speed = 900
					speedBoost = 0.55
				if portal["type"] == "inverted":
					flip_gravity = True
				if portal["type"] == "normal":
					flip_gravity = False

		if showHitboxes == True:
			pygame.draw.line(screen, (0,255,0), (0, player.rect.centery), (player.rect.centerx, player.rect.centery+dy), width=5)
			pygame.draw.line(screen, (0,255,0), (0, 480), (700, 480), width=5)
			pygame.draw.line(screen, (0,255,0), (0, 27), (700, 27), width=5)
			for object in destroyObjects:
				pygame.draw.rect(screen, (0,255,0), pygame.Rect(object["x"], object["y"], destroyObj.get_rect().width, destroyObj.get_rect().height), width=1)
			pygame.draw.rect(screen, (0,255,0), player.rect, width=1)
        # UI 
		screen.blit(distance_txt, (0,0))
		screen.blit(time_txt, (distance_txt.get_width() + get_text_width("gamefont.ttf", str(round(playerX)) + "m", 25)/2 + time_txt.get_width()/2 + 10, 0))
		time_txt_x = distance_txt.get_width() + get_text_width("gamefont.ttf", str(round(playerX)) + "m", 25)/2 + time_txt.get_width()/2 + 10
		draw_text(screen, "gamefont.ttf", str(round(playerX)) + "m", 25, (0,0,0), (distance_txt.get_width() + get_text_width("gamefont.ttf", str(round(playerX)) + "m", 25)/2, 15), (255,255,255))
		draw_text(screen, "gamefont.ttf", str(round(seconds)) + "s", 25, (0,0,0), (time_txt_x + time_txt.get_width() + get_text_width("gamefont.ttf", str(round(seconds)) + "s", 25)/2 + 10, 15), (255,255,255))
		# draw player
		player.draw(screen)
		for portal in speedPortals:
			screen.blit(PORTALS[portal["type"]], (portal["x"], portal["y"]))
		pygame.display.update()
	if activeScreen == "startScreen":
		screen.blit(bg, (0, 0))
		screen.blit(banner, (sw/2 - (banner.get_rect().width/2) - 25, 75))
		if play_btn.draw(screen):
			activeScreen = "playScreen"
		pygame.display.update()
	if activeScreen == "endScreen":
		screen.blit(bg_lose, (0, 0))
		draw_text(screen, "gamefont.ttf", f"SCORE: {round(playerX, 2)}m", 25, (255,255,255), (bg_lose.get_rect().centerx+10, 50))
		if restart_btn.draw(screen):
			activeScreen = "playScreen"
			flip_gravity = False
			dt = time.time() - prev_time
			prev_time = now
			start_ticks=pygame.time.get_ticks()
			seconds=(pygame.time.get_ticks()-start_ticks)/1000
			timer += dt
			playerX = 0
			speed = normSpeed
			speedBoost = 0.10
			stars = []
			destroyObjects = []
			speedPortals = []
			player = Drifter(50, sh/2-25)
		if menu_btn.draw(screen):
			activeScreen = "startScreen"
			flip_gravity = False
			dt = time.time() - prev_time
			prev_time = now
			start_ticks=pygame.time.get_ticks()
			seconds=(pygame.time.get_ticks()-start_ticks)/1000
			timer += dt
			playerX = 0
			speed = normSpeed
			speedBoost = 0.10
			stars = []
			destroyObjects = []
			speedPortals = []
			player = Drifter(50, sh/2-25)
		pygame.display.update()
		
				
  
            
