# Part 3 | Refine your indexing procedure. Implement ranking of returns.
#        | Test and analyze your system, discuss how your design decisions influence the results.
# Name: Souheil Al-awar

# Imports
from nltk.tokenize import word_tokenize, regexp_tokenize
import time
import re

# Regex to extract raw text
regx_reuters = "<REUTERS(.*?)<\/REUTERS>"
regx_newid = "NEWID=\"(.*?)\""
regx_date = "<DATE>(.*?)<\/DATE>"
regx_title = "<TITLE>(.*?)<\/TITLE>"
regx_body = "<BODY>(.*?)<\/BODY>"

def main():
    c = mini_corpus()
    k = corpus()
    
    ####################
    # subproject 1(a)
    
    print("(1)(a) The following are the compared timings between Naive and SPIMI indexers\n"
          + "\tusing a corpus of 10,000 tokens:")
    start = time.time()
    naive(c)
    end = time.time()
    print("\n\tTime of execution of Naive Indexer:", (end-start) * 10**3, "ms")

    start = time.time()
    spimi(c)
    end = time.time()
    print("\tTime of execution of SPIMI:", (end-start) * 10**3, "ms")

    ####################
    # subproject 1(b)
    
    print("\n(1)(b) Let's compile an inverted index for Reuters 21578 without using any\n"
            + "\tcompression techniques. To speed up the process we'll be compiling SPIMI")
    print("\t\nPlease wait while the program compiles the indexer...")
    
    sp = spimi(k)
    prt = ""
    prt = input("\n\tSPIMI indexer was compiled successfully. Would you like to print it?"
                + "\n\t**KEEP IN MIND IT WILL BE LONG** (Enter 1 to print or anything else to"
                + "\n\tcontinue): ")
    if prt == str(1):
        print(sp)
            
    #################
    # subproject 2
    # don't quite understand it

    #################
    # test queries
    print("\n*** TEST QUERIES ***")

    sing_query = ''
    and_query = ''
    or_query = ''
    
    while sing_query != 'done':
        print("\t\n(a) A single keyword query, to compare with Project 2. Enter the word 'done' to move on.")
        sing_query = input("\tEnter your single keyword query: ")
        if sing_query == "done":
            continue
        qry = re.sub(r'[^\w\s]', '', sing_query)
        print(sp[qry.lower()])

    while and_query != 'done':
        print("\t\n(c) A multiple keyword query returning documents containing all the keywords (AND), for unranked Boolean. Enter the word 'done' to move on.")
        and_query = input("\tEnter your multiple keyword query: ")
        if and_query == 'done':
            continue

        # logic: check the term with the smallest list of docIDs and compare with the rest of the list
        #           if all the words appear in the same document then add the docID to a new list

        # regex to avoid errors with apostrophes
        qry = re.sub(r'[^\w\s]', '', and_query)
        
        # separate query into words
        lst_query = qry.split()

        # list for lowercase words
        lwr_query = []

        # loop to make words lowercase
        for i in lst_query:
            lwr_term = i.lower()
            lwr_query.append(lwr_term)
        
        # check if all words are in dictionary
        success = len(lwr_query)
        counter = 0
        for i in lwr_query:
            if i in sp:
                counter = counter + 1

        # list of lengths to organize the terms and its lengths
        lengths = []

        # turn the list of terms for the query into a list of lists with the term and its length
        for i in lwr_query:
            item = [i,len(sp[i])]
            lengths.append(item)    

        # sort the list of lengths terms by ascending order
        lengths.sort(key=lambda x: x[1])

        # now that it's sorted in ascending order let's get rid of the lengths and keep only the terms
        terms_list = [sublist[0] for sublist in lengths]

        # let's create a list to return the documents where all terms appear at the same time
        result_docs = []

        # to verify the current words appear in the same document
        doc_passed = len(terms_list)-1
        
        # populate resulting list
        if counter == success:
            for i in sp[terms_list[0]]:
                in_counter = 0
                for j in terms_list[1:]:
                    if i in sp[j]:
                        in_counter = in_counter + 1
                if in_counter == doc_passed:
                    result_docs.append(i)
            print("Query result: ", result_docs)
        else:
            print("\t\nNot all queries were found. Hence, no successful 'AND' query found.")
            

    while or_query != 'done':
        print("\t\n(d) A multiple keywords query returning documents containing at least one keyword (OR), where documents\n"
                + "are ordered by how many keywords they contain, for unranked Boolean retrieval. Enter the word 'done' to move on.")
        or_query = input("\tEnter your multiple keyword query: ")
        if or_query == "done":
            continue
        qry = re.sub(r'[^\w\s]', '', or_query)
        # separate query into words
        lst_query = qry.split()

        # list for lowercase words
        lwr_query = []

        # loop to make words lowercase
        for i in lst_query:
            lwr_term = i.lower()
            lwr_query.append(lwr_term)

        # let's create a list to return the list of documents for this query
        result_docs = []
        
        for i in lwr_query:
            if i in sp:
                for j in sp[i]:
                    if j in result_docs:
                        continue
                    else:
                        result_docs.append(j)
            else:
                print("\t\nThe following term is not in the dictionary: ", i)

        # sort results
        res = [eval(i) for i in result_docs]
        res.sort()
        sorted_results = res
        
        # print result list
        print("Query result: ", sorted_results)

    print('\nEnd of the program.')
    quit()
    
