import pygame
import pygame.display
from pygame.locals import *

import glm

from gl import Renderer
from buffer import Buffer
from model import Model
from vertexShaders import *
from fragmentShaders import *

width = 1200
height = 640

deltaTime = 0.0


screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()


rend = Renderer(screen)
rend.pointLight = glm.vec3(1,1,1)

currVertexShader = vertex_shader
currFragmentShader = fragment_shader

rend.SetShaders(currVertexShader, currFragmentShader)

skyboxTextures = ["skybox/right.jpg",
				  "skybox/left.jpg",
				  "skybox/top.jpg",
				  "skybox/bottom.jpg",
				  "skybox/front.jpg",
				  "skybox/back.jpg"]

rend.CreateSkybox(skyboxTextures)


faceModel = Model("model.obj")
# Las texturas se cargan automáticamente desde el archivo .mtl si existe
# Si quieres usar texturas manuales, descomenta las siguientes líneas:
# if len(faceModel.textures) == 0:
# 	faceModel.AddTexture("textures/lava_cracks.jpg")

faceModel.position.x = 0
faceModel.position.y = -2
faceModel.position.z = -12
faceModel.scale = glm.vec3(0.05, 0.05, 0.05)

rend.scene.append(faceModel)

print("\n" + "="*60)
print("CONTROLES DE SHADERS")
print("="*60)
print("\nFragment Shaders:")
print("  1 - Basic Lighting")
print("  2 - Rainbow/Gradient (NUEVO)")
print("  3 - Cosmic Shader (NUEVO) - Galaxia con nebulosas y estrellas")
print("  4 - Procedural Pattern (NUEVO)")
print("\nVertex Shaders:")
print("  7 - Standard")
print("  8 - Directional Fold (NUEVO) - Doblez como papel arrugado")
print("  9 - Wave (NUEVO)")
print("  0 - Vortex (NUEVO) - Efecto de remolino/torbellino")
print("\nOtros controles:")
print("  F - Toggle Wireframe/Filled")
print("  Z/X - Ajustar value (intensidad de efectos)")
print("  Flechas - Mover cámara")
print("  W/A/S/D/Q/E - Mover luz")
print("="*60 + "\n")

isRunning = True

while isRunning:

	deltaTime = clock.tick(60) / 1000

	rend.elapsedTime += deltaTime

	keys = pygame.key.get_pressed()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_f:
				rend.ToggleFilledMode()

			# Fragment Shaders
			if event.key == pygame.K_1:
				currFragmentShader = fragment_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
				print("Fragment: Basic Lighting")

			if event.key == pygame.K_2:
				currFragmentShader = rainbow_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
				print("Fragment: Rainbow/Gradient (NUEVO)")

			if event.key == pygame.K_3:
				currFragmentShader = cosmic_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
				print("Fragment: Cosmic Shader (NUEVO) - Galaxia con nebulosas y estrellas")

			if event.key == pygame.K_4:
				currFragmentShader = pattern_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
				print("Fragment: Procedural Pattern (NUEVO)")
			
			# Vertex Shaders
			if event.key == pygame.K_7:
				currVertexShader = vertex_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
				print("Vertex: Standard")


			if event.key == pygame.K_8:
				currVertexShader = twist_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
				print("Vertex: Directional Fold (NUEVO) - Doblez como papel arrugado")
			
			if event.key == pygame.K_9:
				currVertexShader = wave_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
				print("Vertex: Wave (NUEVO)")
			
			if event.key == pygame.K_0:
				currVertexShader = jitter_shader
				rend.SetShaders(currVertexShader, currFragmentShader)
				print("Vertex: Vortex (NUEVO) - Efecto de remolino/torbellino")
	if keys[K_UP]:
		rend.camera.position.z -= 5 * deltaTime

	if keys[K_DOWN]:
		rend.camera.position.z += 5 * deltaTime

	if keys[K_RIGHT]:
		rend.camera.position.x += 5 * deltaTime

	if keys[K_LEFT]:
		rend.camera.position.x -= 5 * deltaTime



	if keys[K_w]:
		rend.pointLight.z -= 10 * deltaTime

	if keys[K_s]:
		rend.pointLight.z += 10 * deltaTime

	if keys[K_a]:
		rend.pointLight.x -= 10 * deltaTime

	if keys[K_d]:
		rend.pointLight.x += 10 * deltaTime

	if keys[K_q]:
		rend.pointLight.y -= 10 * deltaTime

	if keys[K_e]:
		rend.pointLight.y += 10 * deltaTime


	if keys[K_z]:
		if rend.value > 0.0:
			rend.value -= 1 * deltaTime

	if keys[K_x]:
		if rend.value < 1.0:
			rend.value += 1 * deltaTime



	# faceModel.rotation.y += 45 * deltaTime


	rend.Render()
	pygame.display.flip()

pygame.quit()