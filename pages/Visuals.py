# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.
import csv


# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)
with open('data.csv', mode='r') as Csv: #NEW
    csvread = csv.reader(Csv) #NEW
    mydict = dict((rows[0],rows[1]) for rows in csvread) #NEW
    del mydict['Stats']
    count = 0
    for value in mydict.values():
        if value == "0":
            count += 1
    if count < 8:
        st.title("Your Hero is Ready!! 📈")
        st.write("The last step is to give them a name!")
    else:
        st.title("Your Hero Isn't Ready Yet!! 😔")
        st.write("Give your hero a name, and modify their abilities in the Survey Page!")
# PAGE TITLE AND INFORMATION


if 'supName' not in st.session_state:
    st.session_state.supName = ""
hero_Name = st.text_input("What is Your Superhero Name?", value= st.session_state.supName, 
                          placeholder= 'I am . . .')
st.session_state.supName = hero_Name
#Otherwise
if not hero_Name:
    hero_Name = 'Your Hero'


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header('Stat Sheet for {}'.format(hero_Name))



def convert2Json(csv_path, json_path):
    jsonData0 = {}
    jsonData1 = {}
    with open(csv_path, encoding='utf-8') as csvFile:

        csvData = csv.DictReader(csvFile)
        
        for rows in csvData:
            key = rows['Stats']
            jsonData0[key] = rows['Proficiency']
        jsonData1[hero_Name] = jsonData0
        
    with open(json_path, 'w', encoding= 'utf-8') as jsonFile:
        jsonFile.write(json.dumps(jsonData1, indent= 5))

csv_path = r'data.csv'
json_path = r'data.json'



# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.
def ifExists():
    if os.path.exists('data.csv') and os.path.exists('data.json'):
        return True
    else:
        return False
def hasSize():
    if os.path.getsize('data.csv') > 0 and os.path.getsize('data.json') > 0:
        return True
    else:
        return False

if os.path.exists('data.csv') and os.path.exists('data.json'):
    csvFile = pd.read_csv('data.csv')
    st.dataframe(csvFile, hide_index= True)
    convert2Json(csv_path, json_path)
    with open('data.json') as json_file:  #I dont understand but this line of code is the only thing holding this project together.
        statData = json.load(json_file)
else:
    st.info("TODO: Add your data loading logic here.")



# GRAPH CREATION

# Create Dataframe based on Stats sheet
dfCsv = pd.read_csv(csv_path)
#dfJson = pd.read_json(json_path)
st.divider()
st.header("Graphs")
st.image('images/Graph.webp', width = 150)
# GRAPH 1: STATIC GRAPH

st.subheader(f"Static: Histogram of {hero_Name}'s Stats! ") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
if not ifExists():
    st.warning("Placeholder for your first graph.")
else:
    st.bar_chart(dfCsv, x = 'Stats', y = 'Proficiency')
    st.write('Description: Bar chart providing a visual for your selected stats.')


# GRAPH 2: DYNAMIC GRAPH
st.subheader("Dynamic: Line Chart by Power Level + Stat Filter") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TODO:
if 'xVar' not in st.session_state: #NEW
    st.session_state.xVar = 0
if 'yVar' not in st.session_state: #NEW
    st.session_state.yVar = 100
xVar = st.slider('Point Index Minimum', min_value = 0, max_value= 100,  
                 value = st.session_state.xVar, step = 10)
yVar = st.slider('Point Index Maximum', min_value = 100, max_value = 500, 
                 value=st.session_state.yVar, step=10)
st.session_state.xVar = xVar
st.session_state.yVar = yVar

if ifExists():

    dataJsonCopy={}
    for (Name, statDict) in statData.items():
        for (Stat,pointValue) in statDict.items():
            dataJsonCopy[Stat] = pointValue[:]
        #st.write(pointValue)
            if st.session_state.xVar > int(pointValue):
            #st.write('hello')
                dataJsonCopy.pop(Stat) #NEW
            if st.session_state.yVar < int(pointValue):
                dataJsonCopy.pop(Stat) #NEW
    statData = dataJsonCopy
    #st.write(statData)
    st.line_chart(statData,x_label='Stats', y_label='Points') #NEW
    st.write('Description: Using Json data, I have constructed a line chart depicting the results from my survey.' \
    ' Two indexes are provided: The minimum and maximum range. Change them via the sliders.' \
    ' They will affect the graph!')
else:
    st.warning("Placeholder for your second graph.") #NEW


# GRAPH 3: DYNAMIC GRAPH
st.subheader("Dynamic: How would you fare against other Supers?") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create another dynamic graph.
# - If you used CSV data for Graph 1 & 2, you MUST use JSON data here (or vice-versa).
# - This graph must also be interactive and use Session State.
# - Remember to add a description and use '#NEW' comments.

#add data.json to bigger json




reorderList = ['Strength', 'Perception', 'Endurance', 'Charisma','Intelligence','Agility','Dexterity','Luck','Power Prowess']


if ifExists():

    #create lists for comparison
    listboy = ['Strength', 'Perception', 'Endurance', 
        'Charisma','Intelligence','Agility','Dexterity',
    'Luck','Superpowers']

    Subaru = [hero_Name]




    #Call json files into existence

    with open('data.json') as currentData:  #NEW, data.json

        currentData = json.load(currentData) #NEW
        unwantedVar = ""
        for (statDict) in currentData.values():
            for (Proficiency, number) in statDict.items():
                if Proficiency not in listboy: #Check for unwanted attributes
                    unwantedVar = Proficiency
                else:
                    unwantedVar = 'Superpowers'    
            currentData[hero_Name]['Superpowers'] = currentData[hero_Name][unwantedVar]
            del currentData[hero_Name][unwantedVar]
        #Dictionary with correct naming!

    with open('opponents.json') as Opp: #NEW
        oppDict = json.load(Opp) #NEW
        st.write('*Go Against . . .*')

#session state for checkboxes 
    if 'selected_opponents' not in st.session_state: #NEW
        st.session_state.selected_opponents = {}

# Create Checkboxes per superhero
    for (Super, statDict) in oppDict.items(): #NEW
        if Super not in st.session_state.selected_opponents: #NEW
            st.session_state.selected_opponents[Super] = False
    # Create checkbox
        Matchup = st.checkbox(f'{Super}', value=st.session_state.selected_opponents[Super], key=f'{Super}') #NEW, key is for if there are duplicate errors
        st.session_state.selected_opponents[Super] = Matchup #NEW
        if Matchup:
            Subaru.append(Super)
            if Super not in currentData:
                currentData[Super] = statDict #add opponent to copy of data.json
    
    with open('data.json', 'w', encoding='utf-8') as jsonWrite: #NEW
        json.dump(currentData, jsonWrite, indent=5) #rewrite old json with new one

    oppNumber = len(Subaru)
    df = pd.read_json('data.json')
    df = df[Subaru] #make sure columns are of only heroes.
    df.reindex(reorderList) #new; make sure indexes are of the stats
    st.title('Graph and Final dataframe')
    st.dataframe(df)
    st.area_chart(df) #NEW
else:
    st.warning("Placeholder for your third graph.") #NEW

st.write("Description: Test your skills against other heroes of reknown! Select their checkbox to compare their stats"
"to yours!")

if st.button('Rerun'):
    st.rerun()