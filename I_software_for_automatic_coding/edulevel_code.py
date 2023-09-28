import argparse
import json
import os
import re

parser = argparse.ArgumentParser()

parser.add_argument('--articles_path', help='path of the folder containing extracte files and relevant sections')

args = parser.parse_args()

#primary/elementary 1,2,3,4,5
# (seven|7)th grade(|ers)
# grade[s]* (seven|7 |6 and 8)

primary_re1 =  r"((fir|1)st grade(|ers))|((seco|2)nd grade(|ers))|((thi|3)rd grade(|ers))|((four|4)th grade(|ers))|((fif|5)th grade(|ers))"
primary_re2 =  r"((fir|1)st-grade(|ers))|((seco|2)nd-grade(|ers))|((thi|3)rd-grade(|ers))|((four|4)th-grade(|ers))|((fif|5)th-grade(|ers))"
primary_re3 = r"grade[s]* (1|first|2|second|3|third|4|fourth|5|fifth)"
primary_re4 = r"kindergarten|elementary"

#middle/middlelevel,6,7,8
middle_re1 =  r"((six|6)th grade(|ers))|((seven|7)th grade(|ers))|((eigh|8)th grade(|ers))"
middle_re2 =  r"((six|6)th-grade(|ers))|((seven|7)th-grade(|ers))|((eigh|8)th-grade(|ers))"
middle_re3 = r"grade[s]* (6|sixth|7|seventh|8|eighth)"
middle_re4 = r"middle school|middle student[s]*|high school"

#secondary 9,10,11,12
secondary_re1 =  r"((nin|9)th grade(|ers))|((ten|10)th grade(|ers))|((eleven|11)th grade(|ers))|((twelf|12)th grade(|ers))"
secondary_re2 =  r"((nin|9)th-grade(|ers))|((ten|10)th-grade(|ers))|((eleven|11)th-grade(|ers))|((twelf|12)th-grade(|ers))"
secondary_re3 = r"grade[s]* (9|ninth|10|tenth|11|eleventh|12|twelfth)"
secondary_re4 = r"secondary"

#'college/vocational/technical/‘collegeVocationalTechnical
"college, university, technical, vocational, undergraduate, semester", 
college_re = r" college | university |technical|vocational|undergraduate|semester"

#graduate/professional’/graduateProfessional
"graduate, professional, postgraduate,  university degree, college degree"
graduate_re = r" graduate |postgraduate|university degree|college degree"
test = set()
def find_education_level(article):
    primary_count = len(re.findall(primary_re1, article))
    primary_count += len(re.findall(primary_re2, article))
    primary_count += len(re.findall(primary_re3, article))
    primary_count += len(re.findall(primary_re4, article))

    middle_count = len(re.findall(middle_re1, article))
    middle_count += len(re.findall(middle_re2, article))
    middle_count += len(re.findall(middle_re3, article))
    middle_count += len(re.findall(middle_re4, article))

    secondary_count = len(re.findall(secondary_re1, article))
    secondary_count += len(re.findall(secondary_re2, article))
    secondary_count += len(re.findall(secondary_re3, article))
    secondary_count += len(re.findall(secondary_re4, article))

    college_count = len(re.findall(college_re, article))

    graduate_count = len(re.findall(graduate_re, article))
  
    _, max_level = max([(primary_count, "primary"), (middle_count, "middle"), (secondary_count, "secondary"), (college_count, "college"), (graduate_count, "graduate")])

    return max_level

filtering_method = "header_extraction" # the other other one is header_extraction
ground_truths = []
predictions = []

folder = args.articles_path
count = 0
if filtering_method == "citation_based":
    for article_name in os.listdir(folder):
        with open(f"{folder}/{article_name}" ,"r") as f:
            article = f.read()
        # further preprocessing
        if "abstract" in article:
            article = article[article.find("abstract"):]
        # another preprocessing
        article = re.sub(' +',' ',article)
        

        edu_level_prediction = find_education_level(article)
        print(article_name)
        print(edu_level_prediction)
        print()
else:
    for article_name in os.listdir(folder):
        if "json" not in article_name:
            continue
        with open(f"{folder}/{article_name.replace('.json','')}" ,"r") as f:
            article = f.read()
        with open(f"{folder}/{article_name}" ,"r") as f:
            related_work = json.load(f)["rw"]
        
        filtered_article = article
        for line in related_work.split(" $^#@ "):
            if line=="" or line == " ":
                continue
            filtered_article = filtered_article.replace(line, "")
        
        # further preprocessing
        if "abstract" in filtered_article:
            filtered_article = filtered_article[filtered_article.find("abstract"):]
        edu_level_prediction = find_education_level(filtered_article)
        print(article_name)
        print(edu_level_prediction)
        print()