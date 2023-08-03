import argparse
import math
import os
import re

parser = argparse.ArgumentParser()

parser.add_argument('--pdf_extract_dir', help = 'path of the folder containing text for extracted pdfs')
args = parser.parse_args()
folder = args.pdf_extract_dir

al_articles = len(os.listdir(folder))
avg_ref = 0

for file in os.listdir(folder):
    if "json" in file:
        continue
    with open(f"{folder}/{file}", "r") as f:
        article = f.read()
    article = article.lower()
 
    etal_count = len(re.findall("et al.",article))
    year_count = len(re.findall(r"\([0-9]+\)",article))
    number_count = len(re.findall(r"\[[0-9]+\]",article))
    
    one_author_count = len(re.findall(r"[a-z\.]+ [0-9]+",article))
    one_author_count += len(re.findall(r"[a-z\.]+, [0-9]+",article))
    one_author_count += len(re.findall(r"[a-z\.]+,[0-9]+",article))
    
    two_author_count = len(re.findall(r"[a-z\.]+ and [a-z\.]+ [0-9]+",article))
    two_author_count += len(re.findall(r"[a-z\.]+ and [a-z\.]+, [0-9]+",article))
    two_author_count += len(re.findall(r"[a-z\.]+ and [a-z\.]+,[0-9]+",article))
    two_author_count += len(re.findall(r"[a-z\.]+ & [a-z\.]+ [0-9]+",article))
    two_author_count += len(re.findall(r"[a-z\.]+ & [a-z\.]+, [0-9]+",article))
    two_author_count += len(re.findall(r"[a-z\.]+ & [a-z\.]+,[0-9]+",article))

    total_ref = etal_count+year_count+two_author_count+number_count+one_author_count

    paragraphs = article.split("\n\n")
    count_highcite_paragraphs = 0
    delete_paragraphs = []
    for paragraph in paragraphs:
        etal_count = len(re.findall("et al.",paragraph))
        year_count = len(re.findall(r"\([0-9]+\)",paragraph))
        number_count = len(re.findall(r"\[[0-9]+\]",paragraph))
        
        one_author_count = len(re.findall(r"[a-z\.]+ [0-9]+",paragraph))
        one_author_count += len(re.findall(r"[a-z\.]+, [0-9]+",paragraph))
        one_author_count += len(re.findall(r"[a-z\.]+,[0-9]+",paragraph))
        
        two_author_count = len(re.findall(r"[a-z\.]+ and [a-z\.]+ [0-9]+",paragraph))
        two_author_count += len(re.findall(r"[a-z\.]+ and [a-z\.]+, [0-9]+",paragraph))
        two_author_count += len(re.findall(r"[a-z\.]+ and [a-z\.]+,[0-9]+",paragraph))
        two_author_count += len(re.findall(r"[a-z\.]+ & [a-z\.]+ [0-9]+",paragraph))
        two_author_count += len(re.findall(r"[a-z\.]+ & [a-z\.]+, [0-9]+",paragraph))
        two_author_count += len(re.findall(r"[a-z\.]+ & [a-z\.]+,[0-9]+",paragraph))
        
        total_cite_paragraph = etal_count+year_count+two_author_count+number_count+one_author_count
        if total_cite_paragraph >= int(math.ceil(0.3 * total_ref)):
            count_highcite_paragraphs += 1
            delete_paragraphs.append(paragraph)
    if (count_highcite_paragraphs == len(paragraphs)) and (total_ref!=0):
        print(file)
    else:
        for delete_par in delete_paragraphs:
            article = article.replace(delete_par,"")
    with open(f"{folder}/citation_based_filter_{file}", "w") as f:
        f.write(article)
