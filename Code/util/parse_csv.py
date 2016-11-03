import re
import csv
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.stem.porter import PorterStemmer

filepath = "../../Data/data/trainaa.csv"
parsedPath = "../../Data/parsed_data.json"
tokenizedPath = "../../Data/tokenized_data.json"

stemmer = PorterStemmer()

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed
	
# converts text to stems
def tokenize(text):
    text = text.lower()
    tokens = word_tokenize(text)
    filtered = [w for w in tokens if not w in stopwords.words('english')]
    stems = stem_tokens(filtered, stemmer)
    return stems

# converts text to pos_tags
def pos_tokens(text):
    stems = tokenize(text)
    list_of_stems = list(map(lambda x: [x], stems))
    result = [val for sublist in list_of_stems for val in pos_tag(sublist)]
    return result
	
# convert text to filtered tokens with pos_tag in "NN,JJ,NNS"
def filtered_tokens(text):
    pos_tags = pos_tokens(text)
    result = []
    for each in pos_tags:
        if each[1] in ['NN', 'JJ', 'NNS']:
            result.append(each[0])
    return result

def read_csv_to_dict(filepath, parsedPath):

    # read from csv into json format
    inputCsv = open(filepath, 'rU')
    reader = csv.DictReader(inputCsv)
    out = json.dumps([row for row in reader])

    # remove code blocks
    # remove html tags and http links
    # remove tags
    code_pattern = r'(\<code.*?<\/code>)'
    out = re.sub(code_pattern,"",out)
    pattern = r'(<.*?>)'
    out = re.sub(pattern,"",out)
    #http_pattern = r'(http.*?\/\/.*?\r?\n)'
    #out = re.sub(http_pattern,"",out)

    out = out.lower()
    #decode('unicode_escape').encode('ascii','ignore').

    # write data to json file
    outputJson = open(parsedPath,'w')
    outputJson.write(out)
    outputJson.close()

def tokenize_data(parsedPath, tokenizedPath):
    parsedFile = open(parsedPath,'r')
    tokenizedFile = open(tokenizedPath,'w')
    data = json.load(parsedFile)

    feeds = []
    for row in data:
        if (row["tags"]==None or row["body"]==None or row["id"]==None or row["body"]==None):
            continue

        row["tags"] = word_tokenize(row["tags"])
        row["body"] = filtered_tokens(row["body"])
        row["title"] = filtered_tokens(row["title"])

        feeds.append(row)

    json.dump(feeds, tokenizedFile)

def main():
    read_csv_to_dict(filepath,parsedPath)
    tokenize_data(parsedPath, tokenizedPath)

if __name__=='__main__':
    main()
