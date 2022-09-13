#!/usr/bin/env python3

def text_to_ascii_list(text):
    """
    Converts string into list of ascii integers
    Each integer represents one character in original string
    Input:
        text (string): the string to be converted into list of integers
    Output:
        ascii_list (list of integers): ascii values of each character in "text"
    """
    # Convert string "text" into list of characters "text_list"
    text_list = list(text)
    # Initialize list to be populated with ascii integers
    ascii_list = []
    # Iterate through "text_list" and convert each character to ascii integer
    # Populate integer_list with these values
    for character in text_list:
        ascii_number = ord(character)
        ascii_list.append(ascii_number)
    return(ascii_list)


def ascii_list_to_text(ascii_list):
    """
    Converts list of ascii integers into string
    Input:
        ascii_list (list of integers): list of ascii values
    Output:
        text (string): string of characters corresponding to ascii values
    """
    # Initialize string variable "text"
    text = ''
    # Iterate through ascii_list
    # Concatenate character corresponding to each integer to string "text"
    for value in ascii_list:
        text += chr(value)
    return(text)


def decimal_to_binary_list(decimal_num):
    """
    Converts decimal to list of bits corresponding to its binary expansion
    Input:
        decimal_num (integer): decimal integer
    Output:
        list_of_bits (list): list of bits
    """
    # Converts n from decimal number to binary expansion
    # While loop appends the binary bits of n to the list n_binary_expansion
    # After while loop, Least Significant Digit is at n_binary_expansion[0]
    # This means the order of the bits are in reverse
    # List is reversed after while loop to put bits in traditional order
    quotient = decimal_num
    list_of_bits = []
    while quotient > 0:
        bit = quotient % 2
        list_of_bits.append(bit)
        quotient = quotient // 2
    list_of_bits.reverse()
    return(list_of_bits)


def fast_modular_exp(b, n, m):
    """
    Calculates b^n mod m using fast modular exponentiation
    Input:
        b, n, m (integers): decimal integers corresponding to b^n mod m
    Output:
        result (integer): the result of b^n mod m
    """
    # n is converted to its binary expansion as a list of bits
    # n_index is a pointer used to point to each bit in this list
    # n_index is initialized to point to the rightmost bit first
    # This is the Least Significant Digit (LSD) in the binary expansion of n
    # When n_index = 0 it will point to the Most Significant Digit (MSD) of n
    n_binary_expansion = decimal_to_binary_list(n)
    n_index = len(n_binary_expansion) - 1
    # while loop iterates through each bit in the binary expansion of n
    # while loop begins with LSD
    # The variable "square" stores the values of (b^2^n_index mod m)
    # "Square" is initialized to b mod m (that is, b^2^0 mod m)
    # The variable "result" stores the result of b^n mod m
    # When the loop reaches a bit with a value of 1...
    # "result" is updated by multiplying its previous value with...
    # the current value of "square" and then dividing this product by mod m
    # While loop terminates after MSD is reached at n_index[0]
    square = b % m
    result = 1
    while n_index >= 0:
        if n_binary_expansion[n_index] == 1:
            result = (result * square) % m
        square = (square * square) % m
        n_index -= 1
    return(result)


def euclidean_alg(a, b):
    """
    Calculates the Greatest Common Divisor (GCD) of two integers
    Uses the Euclidean Algorithm
        Input:
            a, b (integers)
        Output:
            gcd (integer): the GCD(a, b)
    """
    # Program begins by testing which of a or b are larger
    # The variable larger_num takes the value of the larger of the two values
    # The variable smaller_num takes the value of the smaller of the two values
    if a >= b:
        larger_num = a
        smaller_num = b
    if a < b:
        smaller_num = a
        larger_num = b
    # While loop finds the remainder when larger_num is divided by smaller_num
    # This result is stored in the variable "remainder"
    # as long as there is a remainder...
    # larger_num takes on the value of smaller_num...
    # and smaller_num takes the value of remainder...
    # and the loop again finds the remainder between these two numbers
    # This process continues until there is no remainder (until remainder = 0)
    # At this point the larger_num is the GCD of the original two numbers
    # The program exits the while loop because remainder = 0
    # Variable "gcd" takes the value of larger_num and is returned by function
    remainder = 1
    while remainder > 0:
        remainder = larger_num % smaller_num
        larger_num = smaller_num
        smaller_num = remainder
    gcd = larger_num
    return(gcd)


