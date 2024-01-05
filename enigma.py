import string
import random

class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard

    def set_rotor_positions(self, positions):
        for rotor, position in zip(self.rotors, positions):
            rotor.set_position(position)

    def encrypt(self, message):
        encrypted_message = ""
        for char in message.upper():
            if char in string.ascii_uppercase:
                # Rotate rotors before encryption
                self.rotate_rotors()

                # Pass through plugboard
                char = self.plugboard.get(char, char)

                # Pass through rotors
                for rotor in self.rotors:
                    char = rotor.forward(char)

                # Reflector
                char = self.reflector.reflect(char)

                # Pass back through rotors in reverse
                for rotor in reversed(self.rotors):
                    char = rotor.backward(char)

                # Pass back through plugboard
                char = self.plugboard.get(char, char)

            encrypted_message += char

        return encrypted_message
    
    def decrypt(self, message):
        decrypted_message = ""
        for char in message.upper():
            if char in string.ascii_uppercase:
                # Pass through plugboard
                char = self.plugboard.get(char, char)

                # Pass through rotors
                for rotor in self.rotors:
                    char = rotor.forward(char)

                # Reflector
                char = self.reflector.reflect(char)

                # Pass back through rotors in reverse
                for rotor in reversed(self.rotors):
                    char = rotor.backward(char)

                # Pass back through plugboard
                char = self.plugboard.get(char, char)

            decrypted_message += char

        return decrypted_message

    def rotate_rotors(self):
        # Rotate rightmost rotor every time a key is pressed
        self.rotors[-1].rotate()
        for i in range(len(self.rotors) - 1, 0, -1):
            if self.rotors[i].at_notch():
                self.rotors[i - 1].rotate()

class Rotor:
    def __init__(self, wiring, notch):
        self.wiring = wiring
        self.notch = notch
        self.position = random.choice(string.ascii_uppercase)
        self.starting_position = self.position

    def set_position(self, position):
        self.position = position
        self.starting_position = position

    def rotate(self):
        self.position = chr((ord(self.position) - ord('A') + 1) % 26 + ord('A'))

    def at_notch(self):
        return self.position == self.notch

    def forward(self, char):
        offset = (ord(char) - ord('A') + ord(self.position) - ord('A')) % 26
        return self.wiring[(offset) % 26]

    def backward(self, char):
        offset = (ord(char) - ord('A') + ord(self.position) - ord('A')) % 26
        return chr((self.wiring.index(char) - offset) % 26 + ord('A'))

class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, char):
        return self.wiring[string.ascii_uppercase.index(char)]
    


# Function to get user input and encrypt or decrypt
def get_user_input_and_process(enigma):
    choice = input("Do you want to (E)ncrypt or (D)ecrypt a message? ").upper()

    if choice == 'E':
        user_input = input("Enter a word to encrypt: ").upper()
        result = enigma.encrypt(user_input)
        print(f"Original message: {user_input}")
        print(f"Encrypted message: {result}")
    elif choice == 'D':
        user_input = input("Enter a word to decrypt: ").upper()
        result = enigma.decrypt(user_input)  # Corrected to use decrypt method
        print(f"Encrypted message: {user_input}")
        print(f"Decrypted message: {result}")
    else:
        print("Invalid choice. Please enter 'E' for encrypt or 'D' for decrypt.")
        
# Example usage:
plugboard_settings = {'A': 'B', 'C': 'D', 'E': 'F'}
rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V")
reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")

enigma = EnigmaMachine([rotor1, rotor2, rotor3], reflector, plugboard_settings)

# Set rotor starting positions (for more historical accuracy)
enigma.set_rotor_positions("ABC")

get_user_input_and_process(enigma)

# message = "HELLO"
#encrypted_message = enigma.encrypt(message)
#print(f"Original message: {message}")
#print(f"Encrypted message: {encrypted_message}")
