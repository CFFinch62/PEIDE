import math
import random

def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = 'X' * int(percent) + '-' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end="\r")
    
# Euler's Totient Function
def phi(n):
    # Initialize result as n
    result = n;
    # Consider all prime factors of n and subtract their multiples from result
    p = 2;
    while(p * p <= n):
        # Check if p is a  prime factor.
        if (n % p == 0):
            # If yes, then update n and result
            while (n % p == 0):
                n = int(n / p);
            result -= int(result / p);
        p += 1;
    # If n has a prime factor greater than sqrt(n) (There can be at-most one such prime factor)
    if (n > 1):
        result -= int(result / n);
    return result;

# Returns the number of 1's in the binary representation of
# the non-negative integer x.
def hamming_weight(x):
    return bin(x).count("1")

def gcd(n1,n2):
    while n2 > 0:
        n1, n2 = n2, n1 % n2
    return n1

def lcm(n1, n2):
    return n1 * n2 / gcd(n1, n2)

def gpf(n):
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0 and is_prime(i):
            largest = i
    return largest


def all_factors(n):
    factors = []
    for i in range(1, n + 1):
        if n % i == 0:
            factors.append(i)
    return factors

def get_prime_factors(n):
    """Returns a set of unique prime factors of n"""
    i = 2
    factors = set()
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.add(i)
    if n > 1:
        factors.add(n)
    return list(factors)

def num_prime_factors(n):
    """Returns the number of unique prime factors of n"""
    return len(get_prime_factors(n))

def proper_factors(n):
    factors = []
    for i in range(2, n):
        if n % i == 0:
            factors.append(i)
    return factors

def proper_divisors(n):
    factors = []
    for i in range(1, n):
        if n % i == 0:
            factors.append(i)
    return factors

def coprime(n1, n2):
    for i in range(2, n1):
        if n1 % i == 0 and n2 % i == 0:
            return False
    return True


# Tests whether x is a perfect square, for any integer x.
def is_square(x):
    if x < 0:
        return False
    y = x**0.5
    return y * y == x

# Tests whether the given integer is a prime number.
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_odd(n):
    if n % 2 == 0:
        return False
    else:
        return True

def is_perfect(n):
    tmp = []
    total = 0
    
    tmp = proper_divisors(n)
    for i in range(len(tmp)):
        total += tmp[i]
    if total == n:
        return True
    else:
        return False

def is_abundant(n):
    tmp = []
    total = 0
    
    tmp = proper_divisors(n)
    for i in range(len(tmp)):
        total += tmp[i]
    if total > n:
        return True
    else:
        return False

def is_deficient(n):
    tmp = []
    total = 0
    
    tmp = proper_divisors(n)
    for i in range(len(tmp)):
        total += tmp[i]
    if total < n:
        return True
    else:
        return False
    
def is_triangular(n):
    if ((-1 + ((1 + (8 * n)) ** 0.5)) / 2) % 1 == 0:
        return True
    return False

def is_perfect_square(n):
    if math.isqrt(n) % n == 0:
        return True
    return False

def is_pentagonal(n):
    if (1+(24*n+1)**0.5) % 6 == 0:
        return True
    return False

def is_hexagonal(n):
    if (1+(8*n+1)**0.5) % 4 == 0:
        return True
    return False

def is_pandigital(n, b, z):    
    digits = list(set(str(n)))    
    # do we include zero as a digit
    if z:
        a = 0
    else:
        a = 1    
    # do we use auto or fixed base
    if b > 0:
        base = b
    else:
        base = len(digits)    
    # final check each digit only occurs once in n 
    for i in range(a, base + 1):
        if digits.count(str(i)) < 1 or digits.count(str(i)) > 1:
            return False   
    return True

def is_lychrel(n):
    rn = int(str(n)[::-1])
    nn = n
    i = 0
    while i < 51:
        nn = nn + rn
        if is_palindrome(str(nn)):
            return False
        i += 1
        rn = int(str(nn)[::-1])
    return True

def is_curzon(num):
    elv = 2 ** num + 1
    mul = 2 * num + 1

    res = elv % mul

    if res == 0:
        return True     
    return False

def sum_digits(n):
    idx = 0
    sum = 0
    snum = str(n)
    while idx < len(snum):
        sum = sum + int(snum[idx])
        idx += 1
    return sum

def prime_sieve(n):
    # create intial pre-poulated list
    primes = [ True for i in range(n + 1)]
    
    # mark the primes in list as TRUE
    k = int(n**0.5) 
    for p in range(2,k,1): 
        if (primes[p] == True):
            
            # mark the non prime  as FALSE
            for i in range(p * 2,n,p): 
                primes[i] = False
    return primes

def generate_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = [False] * len(sieve[i*i::i])
    
    return [i for i, is_prime in enumerate(sieve) if is_prime]