def find_public_key_e(p, q):
    """
    Takes two prime numbers and returns a public key for RSA Encryption
    Input:
        p, q (prime integers)
    Output:
        n (integer): the product of p and q
        e (integer): prime number relatively prime to (p - 1)(q - 1)
        (Note: e does not necessarily need to be a prime number in RSA)
    """
    n = p * q
    n_phi = (p - 1) * (q - 1)
    # Identify prime numbers that will serve as candidates for e
    # Use Sieve of Eratosthenes to do so
    # This works by first generating a list of integers from 2 to 500
    # The first value in list, x, is compared to all other values, y, in list
    # All values that are divisible by this first value are deleted
    # This process is repeated for all remaining values in the list
    # The end result is a list of the prime numbers within the original range
    e_candidates = [value for value in range(2, 500)]
    for x in e_candidates:
        for y in e_candidates:
            if x != y and y % x == 0:
                e_candidates.remove(y)
    import random
    e = random.choice(e_candidates)
    while euclidean_alg(e, n_phi) != 1 or e == p or e == q or e < 17:
        e = random.choice(e_candidates)
    return(n, e)


def find_private_key_d(e, p, q):
    """
    Uses Extended Euclidean Algorithm to find inverse of e mod (p-1)(q-1)
    This inverse is d, the private key for RSA encryption
    Input:
        e (integer), relatively prime to (p - 1)(q - 1)
        p, q (prime integers)
    Output:
        d (integer), modular inverse of e mod (p - 1)(q - 1)
    """
    m = (p - 1) * (q - 1)
    n = e
    # Program begins by initializing Bezout Coefficients for m and n
    # Note: m >= n >= 0
    # s corresponds to multiples of the original value of m
    # t correspond to multiples of the original value of n
    (old_s1, old_t1) = (1, 0)  # Initial Bezout Coefficients of m
    (old_s2, old_t2) = (0, 1)  # Initial Bezout Coefficients of n
    while (n > 0):
        # While loop calculates successive factors of m and n
        # k is the remainder when m is divided modulo n
        # q is the quotient when m is divided by n
        k = m % n
        q = m // n
        # m takes the previous value of n
        # n takes the value of k
        m = n
        n = k
        # Bezout coefficients updated
        # m takes what were previously n's coefficients
        # n takes k's coefficients (expressed in terms of s1,s2,t1,t2 and q)
        (new_s1, new_t1) = (old_s2, old_t2)
        (new_s2, new_t2) = ((old_s1 - q * old_s2), (old_t1 - q * old_t2))
        # "old" coefficients updated with current values of coefficients
        # Used to update values of "new" coefficients in subsequent loops
        (old_s1, old_t1) = (new_s1, new_t1)
        (old_s2, old_t2) = (new_s2, new_t2)
    # d is assigned the value of new_t1; this is final Bezout Coefficient of...
    # n (which was our original value for e)
    # Thus, new_t1 is the B.C. for e
    # That is: gcd(e, (p-1)*(q-1)) = (new_s1) * [(p-1)(q-1)] + (new_t1) * e
    # Thus new_t1 is inverse of e mod [(p-1)*(q-1)]
    d = new_t1
    # Final while loop ensures that a positive value of d is returned
    # Because d is a modular inverse of e mod (p - 1)(q - 1)...
    # We can add the modulus (p - 1)(q - 1) to d repeatedly and it will...
    # Still be congruent to original value with regard to e mod (p - 1)(q - 1)
    while d < 0:
        d += ((p - 1) * (q - 1))
    return(d)


