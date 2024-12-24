# Practice 1: Create a function to find which word occurs the most ? Check this function with the following paragraph

# "Friendship is one of the most important things in life. 
# Probably everybody has a few close friends who you met at school or university.
# Nevertheless, I think that our life does consists of more significant things even than friendship.
# For example, family and self-realisation are vital necessities of life at all times. 
# Firstly, a family has a significant influence on both upbringing and education of a child since early age."

# Hints: Using text.split() to convert a paragraph into list of words

def fre(text):
    #remove special characters, dot comma
    remove_comma = text.replace(",", "")
    remove_dot = remove_comma.replace(".", "")

    #lower text in same style, split it and get into list          
    words = remove_dot.lower().split()

    #get a unique word in a list
    words = list(words)
    unique_words = list(set(words))

    print(unique_words)

    #create empty dictionary to include key and value
    frequency = {}

    #use loop to count occurance of each word in list
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else :
            frequency[word] = 1

    print(frequency)

    #find highest frequency
    highest_frequency = max(frequency.values())
    print(highest_frequency)
    
    #print key, frequency and highest frequency
    for a in frequency:
        if frequency[a] >= highest_frequency:
            print(a, ":", frequency[a])
text =  "Friendship is one of the most important things in life. Probably everybody has a few close friends who you met at school or university. Nevertheless, I think that our life does consists of more significant things even than friendship. For example, family and self-realisation are vital necessities of life at all times. Firstly, a family has a significant influence on both upbringing and education of a child since early age."
fre(text)

--
# Practice 2: Count the unique words of the following text

# "Friendship is one of the greatest bonds anyone can ever wish for. \
# Lucky are those who have friends they can trust. Friendship is a devoted relationship between two individuals.\ 
# They both feel immense care and love for each other. \
# Usually, a friendship is shared by two people who have similar interests and feelings"

def uni(text):
    #remove comma, dot in text
    remove_comma = text.replace(",", "")
    remove_dot = remove_comma.replace(".", "")

    #lower text in same style, split it and get into list          
    words = remove_dot.lower().split()
    
    #get a unique word in a list
    words = list(words)
    unique_words = list(set(words))
    frequency = {}
    diction_word = {}

    #use loop to count occurance of each word in list
    for word in unique_words:
        frequency[word] =words.count(word)
        diction_word.setdefault(word, frequency[word])
    print(diction_word)
    
    #count unique word, have a occurane = 1 in text
    count = 0
    for a in diction_word:
        if diction_word[a] == 1:
            count  += 1
    print(count)
text = "Friendship is one of the greatest bonds anyone can ever wish for. Lucky are those who have friends they can trust. Friendship is a devoted relationship between two individuals. They both feel immense care and love for each other. Usually, a friendship is shared by two people who have similar interests and feelings"
uni(text)

--
# Practice 3 Find the number or prime number from the following list

# [1, 7, 6, 9, 13, 21, 27]

def prime(a):
    #use loop for array
    for x in a:

    # examine x with 0 and 1 cases
        if x == 0 or x == 1:
            print(x, "is not the prime nunmber")

    #examine x >1 case, in this case have 2 cases, divide for another num, the another one is prime
        elif x > 1:
            for i in range (2, x):
                if (x % i == 0) : 
                    print(x, " is not the prime number")
                    break
            else :
                print(x, " is the prime number")
                
    # the remained is not prime
        else:
            print(x, " is not the print number")
a = [1, 7, 6, 9, 13, 21, 27]
prime(a)

--
# Practice 4: Check if these two couples of sentences (Sentence 1 & 2, Sentence 3 & 4) are anagrams or not

# Sentence 1 = "listen to the silent whispers"

# Sentence 2 = "silent whispers to the listen"

# Sentence 3 = "listen to the silent night"

# Sentence 4 = "silent whispers to the listen"

# Hints: How to convert a sentence into list of characters

sentence_1 = "listen to the silent whispers"

sentence_2 = "silent whispers to the listen"

sentence_3 = "listen to the silent night"

sentence_4 = "silent whispers to the listen"

def text_transform(text):
  # text format
  text = text.lower()
  text = text.replace('.','').replace(',','').replace('?','').replace('!','')
  # convert text to list and sort
  text_list = text.split()
  text_list = sorted(text_list)
  return text_list

def check_anagrams(text1, text2):
    if text_transform(text1) == text_transform(text2):
      print ('Two sentences are anagrams')
    else:
      print ('Two sentences are not anagrams')  

check_anagrams(sentence_3, sentence_4)

--

# "Practice 5 (Optional): Anna is submitting a requirement on a platform. 
# Howerver, there are limitations about the number of words and number of characters for the submission. 
# Particularly, the number of world should be under 50 words, and number of character should be under 200 characters."
# Please help Anna create a function to do this and check this function with the following submissions !

# Submission 1: "I am very excited about the opportunity to work with your company. 
# My skills in data analysis and programming make me confident that I would be a valuable addition to your team. 
# I look forward to the chance to contribute and grow with your company.
# Submission 2: "I recently bought this product, and I must say, I'm really impressed. 
# The quality is exceptional, and it works just as advertised. 
# I especially appreciate the ease of use, which makes it perfect for both beginners and experts. 
# I would definitely recommend it to others who are looking for something similar."
submission_1 = "I am very excited about the opportunity to work with your company. My skills in data analysis and programming make me confident that I would be a valuable addition to your team. I look forward to the chance to contribute and grow with your company."

submission_2 =  "I recently bought this product, and I must say, I'm really impressed. The quality is exceptional, and it works just as advertised. I especially appreciate the ease of use, which makes it perfect for both beginners and experts. I would definitely recommend it to others who are looking for something similar."
#remove dot, comma in text
def submission_validation(text):
    text = text.lower()
    text = text.replace('.','').replace(',','').replace('?','').replace('!','')

    #count word in paragraph
    word_list = text.split()
    count_word = len(word_list)

    #count character in paragraph
    count_character = len(list(text))

    #notification for each condition
    if count_word <= 50 and count_character <= 200:
        print("Submission approved!")
    elif count_word > 50 and count_character <= 200:
        print("Number of words should be under 50 . Current number of words: " + str(count_word))
    elif count_word <= 50 and count_character > 200:
        print("Number of character should be under 200. Current number of characters: " + str(count_character))
    else:
        print("Numbers of words and characters are over the rule , please check it again!")

#print results
submission_validation(submission_1)

print('')

submission_validation(submission_2)