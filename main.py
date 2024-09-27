import pygame
from pygame.locals import *
from random import *
from datetime import date
import json
import os
import argparse
import sys

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("Cosmic Duel.mp3")
pygame.mixer.music.play(-1)


RED = (200, 25, 25)
BLACK = (0,0,0)
BEIGE = (245, 245, 220)
YELLOW = (250, 200, 20)

if not os.path.exists('best_scores.txt'):
	with open('best_scores.txt', 'w') as file:
		json.dump([], file)

with open('best_scores.txt', 'r') as file:
	best_scores = json.load(file)

record = 1000
for score in best_scores:
	if int(score[1]) < record:
		record = int(score[1])

today = str(date.today())

parser = argparse.ArgumentParser(description="Lire un fichier texte.")

parser.add_argument("filename", help="Le nom du fichier à ouvrir")

args = parser.parse_args()

if not args.filename.lower().endswith('.txt'):
	print(f"Erreur : '{args.filename}' n'est pas un fichier .txt.")
	continuer = False
else:
	try:
		with open(args.filename, 'r') as file:
			list = [line.strip() for line in file.readlines() if line.strip()]
			continuer = True
	except FileNotFoundError:
		print(f"Le fichier '{args.filename}' n'existe pas.")
		continuer = False

def draw_hangman(fenetre, penalties):
    if penalties > 0:
        pygame.draw.line(fenetre, BLACK, (50, 520), (140, 520), 8)
    if penalties > 2:
        pygame.draw.line(fenetre, BLACK, (75, 520), (75, 230), 8)
    if penalties > 4:
        pygame.draw.line(fenetre, BLACK, (75, 230), (250, 230), 8)
    if penalties > 6:
        pygame.draw.line(fenetre, BLACK, (130, 230), (75, 280), 8)
    if penalties > 8:
        pygame.draw.line(fenetre, BLACK, (250, 230), (250, 270), 8)
    if penalties > 10:
        pygame.draw.circle(fenetre, BLACK, (250, 285), 17)
    if penalties > 12:
        pygame.draw.line(fenetre, BLACK, (250, 300), (250, 355), 8)
    if penalties > 14:
        pygame.draw.line(fenetre, BLACK, (250, 300), (225, 330), 8)
    if penalties > 16:
        pygame.draw.line(fenetre, BLACK, (250, 300), (275, 330), 8)
    if penalties > 18:
        pygame.draw.line(fenetre, BLACK, (250, 355), (225, 400), 8)
    if penalties > 20:
        pygame.draw.line(fenetre, BLACK, (250, 355), (275, 400), 8)

def hidden_word(word):
	return ["_ "] * len(word)

def occurences(word, guess):
	occ = []
	for i in range(len(word)):
		if guess == word[i]:
			occ.append(i)
	return occ

n = randint(0,len(list)-1)
word = list[n].lower()
secret_word = hidden_word(word)
penalties = 0

screen_width, screen_height = 600, 600
screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)

background_image = pygame.image.load("bg_game.jpg").convert()

def resize_background(screen_width, screen_height):
    return pygame.transform.scale(background_image, (screen_width, screen_height))

scaled_background = resize_background(screen_width, screen_height)


visuel = ""
for i in range(len(secret_word)) :
	visuel = visuel + secret_word[i]
message = ""
letter_pressed = ""
user_input = ""
input_active = False
input_rect = pygame.Rect(screen_width // 2 - 150, 350, 300, 50)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
				with open('best_scores.txt', 'w') as file:
       					json.dump(best_scores, file)
				running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = event.pos
			if retry_rect.collidepoint(mouse_pos):
				n = randint(0,len(list)-1)
				word = list[n].lower()
				secret_word = hidden_word(word)
				letter_pressed = ""
				penalties = 0
				visuel = ""
				message = ""
				for i in range(len(secret_word)) :
					visuel = visuel + secret_word[i]
			if guess_a_word_rect.collidepoint(mouse_pos) and message == "":
				 input_active = True

		elif penalties > 20 : 
			message = "You lost !"

		elif word.upper() == visuel :
			message = "Victory !"
			if penalties < record :
				best_scores.append([today, penalties])
				record = penalties

		elif input_active:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:  # Quand l'utilisateur appuie sur "Entrée"
					if user_input.lower() == word:
						visuel = word.upper()
						message = "Victory!"
						if penalties < record:
							best_scores.append([today, penalties])
							record = penalties
					else:
						penalties += 5  # Pénalité pour une mauvaise réponse
					user_input = ""  # Réinitialiser l'entrée
					input_active = False  # Désactiver le champ de saisie

				elif event.key == pygame.K_BACKSPACE:  # Gérer la touche "Retour arrière"
					user_input = user_input[:-1]
				else:
					user_input += event.unicode  # Ajouter le caractère à l'entrée

		elif event.type == pygame.KEYDOWN:
			if pygame.K_a <= event.key <= pygame.K_z:
				letter_pressed = chr(event.key)
				letter_pressed = letter_pressed.upper()
				occ = []
				for i in range(len(word)):
					if str(letter_pressed.lower()) == word[i]:
						occ.append(i)
				if occ == [] :
					penalties = penalties +3
				else :
					penalties = penalties +1
				count = len(occ)
				for i in occ:
					secret_word[i] = str(letter_pressed)
				visuel = ""
				for i in secret_word :
					visuel = visuel + i

	screen.blit(background_image, (0, 0))

	font = pygame.font.Font(None, 50)
	font2 = pygame.font.Font(None, 80)
	font3 = pygame.font.Font(None, 150)
	text = font2.render(visuel, True, BLACK)
	text_rect = text.get_rect(center=(screen_width // 2, 150))
	screen.blit(text, text_rect)
	retry = font.render(" New game ", True, BLACK)
	retry_rect = retry.get_rect(topleft=(20, 20))
	pygame.draw.rect(screen, BEIGE, retry_rect, border_radius=10)
	screen.blit(retry, retry_rect)
	best = font.render("Best score " + str(record), True, BLACK)
	best_rect = best.get_rect(topright=(580, 20))
	screen.blit(best, best_rect)
	guess = font.render("Guess " + letter_pressed, True, BLACK)
	guess_rect = guess.get_rect(center=(420, 330))
	screen.blit(guess, guess_rect)
	pen = font.render("Attemps " + str(penalties), True, BLACK)
	pen_rect = pen.get_rect(center=(420, 420))
	screen.blit(pen, pen_rect)
	draw_hangman(screen, penalties)
	endgame = font3.render(message, True, RED)
	endgame_rect = endgame.get_rect(center=(screen_width // 2, screen_height // 2))
	screen.blit(endgame, endgame_rect)
	guess_a_word = font.render(" Guess a word ", True, BLACK)
	guess_a_word_rect = guess_a_word.get_rect(center=(420, 510))
	pygame.draw.rect(screen, YELLOW, guess_a_word_rect, border_radius=10)
	screen.blit(guess_a_word, guess_a_word_rect)

	if input_active:
		pygame.draw.rect(screen, BEIGE, input_rect, border_radius=5)
		input_surface = font.render(user_input.upper(), True, BLACK)
		screen.blit(input_surface, (input_rect.x + 10, input_rect.y + 10))

	pygame.display.flip()
pygame.quit()
sys.exit()
