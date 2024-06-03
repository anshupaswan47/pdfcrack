import itertools
import pikepdf
import string

def generate_passwords(start_length, end_length, charset):
    for length in range(start_length, end_length + 1):
        for combination in itertools.product(charset, repeat=length):
            yield "".join(combination)

def crack_pdf_char(input_pdf, output_pdf, start_length, end_length, use_numeric, use_alpha, use_symbols):
    charset = ""
    if use_numeric:
        charset += string.digits
    if use_alpha:
        charset += string.ascii_letters
    if use_symbols:
        charset += string.punctuation
    
    if not charset:
        print("No character set selected.")
        return False
    
    passwords = generate_passwords(start_length, end_length, charset)
    
    for password in passwords:
        try:
            with pikepdf.open(input_pdf, password=password) as pdf:
                pdf.save(output_pdf)
            print(f"Password cracked: {password}")
            return True
        except :
            print(f"Incorrect: {password}")
    print("Unable to crack PDF with provided password range.")
    return False

def crack_pdf_word(input_pdf, output_pdf, wordlist=None):
    if wordlist:
        with open(wordlist, encoding='utf-8') as f:
            passwords = [line.strip() for line in f]
    else:
        print("No wordlist provided.")
        return False
    
    for password in passwords:
        try:
            with pikepdf.open(input_pdf, password=password) as pdf:
                pdf.save(output_pdf)
            print(f"Password cracked: {password}")
            return True
        except :
            print(f"Incorrect: {password}")
    print("Unable to crack PDF with provided wordlist.")
    return False

def crack_pdf_len(input_pdf, output_pdf, start_range, end_range):
    for password in range(start_range, end_range + 1):
        try:
            with pikepdf.open(input_pdf, password=str(password)) as pdf:
                pdf.save(output_pdf)
            print(f"Password cracked: {password}")
            return True
        except :
            print(f"Incorrect: {password}")
    print("Unable to crack PDF with provided password range.")
    return False

def get_input(prompt, default=None):
    response = input(prompt)
    return response if response else default

# Usage example
input_pdf = "test.pdf"
output_pdf = "cracked_file.pdf"

wordlist = get_input("Enter the path to the wordlist file (leave empty if not using): ")
if wordlist:
    crack_pdf_word(input_pdf, output_pdf, wordlist)

try:
    start_length = int(get_input("Enter start length: "))
    end_length = int(get_input("Enter end length: "))
except (ValueError, TypeError):
    start_length = end_length = None

if start_length and end_length and end_length > 12:
    crack_pdf_len(input_pdf, output_pdf, start_length, end_length)

use_numeric = get_input("Include numeric characters? (y/n): ").lower() == 'y'
use_alpha = get_input("Include alphabetic characters? (y/n): ").lower() == 'y'
use_symbols = get_input("Include symbols? (y/n): ").lower() == 'y'

if use_alpha or use_numeric or use_symbols:
    crack_pdf_char(input_pdf, output_pdf, start_length, end_length, use_numeric, use_alpha, use_symbols)
