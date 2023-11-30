import pygame 
from tiles import AnimatedTile, Tiles
from random import randint
from settings import tile_size
from support import import_folder

class Enemy1(Tiles):
	def __init__(self, size, x, y, path, enemy):
		super().__init__(size, x, y-100)
		self.state = 'idle'
		self.can_attack = True
		self.rect.y += size - self.image.get_size()[1]
		self.direction = 1
		self.speed = self.direction*1

		self.prev_speed = 0
		self.reverse_by_constraint = False
		#Attack
		self.attack_radius = 20
		self.notice_radius = 40
		self.attack_time = None
		self.cooldown = 5000

		self.frame_index = 0
		self.states = {'idle':[], 'run':[], 'attack':[], 'kill':[], 'takehit':[]}
		for animation in self.states.keys():
			full_path = path + '/Monster/'+ enemy + '/' +animation
			self.states[animation]=import_folder(full_path, enemy)
		self.image = self.states[self.state][self.frame_index]
    
	def animate(self, state='idle'):
		self.state = state
		frames = self.states[self.state]
		self.frame_index += 0.15
		if self.frame_index >= len(frames):
			self.frame_index = 0
		self.image = frames[int(self.frame_index)]
	
	def move(self):
		self.rect.x += self.speed

	def reverse_image(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image,True,False)

	def reverse(self):
		self.direction *= -1
		# self.image = pygame.transform.flip(self.image,True,False)

	def collison(self):
		if self.rect.x == 0:
			self.reverse_image()
			self.reverse()

	def get_player_distance(self):
		enemy_pos = self.rect.centerx
		# player_pos = player.rect.center_x
		distance = pygame.mouse.get_pos()[0] - enemy_pos
		radius = abs(distance)
		return distance, radius
	
	def get_status(self):
		distance, radius = self.get_player_distance()

		if radius <= self.notice_radius:
			if distance*self.speed < 0:
				self.direction *= -1

		if radius <= self.attack_radius and self.can_attack:
			self.frame_index = 0
			self.can_attack = False
			self.state = 'attack'
		elif radius <= self.notice_radius:
			self.state = 'idle'
			self.speed = 0
		else:
			self.state = 'run'
			self.speed = self.direction*1
		
		# self.state = 'run'

	def actions(self):
		if self.state == 'attack':
			self.attack_time = pygame.time.get_ticks()
			self.speed = 0

	def cooldownfunc(self):
		if not self.can_attack:
			current_time = pygame.time.get_ticks()
			if current_time - self.attack_time >= self.cooldown:
				self.can_attack = True
				self.speed = self.direction*1
				# self.attack_time = None
			# else:
			# 	self.speed = 0

	def update(self,shift):
		self.rect.x += shift
		self.get_status()
		self.animate(self.state)
		self.move()
		self.reverse_image()
		self.collison()
		self.actions()
		self.cooldownfunc()


#size,x-7*tile_size,y+3,

# class FlyingEye(Enemy):
# 	def __init__(self, size, x, y, path):
# 		super().__init__(size, x, y, path, 'eye')

# 		#Attack
# 		self.attack_radius = 60
# 		self.notice_radius = 80
# 		# self.can_attack = False
# 		self.attack_time = None
# 		self.cooldown = 4000

# 	def get_player_distance(self):
# 		enemy_pos = self.rect.centerx
# 		# player_pos = player.rect.center_x
# 		distance = pygame.mouse.get_pos()[0] - enemy_pos

# 		radius = abs(distance)

# 		return distance, radius
	
# 	def get_status(self):
# 		distance, radius = self.get_player_distance()

# 		if radius <= self.notice_radius and radius >=20:
# 			if distance > 0 and self.speed < 0:
# 				self.reverse()
# 			elif distance < 0 and self.speed > 0:
# 				self.reverse()

# 		if radius <= self.attack_radius and self.can_attack:
# 			if self.state != 'attack':
# 				self.frame_index = 0
# 			self.state = 'attack'

# 		elif radius <= self.notice_radius:
# 			self.state = 'idle'

# 		else:
# 			self.state = 'idle'
		
# 		print(radius, self.state, self.speed)

# 	def actions(self):
# 		if self.state == 'attack':
# 			self.attack_time = pygame.time.get_ticks()
# 			print('attack')

