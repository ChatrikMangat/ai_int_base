import jsonlines
import pickle
from pathlib import Path

# This script extracts relevant data from the .jsonl file provided in Kirchner et. al. (2022)
path = Path('data_dict.pkl')

if path.is_file():
    # If data file is already present, skip extraction
    with open('data_dict.pkl','rb') as fname:
        data_dict = pickle.load(fname)
    with open('info_dict.pkl','rb') as fname:
        info_dict = pickle.load(fname)
else:
    data_dict = {}
    info_dict = {}
    i = 0
    with jsonlines.open('alignment_texts.jsonl', 'r') as reader:
        print(reader)
        for entry in reader:
            try:
                if(entry['source'] == 'arxiv' and entry['alignment_text'] == 'pos'):
                    # Save arxiv paper abstract in data dictionary
                    data_dict.update({str(i) : entry['abstract']})
                    # Save additional information in info dictionary
                    info_dict.update({str(i) : {}})
                    if 'title' in entry.keys(): 
                        info_dict[str(i)].update({'title' : entry['title']})
                    if 'authors' in entry.keys(): 
                        info_dict[str(i)].update({'authors' : entry['authors']})
                    if 'url' in entry.keys():
                        info_dict[str(i)].update({'url' : entry['url']})
                    
                    print("Total papers found: ", i) 
                    i = i+1
            except KeyError as err:
                pass
            
            # Save data files in pickle format
            with open('data_dict.pkl', 'wb') as fname:
                pickle.dump(data_dict,fname)
            with open('info_dict.pkl', 'wb') as oname:
                pickle.dump(info_dict,oname)

print("Data extracted and stored in data_dict.pkl and info_dict.pkl")
