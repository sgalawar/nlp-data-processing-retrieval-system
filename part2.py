# Part 2 | Implement a naive indexer, single term query processing & lossy dictionary compression.
# Name: Souheil Al-awar

# Imports
from nltk.tokenize import word_tokenize, regexp_tokenize
from collections import OrderedDict

# Regex to extract raw text
regx_reuters = "<REUTERS(.*?)<\/REUTERS>"
regx_newid = "NEWID=\"(.*?)\""
regx_body = "<BODY>(.*?)<\/BODY>"

# Global variables
F = {}
file_name = ''
raw_data = ''
article_id = ''
article_body = ''
article_tokens = ''

# 1 - Naive Indexer
def subproject1():
    for x in range(22):
        # Allocate respective names from files 000 to 021
        if x < 10:
            file_name = "reut2-00" + str(x) + ".sgm"
        else:
            file_name = "reut2-0" + str(x) + ".sgm"
        
        # Open file, read and store the raw data into the raw_data string
        with open(file_name, 'r') as rfile:
            raw_data = rfile.read().replace('\n', ' ')
        rfile.close()
        
        # Extract data from inside the reuters tags and store it into the corpus dictionary
        reuters = regexp_tokenize(raw_data, pattern=regx_reuters)
        
        # Loop through every item in the reuters list 
        for y in reuters:
            # Execute conditional if the current item (y) contains a body
            if bool(regexp_tokenize(y, pattern=regx_body)):
                # Store body of every article
                article_body = regexp_tokenize(y, pattern=regx_body)

                # Tokenize body of every post
                article_tokens = word_tokenize(article_body[0])
                
                # Lowercase tokens and insert them back into article_tokens variable
                token_list = []
                for i in article_tokens:
                    lower_token = i.lower()
                    token_list.append(lower_token)
                article_tokens = token_list
                
                # Extract its id
                article_id = regexp_tokenize(y, pattern=regx_newid)
                
                # Loop through the tokens
                for z in article_tokens:
                    # If the token is in our list/dictionary F
                    if z in F:
                        # Store all the values this token already has into a placeholder variable
                        values = F[z]
                        # If those values are already a list type
                        if isinstance(values, list):
                            # Append the new value to the list
                            F[z].append(article_id[0])
                        # Else, if values are not a list type
                        else:
                            # Make sure "values" is a list
                            list_values = list(values)
                            # Assign it to dictionary key (in this case our current z)
                            F[z] = list_values
                            # Append the new value to the list
                            F[z].append(article_id[0])
                    # If our current token (z) is not in the list/dictionary (F)
                    else:
                        # Assign new key-value item to our list/dictionary (F)
                        F[z] = article_id[0]
                        
    # For every key in the list-dictionary
    for z in F:
        # Store the values into a temporary variable "values"
        values = F[z]
        if isinstance(values, list):
            # Turn string values into int
            for i in range(0, len(values)):
                values[i] = int(values[i])
            # Remove duplicate values
            F[z] = list(dict.fromkeys(values))
            # Sort values for every key
            F[z].sort()
            
    # Sort the keys alphabetically
    newF = OrderedDict(sorted(F.items(), key=lambda t: t[0]))

    # Write newF to a file
    newF_name = 'sorted_F.txt'
    with open(newF_name, 'w') as wfile:
        for k,v in newF.items():
            wfile.write('%s:%s\n' % (k, v))
            
    # Write F to a file
    F_name = 'unsorted_F.txt'
    with open(F_name, 'w') as wfile:
        for k,v in F.items():
            wfile.write('%s:%s\n' % (k, v))
            
    print("Naive Indexer done.")
            
## Comment out lines within the lines to print list-dictionary newF
# ============================================================================= 
#    # Print list-dictionary in inverted list format
#    for k,v in new_F.items():
#        print(k,v)
# =============================================================================

# 2 - Single term query processing
def subproject2():
    # Run naives indexer
    subproject1()
    user_input = ''
    # Run query processor until user is ready to quit
    while user_input != 'done':
        user_input = input("Enter a single term query (type \'done\' to exit the application): ")
        user_input = user_input.lower()
        if user_input in F:
            print(F[user_input])
        else:
            print('Sorry, query not found')

def main():
    subproject2()

main()