def encode(n, e, message):
    """
    Encodes text for RSA using function C = M^e mod n
    (Where C = cipher, M = original message, e,n = public key)
    Input:
        n, e (integers): public key
        message (string): message to be encoded
    Output:
        cipher_text (list of integers): each integer is one encoded character
    """
    message_ascii_list = text_to_ascii_list(message)
    cipher_text = []
    for ascii_integer in message_ascii_list:
        cipher_integer = fast_modular_exp(ascii_integer, e, n)
        cipher_text.append(cipher_integer)
    return(cipher_text)


def decode(n, d, cipher_text):
    """
    Decodes cipher for RSA using function M = C^d mod n
    (Where M = original message, C = cipher, d,n = private key)
    Input:
        n, d (integers): private key
        cipher_text (list of integers): each integer is one encoded character
    Output:
        message (string): original message
    """
    message_ascii_list = []
    for cipher_integer in cipher_text:
        ascii_integer = fast_modular_exp(cipher_integer, d, n)
        message_ascii_list.append(ascii_integer)
    message = ascii_list_to_text(message_ascii_list)
    return(message)


def user_get_keys():
    """
    1 of 3 Helper functions for main()
    Prompts user for prime numbers 'p' and 'q'.
    Outputs 'n', 'e', and 'd'.
    """
    action = "\n--- Get Keys ---\n"
    action += "Enter p: "
    p = int(input(action))
    action = "Enter q: "
    q = int(input(action))
    (n, e) = find_public_key_e(p, q)
    d = find_private_key_d(e, p, q)
    conclusion = f"\nPublic Key (n, e): ({n}, {e})\n"
    conclusion += f"Private Key (n, d): ({n}, {d})\n"
    print(conclusion)


def user_encode():
    """
    2 of 3 Helper functions for main()
    Prompts user for 'n', 'e', and message to encrypt.
    Outputs encrypted message as array of integer values.
    Each elt in this array is one encrypted letter. 
    """
    action = "\n--- Encode ---\n"
    action += "Enter n: "
    n = int(input(action))
    action = "Enter e: "
    e = int(input(action))
    action = "Enter message: "
    message = (input(action))
    cipher_text = encode(n, e, message)
    conclusion = f"\nCipher Text: {cipher_text}\n"
    print(conclusion)


def user_decode():
    """
    3 of 3 Helper functions for main()
    Prompts user for 'n', 'd', and cipher text.
    Outputs original, decoded message.
    """
    action = "\n--- Decode ---\n"
    action += "Enter n: "
    n = int(input(action))
    action = "Enter d: "
    d = int(input(action))
    action = "Enter cipher text: "
    raw_cipher_text = list(input(action))
    cipher_text = ''
    valid_numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    seperator = [","]
    for element in raw_cipher_text:
        if element in valid_numbers:
            cipher_text += str(element)
        elif element in seperator:
            cipher_text += ', '
    cipher_text = cipher_text.split(', ')
    for i in range(0, len(cipher_text)):
        cipher_text[i] = int(cipher_text[i])
    message = decode(n, d, cipher_text)
    conclusion = f"\nMessage: {message}\n"
    print(conclusion)
        

def main():
    """
    Orchestrates RSA program
    User can (1) get keys, (2) encode a message, and (3) decode a message.
    While loop keeps RSA program running as long as user wishes.
    Input:
        action (string number): user is prompted to enter 1, 2, 3, or 4
        (1 = get keys, 2 = encode message, 3 = decode message, 4 = end program)
    """
    startup_message = "\n--- CODY'S RSA PROGRAM ---\n"
    print(startup_message)
    programming_running = True
    while programming_running:
        action = "Enter 1, 2, 3, or 4:\n"
        action += "\n\t(1) Get Keys\n \t(2) Encode\n"
        action += "\t(3) Decode\n \t(4) Quit Program\n"
        action += "\nYour Selection:\t"
        user_choice = input(action)
        if user_choice == "1":
            user_get_keys()
        elif user_choice == "2":
            user_encode()
        elif user_choice == "3":
            user_decode()
        elif user_choice == "4":
            programming_running = False
    closing_message = "--- Program Closed ---"
    print(closing_message)


if __name__ == '__main__':
    main()
