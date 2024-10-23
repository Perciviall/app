from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def encrypt_caesar(text, key):
    """Encrypts a given plaintext using the Caesar cipher with the specified key."""
    encrypted_text = ''  # Initialize the encrypted text as an empty string
    alphabet = 'abcdefghijklmnopqrstuvwxyz'  # Lowercase alphabet
    Alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Uppercase alphabet
    number = '0123456789'  # String of digits
    key_alpha = int(key) % 26  # Normalize the key for alphabetic shifting
    key_num = int(key) % 10  # Normalize the key for numeric shifting
    
    for char in text:  # Iterate through each character in the plaintext
        if char.isalpha():  # Check if the character is an alphabetic letter
            if char.isupper():  # If the character is uppercase
                location = (Alphabet.find(char) + key_alpha) % 26  # Calculate new character location
                encrypted_text += Alphabet[location]  # Add the encrypted character to the new text
            else:  # If the character is lowercase
                location = (alphabet.find(char) + key_alpha) % 26  # Calculate new character location
                encrypted_text += alphabet[location]  # Add the encrypted character to the new text
        elif char.isdigit():  # Check if the character is a digit
            location = (number.find(char) + key_num) % 10  # Calculate new digit location
            encrypted_text += number[location]  # Add the encrypted digit to the new text
        else: 
            encrypted_text += char  # Non-alphabetic characters are added unchanged
    return encrypted_text  # Return the encrypted message


@app.route('/encrypt', methods=['POST'])
def encrypt():
    cipher = request.form['cipher']
    text = request.form['text']
    key = request.form['key']
    start_sequence = request.form['start_sequence']
    end_sequence = request.form['end_sequence']
    bit_offset = request.form['bit_offset']
    encoded_name = request.form['encoded_name']

    #Placeholder for actual encryption logic based on the selected cipher
    encrypted_text = ""

    try:
        if cipher == 'caesar':
            encrypted_text = encrypt_caesar(text, key)
        
        elif cipher == 'xor':
            #XOR cipher encryption logic
            encrypted_text = 'Xor Encryption not implemented'

        elif cipher == 'vigenere':
            # Implement Vigenère cipher encryption logic
            encrypted_text = "Vigenère encryption not implemented"
        
        else: 
            encrypted_text = 'Cipher not recognized'

    except ValueError:
        encrypted_text = 'Error: Invalid key for selected cipher. Please ensure the key is numeric for Caesar cipher.'

    return render_template('index.html', encrypted_text = encrypted_text)
    
if __name__ == '__main__':
    app.run(debug=True)
