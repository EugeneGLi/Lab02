# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.
import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

#Lets have the survey be a a survey to create character, a la DND and Fallout   


if 'notSubmitted' not in st.session_state:
    st.session_state.notSubmitted = True


def DATA_DISPLAY():
    st.divider() # Adds a horizontal line for visual separation.
    st.header("Current Stats. See Visuals tab for graphs")

# Check if the CSV file exists and is not empty before trying to read it.
    if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:

    # Read the CSV file into a pandas DataFrame.
        current_data_df = pd.read_csv('data.csv')

    # Display the DataFrame as a table.
        st.dataframe(current_data_df, hide_index=True)

    else:
        st.warning("The 'data.csv' file is empty or does not exist yet.")
#Last stat should be their custom stat; will set during survey
#max stat should be 100
#stats should pull from a collective stat pool


# PAGE CONFIGURATION
st.set_page_config(
    page_title="Hero Survey",
    page_icon="🦸📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Let's create a Superhero! 🦸‍♀️🦸")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.


#NAME
if 'name' not in st.session_state:
    st.session_state.name = ""
ability_name = st.text_input("What is Your Superpower?", value= st.session_state.name, 
                             placeholder= 'I have the ability of . . .')
st.session_state.name = ability_name

#Hero other stats and csv creation ONLY if we haven't started yet
my_data = { 'Stats' : ["Strength", "Perception", "Endurance", "Charisma", 
                       "Intelligence","Agility", "Dexterity", "Luck"],
            'Proficiency' : [0,0, 0, 0, 0, 0, 0, 0]}
df = pd.DataFrame(my_data)
df.to_csv("data.csv", index=False, mode = 'w')


#Name for Stat
abilityStat = f'{ability_name} Proficiency'

myList = my_data.get('Stats')
if ability_name:
    myList.append(abilityStat)
    #st.write(myList)
    if abilityStat not in st.session_state.stat_values:
        st.session_state.stat_values[f'{ability_name} Proficiency'] = 0

#hello
if 'stat_values' not in st.session_state:
    st.session_state.stat_values = {stat: 0 for stat in myList}

#st.write(st.session_state.stat_values)

#stat pool and other variables
statPool = 500
placeholderString = 'Please enter a value'

def Imagine(stat,Width):
    return st.image(f'images/{stat}.png', width= Width, output_format="PNG")


def stat_input(stat):
        
    Input, Image = st.columns(2)
    with Input:
        st.session_state.stat_values[stat] = st.number_input(
            stat,
            min_value= 0,
            max_value= statPool - sum([v for k, v in st.session_state.stat_values.items() if k != stat]),
            value= st.session_state.stat_values[stat],
            step= 10,
            key=f'stat_{stat}',
            placeholder= 'Enter a value'
        )
    with Image:
        if stat != abilityStat:
            Imagine(stat, 200)
        else:
            Imagine('Proficiency', 600)
#stat allocation form

with st.form("survey_form") as form:
    

    st.header('Give your hero some stats!')
    Imagine('Vault_Boy', 150)
    st.subheader('Click the Update button on the bottom of your form to save your stat changes.')
    st.write('*This form will NOT save multiple stat changes*')
    st.write('Max points allocated: {}'.format(statPool))
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.

    #stat_input('Strength')
    #stat_input('Perception')


    
    for stat in myList:
        stat_input(stat)
    
    # The submit button for the form.
    updateform = st.form_submit_button('Update', use_container_width= True)
    if updateform:
         st.rerun()
        #Metrics for logging point allocation
    total_used = sum(st.session_state.stat_values.values())
    remaining_total = statPool - total_used
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Stats Allocated", f"{total_used} / {statPool}")
    with col2:
        st.metric("Remaining Stat Points", remaining_total)


submitted = st.button("Submit Data", use_container_width=True)

    # This block of code runs ONLY when the submit button is clicked.
if 'submittedYay' not in st.session_state:
    st.session_state.submittedYay = False
if submitted:
    st.session_state.submittedYay = True
    st.balloons()


if st.session_state.submittedYay:
        st.session_state.notSubmitted = False
        tempdata = []

        if ability_name:
            for stat in myList:
                tempdata.append(st.session_state.stat_values[stat])

            my_data['Proficiency'] = tempdata
            st.session_state.my_Data = my_data
            #st.write(newData)
            df1 = pd.DataFrame(my_data)
            df1.columns = ['col1', 'col2']

            df1.to_csv("data.csv",index=False, mode='w', header=['Stats', 'Proficiency'])

            st.success("Your data has been submitted!")

            st.write(f"Go to the Visuals Tab to view your stat sheet graph.")
            DATA_DISPLAY()
        else:
            st.markdown(f'<h1 style="color:#ff0000;font-size:20px;">{"Please Choose a Superhero Ability!"}</h1>'
                        , unsafe_allow_html=True)


