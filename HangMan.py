import random
import string
import PySimpleGUI as simple_gui
import requests


def get_random_word():
    response = requests.get('https://random-word-api.herokuapp.com/word?number=1')
    data = response.json()
    word = data[0]
    return word.upper()


def create_keyboard(word_letters, guessed_letters):
    alphabet = list(string.ascii_uppercase)
    available_letters = list(word_letters)
    word_length = len(word_letters)

    min_additional_letters = max(0, word_length - len(alphabet) + len(word_letters))
    num_unique_letters = max(min_additional_letters, 7)

    available_letters += random.sample(sorted(set(alphabet) - set(available_letters)), num_unique_letters)
    random.shuffle(available_letters)
    keyboard = []
    for letter in available_letters:
        if letter in guessed_letters:
            keyboard.append(simple_gui.Button(letter, disabled=True, size=(2, 1)))
        else:
            keyboard.append(simple_gui.Button(letter, key=letter, size=(2, 1), bind_return_key=True))
    return keyboard


def hangman():
    word = get_random_word()
    word_set = set(word)
    guessed_letters = set()
    wrong_guesses = set()
    tries = 6
    hangman_images = [
        "      _______",
        "     |/      |",
        "     |    (*_*)  ",
        "     |      \|/  ",
        "     |       |  ",
        "     |      / \  ",
        " ____|____      "
    ]
    current_stage = 0
    stages_display = [hangman_images[0]]

    layout = [
        [simple_gui.Text("Hangman", font='Arial 20')],
        [simple_gui.Multiline(stages_display[0], size=(15, 8), key='hangman_image', disabled=True)],
        [simple_gui.Text("Guess the word: ")],
        [simple_gui.Text("_ " * len(word), key='guessed_word')],
        create_keyboard(word_set, guessed_letters),
        [simple_gui.Button("Quit")]
    ]

    window = simple_gui.Window("Hangman", layout)

    while True:
        event, values = window.read()

        if event == simple_gui.WINDOW_CLOSED or event == "Quit":
            break

        guess = event

        if guess.isalpha() and len(guess) == 1:
            if guess in guessed_letters:
                simple_gui.popup("You already guessed that letter. Try again.")
            elif guess in word_set:
                guessed_letters.add(guess)
                guessed_word = ''.join([letter + ' ' if letter.upper() in guessed_letters else '_ ' for letter in word])
                window['guessed_word'].update(guessed_word)
                if guessed_letters == word_set:
                    simple_gui.popup("Congratulations! You guessed the word correctly.")
                    break
            else:
                if guess in wrong_guesses:
                    simple_gui.popup("You already guessed that letter. Try again.")
                else:
                    tries -= 1
                    wrong_guesses.add(guess)
                    if tries == 0:
                        simple_gui.popup("Game over! You ran out of tries.")
                        break
                    else:
                        simple_gui.popup("Wrong guess! Tries remaining:", tries)
                        current_stage += 1
                        stages_display.append(hangman_images[current_stage])
                        window['hangman_image'].update('\n'.join(stages_display))

            window[guess].update(disabled=True)
        else:
            simple_gui.popup("Please enter a valid letter.")

    window.close()

    return simple_gui.popup_yes_no("Do you want to play again?", title='Play Again?')


play_again = True
while play_again:
    play_again = hangman()
    if play_again == 'No':
        break
