import argparse
import json
import os
import re
from sklearn.metrics import accuracy_score

parser = argparse.ArgumentParser()

parser.add_argument('--articles_path', help='path of the folder containing extracte files and relevant sections')
parser.add_argument('--label_path', help='path of labels')

args = parser.parse_args()

label_mappings = {
    "college/vocational/technical": "college",
    "collegeVocationalTechnical": "college",
    "graduate/professional": "graduate",
    "graduateProfessional": "graduate",
    "middle": "middle",
    "middle(basicallya50/...ystudents.": "middle", 
    "middlelevel": "middle",
    "elementary": "primary",
    "primary": "primary",
    "secondary": "secondary",
    "adult":"adult"
}

with open (args.label_path, "r") as f:
    labels = json.load(f)

for article in labels:
    try:
        labels[article] = label_mappings[labels[article]]
    except KeyError:
        continue





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

    max_count, max_level = max([(primary_count, "primary"), (middle_count, "middle"), (secondary_count, "secondary"), (college_count, "college"), (graduate_count, "graduate")])

    return max_level

def classify(article, article_name):
    edu_level_prediction = find_education_level(article)
    try: # this is for citation based
        temp = article_name.split("_")[3]
    except:# this is for header_extraction based
        temp = article_name
    
    temp = temp.split(".")
    real_article_name1 = f"({temp[0]} et al., {temp[1]})"
    real_article_name2 = f"({temp[0]}, {temp[1]})"
    try:
        label = labels[real_article_name1]
    except:
        try:
            label = labels[real_article_name2]
        except:
            try:
                label = labels[real_article_name1.capitalize()]
            except:
                try:
                    label = labels[real_article_name2.capitalize()]
                except:
                    label = None
    return label, edu_level_prediction

filtering_method = "citation_based" # the other other one is header_extraction
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
        

        label, edu_level_prediction = classify(article, article_name)
        if label!=edu_level_prediction:
            print(label, edu_level_prediction)
            print(article_name)
            count +=1
        if label:
            ground_truths.append(label)
            predictions.append(edu_level_prediction)
else:
    for article_name in os.listdir(folder):
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
        label, edu_level_prediction = classify(filtered_article, article_name.replace('.json',''))
        if label:
            ground_truths.append(label)
            predictions.append(edu_level_prediction)

print(accuracy_score(ground_truths, predictions))
