import random
from itertools import zip_longest

from util import correct_letter, present_letter, absent_letter, blue, red, cyan, black, green


class Wordle:
    total_number_of_guesses = 6
    current_number_of_guesses = 0

    accepted_words = []
    probable_words = []

    green_letter_guesses = set()
    yellow_letter_guesses = set()
    red_letter_guesses = set()

    alphabets = set("abcdefghijklmnopqrstuvwxyz")

    current_guess = ""

    def __init__(self, accepted_file, probable_file, max_tries=6):
        with open(accepted_file) as accepted_file, open(probable_file) as probable_file:
            self.accepted_words = list(map(str.strip, accepted_file.readlines()))
            self.probable_words += list(map(str.strip, probable_file.readlines()))
        self.max_tries = max_tries
        self.word = self._generate_word()

    def _generate_word(self):
        return random.choice(self.probable_words)

    def _print_welcome_msg(self):
        print(cyan("WELCOME TO WORDLE"))
        print(cyan("------------------"))
        print(cyan("HOW TO PLAY"))
        print(cyan(f"Guess the wordle in {self.max_tries} guesses"))
        print(cyan("• Each guess must be a valid 5 letter word"))
        print(cyan("• The color of the letter change to show how close your guess was to the word"))
        print()
        print(cyan("EXAMPLES"))
        print(correct_letter("w") + " e  a  r  y ")
        print(cyan("w is in the word in the correct spot"))
        print(" p " + present_letter("i") + " l  l  s ")
        print(cyan("i is in the word but in the wrong spot"))
        print(" v  a  g " + absent_letter("u") + " e ")
        print(cyan("u is not in the word in any spot"))
        print()

    def th_suffix(self, i):
        if i == 1:
            return "st"
        elif i == 2:
            return "nd"
        elif i == 3:
            return "rd"
        else:
            return "th"

    def _print_remaining_letters(self):
        print(blue(f"Remaining letters::"))
        for letter in sorted(self.alphabets):
            if letter in self.green_letter_guesses:
                print(correct_letter(letter), end=" ")
            elif letter in self.yellow_letter_guesses:
                print(present_letter(letter), end=" ")
            elif letter in self.red_letter_guesses:
                print(absent_letter(letter), end=" ")
            else:
                print(letter, end=" ")
        print()

    def _print_validated_guess(self, current_guess):
        validated_guess = []
        for i, letter in enumerate(current_guess):
            if letter in self.word and self.word[i] == letter:
                validated_guess.append(correct_letter(letter))
                self.green_letter_guesses.add(letter)
            elif letter in self.word:
                validated_guess.append(present_letter(letter))
                self.yellow_letter_guesses.add(letter)
            else:
                validated_guess.append(absent_letter(letter))
                self.red_letter_guesses.add(letter)
        print(blue(f"You guessed::"))
        print(' '.join(validated_guess))
        print()

    def _pad(self, text, length, pad_character="_"):
        return text.ljust(length, pad_character)

    def _print_current_guess(self):
        print(blue(f"Your current guess:"))
        print(self._pad(self.current_guess, 5))

    def _process_input(self, input_word):
        if input_word == "clear":
            print(blue("resetting"))
            self.current_guess = ""
            self._print_current_guess()
        elif input_word == "del":
            if self.current_guess:
                self.current_guess = self.current_guess[:-1]
            self._print_current_guess()
        elif input_word == "exit":
            print(blue(f"The word was >>> {self.word} <<<"))
            print()
            return False
        elif len(input_word) > 1:
            print(red("Please type one letter at a time"))
        elif input_word in self.red_letter_guesses:
            print(red("Invalid letter, already guessed"))
            self._print_remaining_letters()
        else:
            self.current_guess += input_word
            self._print_current_guess()
        return True

    def run(self):
        self._print_welcome_msg()
        self.word = self._generate_word()
        guess_count = 0

        while guess_count <= self.max_tries:
            self.current_guess = ""
            while len(self.current_guess) < 5:
                j = len(self.current_guess) + 1
                th_suffix = self.th_suffix(j)
                input_word = input(blue(f"Enter the {j}{th_suffix} letter of your guess:\n")).lower().strip()
                print()
                if not self._process_input(input_word):
                    return False
                print()

            if self.current_guess not in self.accepted_words and self.current_guess not in self.probable_words:
                print(red(f"'{self.current_guess}' is not a valid word"))
                continue

            self._print_validated_guess(self.current_guess)

            if self.current_guess == self.word:
                print(green("Hurray !!!! You won!!!✓ (❁´◡`❁)"))
                print()
                return True

            guess_count += 1
            print(blue(f"{self.max_tries - guess_count} guesses remaining\n"))

            self._print_remaining_letters()
            print()

        return False


if __name__ == '__main__':
    wordle = Wordle("accepted.csv", "probable.csv")
    wordle.run()
    print(f"Thank you for playing")
