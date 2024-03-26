import pandas as pd
import streamlit as st

import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
        .stApp {
            background-image: url("data:image/png;base64,%s");
            background-size: cover;
        }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('background.png')

css ='''
<style>
    # .stApp {
    #     background-image: url("https://plus.unsplash.com/premium_photo-1667811946004-7c03b11fcd11?q=80&w=2574&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    #     background-size: cover;
    # }

    [data-testid="stHorizontalBlock"] {
        align-items: center;
        
    }

    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #fff4ec;
    }

    button[data-baseweb="tab"] > div > p {
        font-size: 24px
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)

df_overview = pd.read_csv('data/staff-info.csv')
filtered_data = df_overview.copy()
if st.session_state['generational'] != "":
    filtered_data = filtered_data[filtered_data['Generational'] == st.session_state['generational']]
    st.title(f"Staff of {st.session_state['generational']}")
if st.session_state['profession'] != "":
    filtered_data = filtered_data[filtered_data['IAEA Profession'] == st.session_state['profession']]
    st.title(f"{st.session_state['profession']} Staff")

default_option = "All"

nationality_options = [default_option] + list(filtered_data['Nationality'].unique())
nationality_filter = st.sidebar.selectbox("Select Nationality:", nationality_options, index=nationality_options.index(default_option))

experience_options = [default_option] + list(filtered_data['Pre-IAEA Work Experience'].unique())
experience_filter = st.sidebar.selectbox("Select Work Experience:", experience_options, index=experience_options.index(default_option))

academic_options = [default_option] + list(filtered_data['Academic'].unique())
academic_filter = st.sidebar.selectbox("Select Academic Background:", academic_options, index=academic_options.index(default_option))

if nationality_filter != default_option:
    filtered_data = filtered_data[filtered_data['Nationality'] == nationality_filter]

if experience_filter != default_option:
    filtered_data = filtered_data[filtered_data['Pre-IAEA Work Experience'] == experience_filter]

if academic_filter != default_option:
    filtered_data = filtered_data[filtered_data['Academic'] == academic_filter]

filtered_data = filtered_data.reset_index(drop=True)

# if len(filtered_data) == 0:
#     st.write("no data")
with st.container(border=True):
    # cols = st.columns((1, 3, 6, 6, 3, 1))
    # fields = ["", "Staff ID", 'Name', 'IAEA Profession', "Action", ""]
    cols = st.columns((1,2,3,2))
    fields = ["Staff ID", 'Name', 'IAEA Profession', "Action"]
    for col, field_name in zip(cols, fields):
        # header
        if field_name:
            col.markdown(f'**{field_name}**')

    for idx, staffId in enumerate(filtered_data["Staff ID"]):
        # col0, col1, col2, col3, col4, col5 = st.columns((1, 3, 6, 6, 3, 1))
        col1, col2, col3, col4 = st.columns((1, 2, 3, 2))

        # col0.empty()
        col1.write(str(staffId))
        col2.write(filtered_data["Name"][idx])
        col3.write(filtered_data["IAEA Profession"][idx])
        btn_placeholder = col4.empty()
        # col5.empty()
        
        clicked = btn_placeholder.button(label="See Profile", key=staffId)
        if clicked:
            card_template = """
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
                        <div class="card text-black bg-light mb-3" >
                            <div class="row no-gutters">
                                <div class="col-md-4">
                                    <img src="{}" class="w-50 m-5" alt="avatar">
                                </div>
                                <div class="col-md-8">
                                    <div class="card-body">
                                        <h5 class="card-title">{}({})</h5>
                                        <p class="font-italic">{}</p>
                                        <p class="card-text"><span class=" font-weight-bold">Nationality:</span> {}</p>
                                        <p class="card-text"><strong>Pre IAEA Background:</strong> {}</p>
                                        <p class="card-text">{}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
            """
            gender_text = "She/her"
            avartar_url = "https://avatar.iran.liara.run/public/girl"
            if filtered_data["Gender"][idx] == "Male":
                gender_text = "He/him"
                avartar_url = "https://avatar.iran.liara.run/public/boy"
            
            st.markdown(
                card_template.format(
                    avartar_url, 
                    filtered_data["Name"][idx], 
                    gender_text,
                    filtered_data["IAEA Profession"][idx], 
                    filtered_data["Nationality"][idx], 
                    filtered_data["Pre-IAEA Work Experience"][idx], 

                    "Some brief introduction text to introduce the staff's portfolio. " 
                    ), 
                    unsafe_allow_html=True
                )
# st.session_state