def get_primes_up_to(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = [False] * len(sieve[i*i::i])
    return [i for i, is_prime in enumerate(sieve) if is_prime] 

def collatz_chain(n):    
    tmp = 0
    chain = []

    chain.append(n)
    # is even
    if n % 2 == 0:
        tmp = n // 2
        chain.append(tmp)
        while tmp != 1:
            if tmp % 2 == 0:
                tmp //= 2
                chain.append(tmp)
            else:
                tmp = (3 * tmp) + 1
                chain.append(tmp)
    # is odd    
    else:
        tmp = (3 * n) + 1
        chain.append(tmp)
        while tmp != 1:
            if tmp % 2 == 0:
                tmp //= 2
                chain.append(tmp)
            else:
                tmp = (3 * tmp) + 1
                chain.append(tmp)

    return chain

def choose(r, d):
    return (math.factorial(r) / (math.factorial(d) * math.factorial(r-d)))

def get_2D_row(r, a):
    return [row for row in a[r]]

def get_2D_col(c, a):
    return [row[c] for row in a]

def decimalToBinary(n):  
    return bin(n).replace("0b", "")

def genRandomBinaryString(n):
    bin_str = ""
    cnt = 0
    while cnt <= n:
        bin_str += str(random.randint(0, 1))
        cnt += 1
    return bin_str

def is_palindrome(s):
    return s == s[::-1]

def ltr_to_int(ltr):
    l = { 'A' : 1, 'B' : 2, 'C' : 3, 'D' : 4, 'E' : 5, 'F' : 6,
          'G' : 7, 'H' : 8, 'I' : 9, 'J' : 10, 'K' : 11, 'L' : 12,
          'M' : 13, 'N' : 14, 'O' : 15, 'P' : 16, 'Q' : 17, 'R' : 18,
          'S' : 19, 'T' : 20, 'U' : 21, 'V' : 22, 'W' : 23, 'X' : 24,
          'Y' : 25, 'Z' : 26 }
    return l[ltr]

def int_to_ltr(num):
    i = { 1 : 'A', 2 : 'B', 3 : 'C', 4 : 'D', 5 : 'E', 6 : 'F', 7 : 'G',
          8 : 'H', 9 : 'I', 10 : 'J', 11 : 'K', 12 : 'L', 13 : 'M', 14 : 'N',
          15 : 'O', 16 : 'P', 17 : 'Q', 18 : 'R', 19 : 'S', 20 : 'T', 21 : 'U',
          22 : 'V', 23 : 'W', 24 : 'X', 25 : 'Y', 26 : 'Z'}
    return i[num]

def word_score(w):
    score = 0
    for i in range(len(w)):
        score += ltr_to_int(w[i])
    return score

def bubble_sort(arr, d=True):
    # assume array is passed in unsorted
    sorted = False
    # sort array
    while not sorted:
      # assume array will be sorted by a single pass
        sorted = True
        # attempt a bubble pass
        for i in range(0, len(arr) - 1):
            # do the sorting according to desired direction 
            if d:
                # if a pair found out of order then swap pair
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    # because we had to do a swap assume we need another pass
                    sorted = False
            else:
                if arr[i] < arr[i + 1]:
                    arr[i + 1], arr[i] = arr[i], arr[i + 1]
                    # because we had to do a swap assume we need another pass
                    sorted = False
  
    return arr

def caesar_cipher_decoder(message, offset):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    punctuation = [" ", ",", ".", "!", "?"]
    decoded_message = ""
    for char in message:
        if char in punctuation:
            decoded_message += char
        else:
            decoded_message += alphabet[(alphabet.find(char) + offset) % len(alphabet)]
    return decoded_message

def caesar_cipher_encoder(message, offset):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    punctuation = [" ", ",", ".", "!", "?"]
    coded_message = ""
    for char in message:
        if char in punctuation:
            coded_message += char
        else:
            coded_message += alphabet[(alphabet.find(char) + offset) % len(alphabet)]
    return coded_message

def vigenere_cipher_decoder(message, key):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    punctuation = [" ", ",", "'", ".", "!", "?"]
    decoded_message = ""
    offset = 0
    location = 0
    ki = 0
    for i in range(len(message)):
        if ki > 6:
            ki = 0
        if message[i] in punctuation:
            decoded_message += message[i]
        else:
            offset = alphabet.find(key[ki])
            location = (alphabet.find(message[i]) - offset) % 26
            decoded_message += alphabet[location]
            ki += 1
    return decoded_message

def vigenere_cipher_encoder(message, key):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    punctuation = [" ", ",", "'", ".", "!", "?"]
    encoded_message = ""
    offset = 0
    location = 0
    ki = 0
    for i in range(len(message)):
        if ki > 6:
            ki = 0
        if message[i] in punctuation:
            encoded_message += message[i]
        else:
            offset = alphabet.find(key[ki])
            location = (alphabet.find(message[i]) + offset) % 26
            encoded_message += alphabet[location]
            ki += 1
    return encoded_message