# 		# elif self.status == 'run':
# 		# 	self.direction = self.get_player_distance_direction(player)[1]
# 		# else:
# 		# 	self.direction = pygame.math.Vector2()

# 	def cooldownfunc(self):
# 		if not self.can_attack:
# 			current_time = pygame.time.get_ticks()
# 			if current_time - self.attack_time >= self.cooldown:
# 				self.can_attack = True

# 	def update(self, shift):
# 		self.updateall(shift)
# 		self.get_status()
# 		self.actions()
# 		self.cooldownfunc()

import pygame
from support import import_folder
import time
from math import sqrt
# from healthbar import Healthbar

class Enemy(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.import_character_assets()
		self.frame_index=0
		self.animation_speed=0.15
		self.image = self.animations['run'][self.frame_index]
		self.rect=self.image.get_rect(bottomleft= pos)
		self.hitbox=pygame.Rect(self.rect.x+56, self.rect.y, 80, 93)


		self.speed=1
		self.health=30
		self.damage=7.5

		self.status='run'
		self.attacking=False
		self.attack_radius=92
		self.facing_right=True
		self.can_attack = True
		self.hasattacked=False
		self.taking_damage=False
		self.dead=False

		# self.healthbar=pygame.sprite.GroupSingle()
		# h=Healthbar(self, (self.rect.x+75, self.rect.y-30))
		# self.healthbar.add(h)

	def import_character_assets(self):
		character_path='/home/sarthak/Programming/PyLagu/level/graphics/enemy1/PNG files/'
		self.animations={'idle':[], 'run':[], 'death':[], 'takehit':[], 'attack':[]}
		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation]=import_folder(full_path)

	def animate(self):
		animation = self.animations[self.status]

		self.frame_index+=self.animation_speed
		if self.frame_index >= len(animation):
			if self.attacking:
				self.status='idle'
				self.startidle=pygame.time.get_ticks()
				self.attacking = False
			if self.status=='take_hit':
				self.status='idle'
				self.taking_damage=False
				self.can_attack=True
			if self.status=='death':
				self.frame_index=len(animation)-2
			if not self.dead:
				self.frame_index=0

		image=animation[int(self.frame_index)]
		if not self.facing_right:
			self.image=image
		else:
			flipped_image=pygame.transform.flip(image, True, False)
			self.image=flipped_image
		
		

	def get_status(self, player):
		distx = player.rect.centerx- self.rect.centerx
		disty = player.rect.centery - self.rect.centery

		distance = sqrt(distx**2 + disty**2)
		if self.status=='idle':
			current_time=pygame.time.get_ticks()
			if current_time - self.startidle > 500:
				self.can_attack = True
				self.hasattacked=False
			if self.taking_damage:
				self.status='take_hit'
				self.speed=0
				self.taking_damage=False
		if not self.attacking and self.can_attack:
			if abs(distance)< self.attack_radius:
				self.attacking = True
				self.status='attack'
				self.can_attack = False
				self.frame_index=0
				if distx*self.speed<0:
					self.facing_right=not self.facing_right
				else:
					if self.speed == 0:
						if distx>0 and not self.facing_right:
							self.facing_right=not self.facing_right
						elif distx <0 and self.facing_right:
							self.facing_right=not self.facing_right
				self.speed=0
			else:
				self.status='run'
				if self.facing_right:
					self.speed=1
				else:
					self.speed=-1
		else:
			if self.can_attack:
				self.status='run'
				if self.facing_right:
					self.speed=1
				else:
					self.speed=-1

		if self.health==0:
			self.dead=True
			if self.status!='death':
				self.frame_index=0
			self.status='death'

	def move(self, world_shift):
		self.rect.x+=self.speed
		self.rect.x+=world_shift
		if self.rect.x < 0 or self.rect.x>1100:
			self.speed*=-1
			self.facing_right= not self.facing_right
	
	def reverse(self):
		if self.facing_right:
			self.facing_right = False
		else:
			self.facing_right = True
		self.speed *= -1

	def update(self, world_shift):
		# self.get_status(player)
		self.move(world_shift)
		self.animate()
		# self.healthbar.sprite.update((self.rect.x+75 ,self.rect.y-30))
		self.hitbox=pygame.Rect(self.rect.x+41 ,self.rect.y, 104, 93)
