import random
from sympy import isprime, nextprime

def generate_prime(bits=512):
    """Generate a large prime number."""
    prime = random.getrandbits(bits)
    return nextprime(prime)

def initialize_alphabet():
    """Initialize the alphabet mapping."""
    return {char: index for index, char in enumerate(' ABCDEFGHIJKLMNOPQRSTUVWXYZ')}

def text_to_numbers(text, alphabet):
    """Convert text to a list of numbers based on the alphabet."""
    return [alphabet[char] for char in text.upper()]


def numbers_to_text(numbers, alphabet):
    """Convert a list of numbers back to text based on the alphabet."""
    inv_alphabet = {v: k for k, v in alphabet.items()}
    return ''.join(inv_alphabet.get(number, '?') for number in numbers)  # Replace '?' with any placeholder you prefer


def generate_keys():
    """Generate public and private keys."""
    p = generate_prime()
    q = generate_prime()
    n = p * q
    return n, (p, q)

def encrypt(message, public_key, alphabet):
    """Encrypt a message using the public key."""
    numbers = text_to_numbers(message, alphabet)
    return [number**2 % public_key for number in numbers]

def decrypt(ciphertext, private_key, alphabet):
    """Decrypt a ciphertext using the private key."""
    p, q = private_key
    decrypted_numbers = []
    for number in ciphertext:
        # Four possible roots
        roots = []
        m_p = pow(number, (p + 1) // 4, p)
        m_q = pow(number, (q + 1) // 4, q)
        roots.append((m_p * q * pow(q, -1, p) + m_q * p * pow(p, -1, q)) % (p * q))
        roots.append(p * q - roots[0])
        roots.append((m_p * q * pow(q, -1, p) - m_q * p * pow(p, -1, q)) % (p * q))
        roots.append(p * q - roots[2])

        # Find the first root that maps to a valid character
        found_valid_root = False
        for root in roots:
            if root in alphabet.values():
                decrypted_numbers.append(root)
                found_valid_root = True
                break

        if not found_valid_root:
            decrypted_numbers.append(0)  # Append 0 (space) if no valid root is found

    return numbers_to_text(decrypted_numbers, alphabet)


def findMissingText(text, text_list):
    """finds if a text is not in the given list"""
    for existing_text in text_list:
        if text == existing_text:
            return False
    return True

# Example usage
done = 0
while done == 0:
    try:
        decrypted_text_list = []
        plaintext = input("Enter message: ")
        emptyroot = ""
        for i in range(0,len(plaintext)):
            emptyroot += " "

        while len(decrypted_text_list)<4:
            alphabet = initialize_alphabet()
            public_key, private_key = generate_keys()

            ciphertext = encrypt(plaintext, public_key, alphabet)

            decrypted_text = decrypt(ciphertext, private_key, alphabet)

            #completes the list with the four different solutions from the roots
            if findMissingText(decrypted_text,decrypted_text_list):
                decrypted_text_list.append(decrypted_text)
            elif decrypted_text == emptyroot and emptyroot != "A":
                decrypted_text_list.append(decrypted_text)
                emptyroot = "A"


        print(f"Plaintext: {plaintext}")
        print(f"Ciphertext: {ciphertext}")
        for i in range(0,len(decrypted_text_list)):
            print(f"Decrypted text {i+1}: {decrypted_text_list[i]}")
        done = 1
    except Exception:
        print(f"{plaintext} is not valid for the encryption, try another")
