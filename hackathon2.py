import ratemyprofessor
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import json
import requests
import requests_cache
from urllib.request import urlopen
requests_cache.install_cache("mycache")

# making dataframe
response = requests.post('https://ucannualwage.ucop.edu/wage/search.action', params = {'_search':"false",'nd':"1674788674156",'rows':"46322",'sidx':"EAW_LST_NAM",'sord':"asc",'year':"2021",'location':"Davis",'title':'Prof'})
response.raise_for_status()
results = json.loads(response.text.replace("\'", "\""))

#changed results into dataframe and converted 'rows' to a lists of lists which contains the information we need 
results_series = list(pd.DataFrame(results['rows'])['cell'])
# print(results_series)

# use the lists of lists to create a dataframe and assign the correct column names found on website 
results_df = pd.DataFrame(results_series,columns = ['ID','Year','Location','First Name','Last Name','Title','Gross Pay','Regular Pay','Overtime Pay','Other Pay'])

# get rid of all rows that do not have a publicly available name 
# results_df = results_df[~results_df.select_dtypes(['object']).eq('*****').any(1)]


#simplify the dataframe to only contain the required columns 
name_pay_df = results_df[['First Name','Last Name']]

name_pay_df = name_pay_df[name_pay_df['Last Name'] != '*****']

# joining 
name_pay_df = name_pay_df['First Name'] + " "+name_pay_df['Last Name']
name_pay_df = name_pay_df.head(10)

column_names = ['name']
name_pay_df.columns = column_names
print(name_pay_df)

# name_pay_df.to_csv('file1.csv')
name_pay_df = name_pay_df.to_frame(name = "name")
listr = []
for _, row in name_pay_df.iterrows():
    professor = ratemyprofessor.get_professor_by_school_and_name(ratemyprofessor.get_school_by_name("University of California Davis"), row['name'])
    if professor is not None:
        item = [row['name'], professor.rating]
    else:
        item = [row['name'], None]
    listr.append(item)
   

df_rating = pd.DataFrame(listr, columns=["name","rating"])


merged_df = name_pay_df.merge(df_rating, on="name", how="left")
print(merged_df)
merged_df_csv = merged_df.to_csv("combined_data.csv", index = False)
# # RMP API


# professor.would_take_again
# professor.rating
# professor.difficulty
# professor.name


