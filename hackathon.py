import ratemyprofessor
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import json
import requests
import requests_cache
from urllib.request import urlopen
requests_cache.install_cache("mycache")

response = requests.post('https://ucannualwage.ucop.edu/wage/search.action', params = {'_search':"false",'nd':"1674788674156",'rows':"46322",'sidx':"EAW_LST_NAM",'sord':"asc",'year':"2021",'location':"Davis",'title':'Prof'})
response.raise_for_status()
results = json.loads(response.text.replace("\'", "\""))

#changed results into dataframe and converted 'rows' to a lists of lists which contains the information we need 
results_series = list(pd.DataFrame(results['rows'])['cell'])


# use the lists of lists to create a dataframe and assign the correct column names found on website 
results_df = pd.DataFrame(results_series,columns = ['ID','Year','Location','First Name','Last Name','Title','Gross Pay','Regular Pay','Overtime Pay','Other Pay'])

# get rid of all rows that do not have a publicly available name 
# results_df = results_df[~results_df.select_dtypes(['object']).eq('*****').any(1)]


#simplify the dataframe to only contain the required columns 
name_pay_df = results_df[['First Name','Last Name']]
# name_pay_df = name_pay_df.head(00)


#function to get email name
def find_email(name):
      email_list = []
      #query directory for name
      response = requests.get("https://org.ucdavis.edu/directory-search/person",params ={'query':name})
      results = response.json()

      #some return multiple results so we need to append all emails to a list
      for item in results:
          email_list.append(item['mail'])
      
      #get first non-None value from list. If there is no non-None value return Not_Found instead
      email = next((d for d in email_list if d is not None), 'Not_Found')

      return email

  
emails = []
for index in range(len(name_pay_df["First Name"])):
    #have to preprocess first names to get rid of middle names and replace double quotes with single 
    firstName = name_pay_df.iloc[index]["First Name"].split()[0]
    firstName = firstName.replace("\"", "\'")

    #preprocess last names to get rid of hyphens and replace double quotes with single D"Cruz -> D'Cruz
    lastName = name_pay_df.iloc[index]["Last Name"].split("-")[0]
    lastName = lastName.replace("\"", "\'")

    #concatenate them together 
    string_name = firstName + " " + lastName

    #get email name for each person
    emails.append(find_email(string_name))



#create new column and store email name for each person
name_email_df = name_pay_df.assign(email = emails)
name_email_df = name_email_df[name_email_df['Last Name'] != '*****']
name_email_df = name_email_df[name_email_df['email'] != 'Not_Found']
# print(name_email_df)

# make a list of the 

# RMP API
professor = ratemyprofessor.get_professor_by_school_and_name(
    ratemyprofessor.get_school_by_name("University of California Davis"), "Daryl Posnett")

if professor is not None:
    print("%sworks in the %s Department of %s." % (professor.name, professor.department, professor.school.name))
    print("Rating: %s / 5.0" % professor.rating)
    print("Difficulty: %s / 5.0" % professor.difficulty)
    print("Total Ratings: %s" % professor.num_ratings)
    if professor.would_take_again is not None:
        print(("Would Take Again: %s" % round(professor.would_take_again, 1)) + '%')
    else:
        print("Would Take Again: N/A")

# how to connect the 