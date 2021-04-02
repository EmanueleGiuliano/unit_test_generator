import os
import sys
import re
import ast 
from os import listdir
from os.path import isfile, join

def check_keywords(word, keyword_list):    
    for keyword in keyword_list:        
        if re.search(keyword, word):
            #print("\t" + word + " matched with \t" + keyword)
            return True
    return False

def read_dictionary(data):            
    # reconstructing the data as a dictionary 
    d = ast.literal_eval(data) 
    
    print("attributes dictionary : ", type(d)) 
    print(d) 

    return d


def generate_test(content, keyword_list, test_model, test_keywords, classToBeTested, output_package, attributes_dictionary):
    words = content.split()
    attributes = list()

    print("file content: \n")
    print(words)  

    print("attributes found: \n")
    for word in words:
        #check_keywords(word, keyword_list)        
        if not check_keywords(word, keyword_list):
            print(word)
            attributes.append(word)
    
    setters = ""
    assertions = ""

    #builds setters and assertions
    for attribute in attributes:      
      if(attribute != classToBeTested):
          value_to_set = None
          if attribute[:-1] in attributes_dictionary:
              value_to_set = attributes_dictionary[attribute[:-1]]

          attrList = list(attribute)
          attrList[0] = attrList[0].upper()
          attribute = ''.join(attrList)
          attribute = attribute[:-1]
          if value_to_set == None:
              setters = setters + "out.set" + attribute + "();\n"
          else:
              setters = setters + "out.set" + attribute + "("+value_to_set+");\n"
          assertions = assertions + "assertNotNull("+"out.get"+attribute+"());\n"

    test_model = test_model.replace("[classToBeTested]",classToBeTested)
    test_model = test_model.replace("[setters]", setters)
    test_model = test_model.replace("[assertions]", assertions)
    test_model = test_model.replace("[outputPackage]", output_package)
    
    print("generated test:\n")
    print(test_model)

    return test_model

if len(sys.argv) > 4:
    print('You have specified too many arguments')
    sys.exit()

if len(sys.argv) < 4:
    print('You need to specify the path to be listed and the output package')
    sys.exit()

input_path = sys.argv[1]
output_path = sys.argv[2]
output_package = sys.argv[3]

keys_file = open(".\special_keywords.txt", "r")
special_keywords = keys_file.read().split()
keys_file.close()

test_model_file = open(".\\test_model.txt", "r")
test_model = test_model_file.read()
test_model_file.close()

test_keywords_file = open(".\\test_keywords.txt", "r")
test_keywords = test_keywords_file.read()
test_keywords_file.close()

field_values_file = open(".\\field_values.json", "r")
field_values = field_values_file.read()
field_values_file.close()

attributes_dictionary = read_dictionary(field_values)

print("skipping these patterns: \n")
print(special_keywords)

if not os.path.isdir(input_path):
    print('The path specified does not exist')
    sys.exit()

print('reading data from: \t' + input_path + '\n')
print('writing data into: \t' + output_path + '\n')

onlyfiles = [f for f in listdir(input_path) if isfile(join(input_path, f))]

print("files to be processed: ")
print(onlyfiles)
print("\n")

for element in onlyfiles:
    f = open(input_path+"\\"+element, "r")
    print(".... generating test for class: \t" + element + "....")

    splittedFileName = element.split(".")
    classToBeTested = splittedFileName[0]

    fwr = open(output_path+"\\"+ classToBeTested + "Test.java", "w")
    fwr.write(generate_test(f.read(), special_keywords, test_model, test_keywords, classToBeTested, output_package, attributes_dictionary))
    fwr.close()
    f.close()

