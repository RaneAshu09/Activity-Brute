from itertools import product
import pandas as pd
import numpy as np
import gspread as gc
import math
from oauth2client.service_account import ServiceAccountCredentials
main_df = pd.read_excel("myfile.xlsx")
main_df.index = np.arange(1,len(main_df)+1)
main_df = main_df.rename_axis(columns="Test Case No. ")
# main_df
percentage = {}
for param, value in zip(main_df["parameter"], main_df["values"]):
    if "%" in value:
        res = any(chr.isdigit() for chr in value)
        if res:
            temp = int(''.join(filter(str.isdigit, value)))
            percentage[param] = temp

main_df = main_df[main_df["parameter"].str.contains("Select") == True]
def Select(param):
    parameter = param.split(" ")
    parameter = [x.capitalize() for x in parameter]
    print(parameter)
    if parameter[0] == "Select":
        return " ".join(parameter[1:])
    else:
        return param

def Concession(param):
    x = param.split(" ")
    if x[-1] == "Concession":
        return " ".join(x[:-1])
    else:
        return param

main_df['parameter'] = main_df["parameter"].apply(Select)
main_df['parameter'] = main_df["parameter"].apply(Concession)

brute = {}
for param, value in zip(main_df["parameter"], main_df["values"]):
    if "Infeasible Input" in value:
        continue
    elif "Concession" in value:
        continue
    else:
        brute[param] = value.split(",")

def expand_grid(dictionary):
    return pd.DataFrame([row for row in product(*dictionary.values())], 
                       columns=dictionary.keys()) 


main_df1 = expand_grid(brute)
# def Infeasible():
#     main_df1.loc[main_df1['Gender'] == 'Male','Widow'] = 'NA'
#     main_df1.loc[main_df1['Passenger Type'] == 'Senior Citizen','Student'] = 'NA'
#     main_df1.loc[main_df1['Passenger Type'] == 'Child','Widow'] = 'NA'


z = []
for param, value in zip(main_df["parameter"],main_df["values"]):
    if "Infeasible Input" in value:
        z.append(param)
final_infeasible = list(map(str.strip, z))
print(final_infeasible)
final = []
	
for x in final_infeasible:
	    j = x.split(" And ")
	    final.append(j)

print(final)

final_infe = []
	
for i in final:
	    infe = []
	    for k in i:
	        if "-" in k:
	            al = k.split("-")
	            infe = al
	        else:
	            infe.append(k)
	    final_infe.append(infe)

print(final_infe)
last_final = []
for singers in final_infe:
    last = []
    for singer in singers:
        last.append(singer.title())
    last_final.append(last)


print(last_final)
for i in last_final:
	    if len(i) == 3:
	        main_df1.loc[main_df1[i[0]] == i[1],i[2]] = 'NA'
	    elif len(i) == 2:
	        main_df1.loc[main_df1[i[0]] == "",i[1]] = 'NA'

pd.DataFrame.drop_duplicates(main_df1,inplace=True)
main_df1.index = np.arange(1,len(main_df1)+1)
main_df1 = main_df1.rename_axis(index="Test Case No.")



gc1 = gc.service_account(filename='creds.json')
sh = gc1.open_by_key('1mezaJvNJ_jR-I-keGnJVUGyolyfsrWD5LWU2QLM_Gu8')
worksheet2 = sh.get_worksheet(1)
res2 = worksheet2.get_all_records()

df = pd.DataFrame.from_dict(res2)
df.set_index('', inplace=True)

worksheet3 = sh.get_worksheet(2)
res3 = worksheet3.get_all_records()
df1 = pd.DataFrame.from_dict(res3)
df1.index

df2=df1.reset_index()
df3=df1.set_index('Concession Type Name')

df3.drop('Concession Category Name', axis=1, inplace=True)

df3.reset_index(inplace=True)
Abb = dict(df3.values)

#journey = {"Sleeper": "SL", "First": "1st", "AC-I": "1AC"}
journey = {"Sleeper":"SL","First":"1st","AC-I":"1AC","Second":"2nd","AC-II":"2AC","AC-III":"3AC","CC":"CC"}


#main_df1.fillna(value='NA', inplace=True)
print(main_df1)
concessions = []
for row in main_df1.to_dict(orient="records"):
    alist = []
    jour = row['Journey Class']
    jour = jour.strip()
    # print(row['Test Case No.'])
    for i in list(row.values())[2:]:
        #print(i)
        i = i.strip()
        #print(i)
        if i == "NA":
            alist.append(np.NaN)
            continue
        elif i == "Adult":
            alist.append(np.NaN)
            continue
        elif i == "NS":
            alist.append(np.NaN)
            continue
        elif " and " in i:
            x = i.split(' and ')
            stripped = [s.strip() for s in x]
            y = []
            for item in stripped:
                y.append(df.loc[journey[jour]][Abb[item]])
            y.sort(reverse=True)
            if len(y) == 2:
                # x1 = y[0] + 0.05*y[1]
                x1 = y[0] + (percentage['2']/100)*y[1]
                alist.append(x1)
            elif len(y) == 3:
                # x1 = y[0] + 0.07*y[1]
                x1 = y[0] + (percentage['3']/100)*y[1]
                alist.append(x1)
            else:
                # x1 = y[0] + 0.10*y[1]
                x1 = y[0] + (percentage['If No. of concession types  selected more than 3']/100)*y[1]
                alist.append(x1)
            continue
        #print(Abb[i])
        alist.append(df.loc[journey[jour]][Abb[i]])
    #for j in alist:
        #print(type(j))
    
    #print(alist)
    cleanedList = [x for x in alist if (math.isnan(x) == False)]
    cleanedList.sort(reverse=True)
    #print(cleanedList)
    concession = 0
    if len(cleanedList) > 3:
        # concession = cleanedList[0] + cleanedList[1]*0.10
        concession = cleanedList[0] + cleanedList[1] *(percentage['If No. of concession types  selected more than 3']/100)
    elif len(cleanedList) == 3:
        # concession = cleanedList[0] + cleanedList[1]*0.07
        concession = cleanedList[0] + cleanedList[1]*(percentage['3']/100)

    elif len(cleanedList) == 2:
        # concession = cleanedList[0] + cleanedList[1]*0.05
        concession = cleanedList[0] + cleanedList[1]*(percentage['2']/100)

    elif len(cleanedList) == 1:
        concession = cleanedList[0]
    else:
        concession = 0
    #print(concession)

    if concession > 100:
        concession = percentage['Maximum Allowed Concession']
    #"{:.2f}".format(concession)
    concession = round(concession, 2)

    concessions.append(concession)


