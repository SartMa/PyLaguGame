import pygame
from support import import_folder
import time
from math import sqrt
from healthbar import Healthbar

class Enemy(pygame.sprite.Sprite):
	def __init__(self, pos, path, type):
		super().__init__()
		self.path = path
		self.type = type
		self.import_character_assets()
		self.frame_index=0
		self.animation_speed=0.15
		self.image = self.animations['run'][self.frame_index]
		# self.rect=self.image.get_rect(bottomleft= pos)
		# self.hitbox=pygame.Rect(self.rect.x+56, self.rect.y, 80, 93)


		# self.speed=1
		# self.health=30
		# self.damage=7.5

		self.status='run'
		self.attacking=False
		# self.attack_radius=92
		self.facing_right=True
		self.can_attack = True
		self.hasattacked=False
		self.taking_damage=False
		self.dead=False



		# self.healthbar=pygame.sprite.GroupSingle()
		# h=Healthbar(self, (self.rect.x+75, self.rect.y-30))
		# self.healthbar.add(h)

	def import_character_assets(self):
		self.animations={'idle':[], 'run':[], 'kill':[], 'takehit':[], 'attack':[]}
		for animation in self.animations.keys():
			full_path = self.path+ '/' + animation
			self.animations[animation]=import_folder(full_path, self.type)

	def animate(self):
		animation = self.animations[self.status]

		self.frame_index+=self.animation_speed
		if self.frame_index >= len(animation):
			if self.attacking:
				self.status='idle'
				self.startidle=pygame.time.get_ticks()
				self.attacking = False
			if self.status=='takehit':
				self.status='idle'
				self.taking_damage=False
				self.can_attack=True
			if self.status=='kill':
				self.frame_index=len(animation)-1
			if not self.dead:
				self.frame_index=0

		image=animation[int(self.frame_index)]
		if not self.facing_right:
			self.image=image
		else:
			flipped_image=pygame.transform.flip(image, True, False)
			self.image=flipped_image
		
		

	def get_status(self, player, idletime):
		distx = player.rect.centerx- self.rect.centerx
		disty = player.rect.centery - self.rect.centery

		distance = sqrt(distx**2 + disty**2)
		if self.status=='idle':
			current_time=pygame.time.get_ticks()
			if current_time - self.startidle > idletime:
				self.can_attack = True
				self.hasattacked=False
			if self.taking_damage:
				self.status='takehit'
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
			if self.status!='kill':
				self.frame_index=0
			self.status='kill'

	def move(self, world_shift):
		self.rect.x+=self.speed
		self.rect.x+=world_shift
		
	def reverse(self):
		if self.facing_right:
			self.facing_right = False
		else:
			self.facing_right = True
		self.speed *= -1

	def update(self, world_shift, player):
		self.get_status(player, self.idletime)
		self.move(world_shift)
		self.animate()
		# self.healthbar.sprite.update((self.rect.x ,self.rect.y))
		self.hitbox=pygame.Rect(self.rect.x ,self.rect.y, 104, 93)

class Boss(Enemy):
	def __init__(self, pos):
		super().__init__(pos, '/home/sarthak/Programming/PyLagu/level/graphics/enemy1/PNG files', 'boss')
		self.rect=self.image.get_rect(bottomleft= pos)
		self.hitbox=pygame.Rect(self.rect.x+41, self.rect.y, 104, 93)
		self.name = 'boss'

		self.speed=1000
		self.health=50
		self.damage=7.5
		self.attack_radius = 92

		self.healthbar=pygame.sprite.GroupSingle()
		self.h=Healthbar(self, 'boss', (self.rect.x+75, self.rect.y-30))
		self.healthbar.add(self.h)
		self.idletime=500

	def get_status(self, player, idletime):
		return super().get_status(player, self.idletime)

	def update(self, world_shift, player):
		if self.dead:
			self.healthbar.sprite.kill()
		if not self.dead:
			self.healthbar.sprite.update((self.rect.x+75 ,self.rect.y-30))
		self.hitbox=pygame.Rect(self.rect.x+41, self.rect.y, 104, 93)
		return super().update(world_shift, player)

class Eye(Enemy):
	def __init__(self, pos):
		super().__init__(pos, '/home/sarthak/Programming/PyLagu/level/graphics/Monster/eye', 'eye')
		self.rect=self.image.get_rect(bottomleft= pos)
		self.hitbox=pygame.Rect(self.rect.x+56, self.rect.y, 80, 93)
		self.name = 'eye'

		self.speed=2
		self.health=10
		self.damage=2.5
		self.attack_radius = 50
		self.idletime=2000

		self.healthbar=pygame.sprite.GroupSingle()
		self.h=Healthbar(self, 'eye', (self.rect.x+75, self.rect.y-30))
		self.healthbar.add(self.h)

	def get_status(self, player, idletime):
		return super().get_status(player, self.idletime)
	
	def update(self, world_shift, player):
		if self.dead:
			self.h.kill()
		if not self.dead:
			self.healthbar.sprite.update((self.rect.x+10 ,self.rect.y-30))
		return super().update(world_shift, player)
	
class Skeleton(Enemy):
	def __init__(self, pos):
		super().__init__(pos, '/home/sarthak/Programming/PyLagu/level/graphics/Monster/Skeleton', 'skeleton')
		self.rect=self.image.get_rect(bottomleft= pos)
		self.hitbox=pygame.Rect(self.rect.x+43, self.rect.y, 50, 56)
		self.name = 'skeleton'

		self.speed=2
		self.health=30
		self.damage=7.5
		self.attack_radius = 68
		self.idletime=1500

		self.healthbar=pygame.sprite.GroupSingle()
		self.h=Healthbar(self, 'skeleton', (self.rect.x+75, self.rect.y-30))
		self.healthbar.add(self.h)
	
	# def get_status(self):
	# 	return super().get_status()
	
	def update(self, world_shift, player):
		if self.dead:
			self.h.kill()
		if not self.dead:
			self.healthbar.sprite.update((self.rect.x+75 ,self.rect.y-30))
		return super().update(world_shift, player)