def naive(c):
    # accept a c (corpus of 10,000 items) as a list of tokens
    F = []
    pair = []

    # outputs term-docID pairs to a list F
    for i in c:
        for j in i[1]:
            pair = [j, i[0]]
            F.append(pair)

    # sort F
    F.sort()

    # remove duplicates
    new_F = []
    for l in F:
        if l not in new_F:
            new_F.append(l)
   
    # turn the docIDs paired with the same term into a postings list
    #   & setting the pointer
    dic_F = {}
    for i in new_F:
        # if our current token (i) is not in the dictionary
        if i[0] not in dic_F:
            # assign new key-value item to our dictionary
            dic_F[i[0]] = i[1]
        else:
            # store all the values this token already has into a placeholder variable
            values = dic_F[i[0]]
            # if those values are already a list type
            if isinstance(values, list):
                # append the new value to the list
                dic_F[i[0]].append(i[1])
            # else, if values are not a list type
            else:
                # make sure "values" is a list
                list_values = []
                list_values = list(values)
                # assign it to dictionary key (in this case our current i)
                dic_F[i[0]] = list_values
                # append the new value to the list
                dic_F[i[0]].append(i[1])

    return(dic_F)

def spimi(k):
    # directly append the docID to the postings list for the term
    # dictionary for all terms
    F = {}

    # go through every item in the corpus
    for i in k:
        # go through every token per item
        for j in i[1]:
            # if the token IS NOT in the dictionary F
            if j not in F:
                # assign new key-value item to our dictionary
                F[j] = i[0]
            # if the token IS in the dictionary F
            elif j in F:
                # store all the values this token already has into a placeholder variable
                values = F[j]
                if i[0] not in values:
                    # if those values are already a list type
                    if isinstance(values, list):
                        # append the new value to the list
                        F[j].append(i[0])
                    # else, if values are not a list type
                    else:
                        # make sure "values" is a list
                        list_values = []
                        list_values = list(values)
                        # assign it to dictionary key (in this case our current i)
                        F[j] = list_values
                        # append the new value to the list
                        F[j].append(i[0])
    return(F)

