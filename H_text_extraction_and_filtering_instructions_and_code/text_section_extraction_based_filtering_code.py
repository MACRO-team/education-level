import argparse
import json
import os

def save_json(out_path, save_dict, indent=4, encoding='utf-8') :
    with open(out_path, 'w+') as f :
        json.dump(save_dict, f, indent=indent, ensure_ascii=False)

parser = argparse.ArgumentParser()

parser.add_argument('--pdf_extract_dir', help = 'path of the folder containing text for extracted pdfs')
parser.add_argument('--output_path', help = 'path of output folder')

args = parser.parse_args()


if not os.path.exists(args.output_path) :
    os.mkdir(args.output_path)

## Getting list of all pdfs
extracted_pdfs = os.listdir("test")

## Iterating over each extracted pdf text and getting Abstract and Methods section
j=0
for pdf_txt in extracted_pdfs :
    
    if os.path.join("test", "test" + pdf_txt + '.json') in extracted_pdfs:
        continue

    print (str(j) + '  /  ' + str(len(extracted_pdfs)))
    j += 1

    extracted_sections = {}

    lines = open(os.path.join("test",pdf_txt),'r').readlines()


    ## related work extraction
    rw_lines = ''
    add_line = False
    end_rw = False
    t=1
    for line in lines :
        line = line.strip('\n').strip()

        #To ignore lines where pdfminer reads random text
        if len(line) > 500 :
            continue

        if ("review of relevant literature" in line.lower()[:50] or 'related work' in line.lower()[:30] or "literature" in line.lower()[:30] or "comparisons" in line.lower()[:30] or "similar work" in line.lower()[:30] or "review of literature" in line.lower()[:30]) and (t==1):
            add_line = True
            t=0

        if add_line :
            if "discussion" in line.lower()[:10] or "conclusion" in line.lower()[:10] or 'keywords' in line.lower()[:8] or 'introduction' in line.lower()[:12] or 'table' in line.lower()[:8] or 'participants' in line.lower()[:17]  or 'sample' in line.lower()[:10] or 'setting and participants' in line.lower()[:30] or 'procedure' in line.lower()[:12]  or 'fig' in line.lower()[:5] or 'independent variables' in line.lower()[:23] or 'research design' in line.lower()[:18]:
                break

            if line == '' and end_rw :
                add_line = False
                break
            if line != '' :
                if line[-1] == '.' :
                    end_rw = True
                rw_lines += ' $^#@ ' + line.strip()

    extracted_sections['rw'] = rw_lines
    extracted_sections['rw_num_words'] = len(rw_lines.split())

    save_json(os.path.join("test", "test" + pdf_txt + '.json'), extracted_sections)
