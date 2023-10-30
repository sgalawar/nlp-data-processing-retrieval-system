# Part 1 | Developing a pipeline of steps to read, extract, tokenize, and more
# Name: Souheil Al-awar

# Imports
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, regexp_tokenize

# Regex to extract raw text
regx_reuters = "<REUTERS(.*?)<\/REUTERS>"
regx_newid = "NEWID=\"(.*?)\""
regx_date = "<DATE>(.*?)<\/DATE>"
regx_title = "<TITLE>(.*?)<\/TITLE>"
regx_body = "<BODY>(.*?)<\/BODY>"

# Global Variables
raw_data = ''
file_name = ''
new_file_name = ''
corpus = [{}]*22

# Menu with every step for the pipeline
def main():
    user_input = ''
    while user_input != str(6):
        print("\n1 - Read the Reuter's collection and extract the raw text of each article from the corpus." +
              "\n2 - Tokenize." +
              "\n3 - Make all text lowercase." +
              "\n4 - Apply Porter Stemmer." +
              "\n5 - Given a list of stop words, remove those stop words from text. Note that your code has " +
              "to accept the stop word list as a parameter, do not hardcode a particular list." +
              "\n6 - Exit program.")
        user_input = input("Enter your option number and press [enter]: ")
        if user_input == str(1):
            step1()
        elif user_input == str(2):
            step2()
        elif user_input == str(3):
            step3()
        elif user_input == str(4):
            step4()
        elif user_input == str(5):
            user_input = input("Input list of stopwords (choose 1 for english default): ")
            if (user_input == 1):
                step5("stopwords.words('english')")
            else:
                step5(user_input)
        elif user_input == str(6):
            print("Good-bye ;)")
            quit()
        else:
            print("Option not available. Please try again with a single number amongst the options.")
        
# Step 1. Read the Reuter's collection and extract the raw text of each article from the corpus.
def step1():
    for x in range(22):
        # Assign file name from 000 to 021
        if x < 10:
            file_name = "reut2-00" + str(x) + ".sgm"
        else:
            file_name = "reut2-0" + str(x) + ".sgm"
            
        # Save current file name in a dictionary where x is the number of the file and 'name' is the category
        corpus[x]['name'] = file_name
        
        # Open file, read and store the raw data into the raw_data string
        with open(file_name, 'r') as rfile:
            raw_data = rfile.read().replace('\n', ' ')
        rfile.close()
        
        # Store data into dictionary
        corpus[x]['data'] = raw_data
        
        # Extract data from inside the reuters tags and store it into the corpus dictionary
        reuters = regexp_tokenize(raw_data, pattern=regx_reuters)
        corpus[x]['reuters'] = reuters
        
        # Count to go through every article/reuters tag
        count = 0
        
        # Name new file to later assign output document
        new_file_name = "step1_doc_" + str(x) + ".txt"
        
        # Write output into document
        with open(new_file_name, 'w') as wfile:
            
            # Write date, title and body of articles in an organized manner {NEWID: [date, title, body]}
            for y in reuters:
                # For every article in the reuters dictionary store the id number
                newid = regexp_tokenize(reuters[count], pattern=regx_newid)
                newid_str = newid[0]
                
                # Separate data from each article (date, title, and body) and store into dictionaries
                title = regexp_tokenize(reuters[count], pattern=regx_title)
                date = regexp_tokenize(reuters[count], pattern=regx_date)
                body = regexp_tokenize(reuters[count], pattern=regx_body)
                
                # Write output to text file
                for line in title:
                    wfile.write(line)
                    wfile.write('\n')
                
                for line in date:
                    wfile.write(line)
                    wfile.write('\n')
                    
                for line in body:
                    wfile.write(line)
                    wfile.write('\n')
                
                wfile.write("\n")
                                
                # For every id in every article in every document store the collected info in the corpus
                # dictionary assigning it to its correspondent id as a list
                corpus[x][newid_str] = [date, title, body]
                
                # Increment article/reuters tags
                count = count + 1
        wfile.close()
        
# Step 2. Tokenize
def step2():
    for x in range(22):
        # Assign file names to collect data from step 1
        file_name = "step1_doc_" + str(x) + ".txt"
        
        # Open file, read and store the raw data into the raw_data string
        with open(file_name, 'r') as rfile:
            raw_data = rfile.read().replace('\n', ' ')
        rfile.close()
        
        # Tokenize document with nltk
        raw_data = word_tokenize(raw_data)

        # Name new file to later assign output document
        new_file_name = "step2_doc_" + str(x) + ".txt"
        
        # Write tokenized data into the new document
        with open(new_file_name, 'w') as wfile:
            for i in raw_data:
                wfile.write(i)
                wfile.write('\n')
        wfile.close()

# Step 3. Text to lowercase
def step3():
    for x in range(22):
        # Assign file names to collect data from step 2
        file_name = "step2_doc_" + str(x) + ".txt"
        
        # Open file, read and store the raw data into the raw_data string
        with open(file_name, 'r') as rfile:
            raw_data = rfile.read().replace('\n', ' ')
        rfile.close()

        # Text to lowercase
        raw_data = raw_data.lower()

        # Split string into list
        raw_data = raw_data.split()
        
        # Name new file to later assign output document
        new_file_name = "step3_doc_" + str(x) + ".txt"
        
        # Write lowercased words into document
        with open(new_file_name, 'w') as wfile:
            for i in raw_data:
                wfile.write(i)
                wfile.write('\n')
        wfile.close()
        
# Step 4. Porter Stemmer
def step4():
    for x in range(22):
        # Assign file names to collect data from step 3
        file_name = "step3_doc_" + str(x) + ".txt"
        
        # Open file, read and store the raw data into the raw_data string
        with open(file_name, 'r') as rfile:
            raw_data = rfile.read().replace('\n', ' ')
        rfile.close()

        # Simplify Porter stemmer function into a variable
        ps = PorterStemmer()

        # Split string into list
        raw_data = raw_data.split()
        
        # Name new file to later assign output document
        new_file_name = "step4_doc_" + str(x) + ".txt"
        
        # Apply porter stemmer and write to new document
        with open(new_file_name, 'w') as wfile:
            for i in raw_data:
                wfile.write(i + " : " + ps.stem(i))
                wfile.write('\n')
        wfile.close()

# Step 5. Stop words
def step5(list_of_stop_words):
    for x in range(22):
        # Assign file names to collect data from step 3 (not 4 because those have words have :)
        file_name = "step3_doc_" + str(x) + ".txt"
        
        # Open file, read and store the raw data into the raw_data string
        with open(file_name, 'r') as rfile:
            raw_data = rfile.read().replace('\n', ' ')
        rfile.close()

        # Split string into list
        raw_data = raw_data.split()

        # Stop words
        filtered_words = [word for word in raw_data if word not in list_of_stop_words]
        
        # Name new file to later assign output document
        new_file_name = "step5_doc_" + str(x) + ".txt"
        
        # Write filtered words into output file
        with open(new_file_name, 'w') as wfile:
            for i in filtered_words:
                wfile.write(i)
                wfile.write('\n')
        wfile.close()

# Main method
print("Welcome")
main()