def corpus():
    #------------------------------------------------------#
    # format of corpus: ['docID', ['token', 'token', ...]] #
    #------------------------------------------------------#

    # list for the new corpus containing a list of lists
    corpus = []
    
    # current document length
    doc_len = 0

    # reuters has 22 files from 000 to 021, assign the names one by one
    for x in range(22):
        # Allocate respective names from files 000 to 021
        if x < 10:
            file_name = "reut2-00" + str(x) + ".sgm"
        else:
            file_name = "reut2-0" + str(x) + ".sgm"

        
        # get the file
        with open(file_name, 'r') as rfile:
            raw_data = rfile.read().replace('\n', ' ')
        rfile.close()

        # get the raw data in each reuters tag from the file
        reuters = regexp_tokenize(raw_data, pattern=regx_reuters)

        # go through the reuters tags
        for y in reuters:

            # list to store ALL the current document [docID, content]
            doc_list = []
    
            # list variable to store document content
            doc_content = []
        
            # extract and store aside the docID from the document
            doc_id = regexp_tokenize(y, pattern=regx_newid)

            # assign doc_id to a list for the current document
            doc_list.append(doc_id[0])
        
            # check for a title tag
            if bool(regexp_tokenize(y, pattern=regx_title)):
            
                # extract and store aside the title from the document
                doc_title = regexp_tokenize(y, pattern=regx_title)

                # tokenize title
                tkn_title = word_tokenize(doc_title[0])

                # lowercase tokens
                tkn_list = []
                for i in tkn_title:
                    lower_token = i.lower()
                    tkn_list.append(lower_token)
                tkn_title = tkn_list

                # insert title tokens to list
                doc_content.extend(tkn_title)
            
            # check for a body tag
            if bool(regexp_tokenize(y, pattern=regx_body)):

                # extract and store aside the body from the document 
                doc_body = regexp_tokenize(y, pattern=regx_body)

                # tokenize body
                tkn_body = word_tokenize(doc_body[0])

                # lowercase tokens
                tkn_list = []
                for i in tkn_body:
                    lower_token = i.lower()
                    tkn_list.append(lower_token)
                tkn_body = tkn_list

                # insert body tokens to list
                doc_content.extend(tkn_body)

            # append current document to current doc_list
            doc_list.append(doc_content)
            
            # append current doc_list to corpus
            corpus.append(doc_list)
    
    return(corpus)

def mini_corpus():
    #------------------------------------------------------#
    # format of corpus: ['docID', ['token', 'token', ...]] #
    #------------------------------------------------------#
    
    # to keep count of our 10000 ceiling
    term_count = 0
    
    # list for the new corpus containing a list of lists
    mini_corpus = []
    
    # current document length
    doc_len = 0
    
    # get the file
    with open('reut2-000.sgm', 'r') as rfile:
        raw_data = rfile.read().replace('\n', ' ')
    rfile.close()

    # get the raw data in each reuters tag from the file
    reuters = regexp_tokenize(raw_data, pattern=regx_reuters)

    # go through the reuters tags
    for y in reuters:

        # list to store ALL the current document [docID, content]
        doc_list = []
    
        # list variable to store document content
        doc_content = []
        
        # check for 10000 words
        if term_count >= 10000:
            break
        
        else:
            # extract and store aside the docID from the document
            doc_id = regexp_tokenize(y, pattern=regx_newid)

            # assign doc_id to a list for the current document
            doc_list.append(doc_id[0])
        
            # check for a title tag
            if bool(regexp_tokenize(y, pattern=regx_title)):
            
                # extract and store aside the title from the document
                doc_title = regexp_tokenize(y, pattern=regx_title)

                # tokenize title
                tkn_title = word_tokenize(doc_title[0])

                # lowercase tokens
                tkn_list = []
                for i in tkn_title:
                    lower_token = i.lower()
                    tkn_list.append(lower_token)
                tkn_title = tkn_list

                # insert title tokens to list
                doc_content.extend(tkn_title)
            
            # check for a body tag
            if bool(regexp_tokenize(y, pattern=regx_body)):

                # extract and store aside the body from the document 
                doc_body = regexp_tokenize(y, pattern=regx_body)

                # tokenize body
                tkn_body = word_tokenize(doc_body[0])

                # lowercase tokens
                tkn_list = []
                for i in tkn_body:
                    lower_token = i.lower()
                    tkn_list.append(lower_token)
                tkn_body = tkn_list

                # insert body tokens to list
                doc_content.extend(tkn_body)

            # get length of current doc
            doc_len = len(doc_content)

            # increase count
            term_count = term_count + doc_len

            # append current document to current doc_list
            doc_list.append(doc_content)
            
            # append current doc_list to mini_corpus
            mini_corpus.append(doc_list)
        
    # store aside last document text to trim
    extra_tokens = mini_corpus[60][1]

    # remove the last 493 terms in the list of words, join back
    #   by " " spaces, and store aside
    last_tokens = extra_tokens[:len(extra_tokens)-157]

    # enter back the document text to the mini_corpus's last index
    mini_corpus[60][1] = last_tokens

    # update term_count
    term_count = term_count - 157
    
    return(mini_corpus)

main()
