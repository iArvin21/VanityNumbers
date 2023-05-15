import boto3
import json
import itertools
import heapq
import re
from nltk.corpus import words
import nltk
from datetime import datetime

#download the words dictionary to lambda temp folder
nltk.data.path.append("/tmp")
nltk.download("words", download_dir="/tmp")

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False
        
class Trie:
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self, word):
        current = self.root
        for letter in word:
            if letter not in current.children:
                current.children[letter] = TrieNode()
            current = current.children[letter]
        current.is_word = True
        
    def search(self, word):
        current = self.root
        for letter in word:
            if letter not in current.children:
                return False
            current = current.children[letter]
        return current.is_word

def generate_vanity_number(phone_number):
    phone_number_digits = re.sub(r'\D', '', phone_number)
    dash_positions = [i for i, char in enumerate(phone_number) if char == '-']
    
    #number mapping
    digit_map = {
        '0': ['0'],
        '1': ['1'],
        '2': ['a', 'b', 'c'],
        '3': ['d', 'e', 'f'],
        '4': ['g', 'h', 'i'],
        '5': ['j', 'k', 'l'],
        '6': ['m', 'n', 'o'],
        '7': ['p', 'q', 'r', 's'],
        '8': ['t', 'u', 'v'],
        '9': ['w', 'x', 'y', 'z']
    }
    
    # Get all the possible combinations
    letter_combinations = [digit_map[digit] for digit in phone_number_digits]

    # Build the Trie data structure
    trie = Trie()
    for word in words.words():
        if len(word) == len(phone_number_digits):
            trie.insert(word.lower())

    # Use a heap to keep track of the top 3 vanity numbers
    top_vanity_numbers = []

    # Generate all possible combinations of letters from the digit map
    for i in range(len(phone_number_digits)):
        for j in range(i + 1, len(phone_number_digits) + 1):
            prefix = phone_number_digits[:i]
            suffix = phone_number_digits[j:]
            for combination in itertools.product(*letter_combinations[i:j]):
                word = prefix + ''.join(combination) + suffix
                # Check if at least one English word is present in the combination
                if any(trie.search(w.lower()) for w in re.findall(r'\w+', word)):
                    vanity_number = word
                    # Add the dashes back to the vanity number at the original positions
                    for pos in dash_positions:
                        vanity_number = vanity_number[:pos] + phone_number[pos] + vanity_number[pos:]
                    heapq.heappush(top_vanity_numbers, (-len(vanity_number), vanity_number))

    # If there are fewer than 5 vanity numbers in the heap, add vanity numbers that did not form words
    while len(top_vanity_numbers) < 5:
        for combination in itertools.product(*letter_combinations):
            word = ''.join(combination)
            vanity_number = word
            # Add the dashes back to the vanity number at the original positions
            for pos in dash_positions:
                vanity_number = vanity_number[:pos] + phone_number[pos] + vanity_number[pos:]
            heapq.heappush(top_vanity_numbers, (-len(vanity_number), vanity_number))
            if len(top_vanity_numbers) >= 5:
                break

    # Extract the top 5 vanity numbers from the heap and return them
    result = [heapq.heappop(top_vanity_numbers)[1] for _ in range(5)]
    return result

def lambda_handler(event, context):
    phone_number = event['Details']['ContactData']['CustomerEndpoint']['Address']
    vanity_numbers = generate_vanity_number(phone_number)
    
    # Save to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('vanity_nums')
    now = datetime.now()
    item = {
        'id': phone_number,
        'vanity_numbers': vanity_numbers[:5],
        'added_date' : now.strftime("%d/%m/%Y %H:%M:%S")
    }
    table.put_item(Item=item)
    
    data = {
        "vanity1":vanity_numbers[:1],
        "vanity2":vanity_numbers[1:2],
        "vanity3":vanity_numbers[2:3]
    }
    return  {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(data)
    }