# concessions = []
# for row in main_df1.to_dict(orient="records"):
#     alist=[]
#     jour=row['Journey Class']
#     jour = jour.strip()
#     dis = row['Disabled Passenger']
#     dis = dis.strip()
#     #print(dis)
#     if dis == 'Handicapped':
#         alist.append(df.loc[journey[jour]][Abb['Orthopadically Handicapped']])
#     elif dis == 'Handicapped and Mentally Retarded':
#         dis_p =[]
#         dis_p.append(df.loc[journey[jour]][Abb['Orthopadically Handicapped']]) 
#         dis_p.append(df.loc[journey[jour]][Abb['Mentally Retarded']])
#         dis_p.sort(reverse=True)
#         # x1 = dis_p[0]+0.05*dis_p[1]
#         x1 = dis_p[0]+(percentage['2']/100)*dis_p[1]
#         alist.append(x1)
#     elif dis == 'Mentally Retarded':
#         alist.append(df.loc[journey[jour]][Abb[dis]])
#     else:
#         alist.append(0)
    
#     pat = row['Patient']
#     pat = pat.strip()
#     #print(pat)
#     if "and" in pat:
#         x = pat.split('and')
#         stripped = [s.strip() for s in x]
#         y = []
#         for item in stripped:
#             y.append(df.loc[journey[jour]][Abb[item]])
#         y.sort(reverse=True)
#         if len(y) == 2:
#             x1 = y[0] + (percentage['2']/100)*y[1]
#             alist.append(x1)
#         elif len(y) == 3:
#             x1=y[0] + (percentage['3']/100)*y[1]
#             alist.append(x1)
#         else:
#             x1 = y[0] + (percentage['If No. of concession types  selected more than 3']/100)*y[1]
#             alist.append(x1)
#     elif pat == "NS":
#         alist.append(0)
#     else:
#         alist.append(df.loc[journey[jour]][Abb[pat]])
        
    
#     wid = row['Widow']
#     wid = wid.strip()
#     if wid == 'NS' or wid == 'NA' :
#         alist.append(0)
#     else:
#         alist.append(df.loc[journey[jour]][Abb[wid]])
    
#     stud = row['Student']
#     stud = stud.strip()
#     if stud == 'NS' or stud =="NA":
#         alist.append(0)      
#     else:
#         alist.append(df.loc[journey[jour]][Abb[stud]])
    
#     pass_type = row['Passenger Type']
#     pass_type = pass_type.strip()
#     if pass_type == "Adult":
#         alist.append(0)
#     else:
#         alist.append(df.loc[journey[jour]][Abb[pass_type]])
#     alist.sort(reverse=True)
    
#     concession = 0;
#     if alist.count(0) == 4:
#         concession = alist[0]
#     elif alist.count(0) == 3:
#         concession = alist[0] + alist[1]*(percentage['2']/100)
#     elif alist.count(0) == 2:
#         concession = alist[0] + alist[1]*(percentage['3']/100)
#     #elif alist.count(0) <=1:
#         #concession = alis[0] + alist[1]*0.10
#     else:
#         concession = alist[0] + alist[1]*(percentage['If No. of concession types  selected more than 3']/100)
#         #concession = 0;
#         #Condition can be changed
    
    # if concession>100:
    #     concession = percentage['Maximum Allowed Concession']
    # #"{:.2f}".format(concession)
    # concession = round(concession,2)
    
    # concessions.append(concession)

main_df1['Expected Concession'] = concessions
main_df1['Actual Output'] = ""
main_df1["Remark (Pass/Fail)"]=""

def create_tuple_for_for_columns(df_a, multi_level_col):
    """
    Create a columns tuple that can be pandas MultiIndex to create multi level column

    :param df_a: pandas dataframe containing the columns that must form the first level of the multi index
    :param multi_level_col: name of second level column
    :return: tuple containing (second_level_col, firs_level_cols)
    """
    temp_columns = []
    for item in df_a.columns:
        temp_columns.append((multi_level_col, item))
    return temp_columns

columns = create_tuple_for_for_columns(main_df1, 'Automated Test suite for RRS (Condensed Form)')
main_df1.columns = pd.MultiIndex.from_tuples(columns)
main_df1.fillna(value='NA', inplace=True)
main_df1.replace(to_replace ="NS",
                 value =np.nan,inplace=True)

#main_df1.isnull().sum()
#main_df1.isnull().sum()
main_df1.to_excel("Final.xlsx")
