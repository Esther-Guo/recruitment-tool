import pandas as pd
import streamlit as st

df_overview = pd.read_csv('data/staff-info.csv')
filtered_data = df_overview.copy()
if st.session_state['generational']:
    filtered_data = filtered_data[filtered_data['Generational'] == st.session_state['generational']]
else:
    filtered_data = filtered_data[filtered_data['IAEA Profession'] == st.session_state['profession']]
filtered_data = filtered_data.reset_index(drop=True)

cols = st.columns((1, 2, 2, 1))
fields = ["Staff ID", 'Name', 'IAEA Profession', "Action"]
for col, field_name in zip(cols, fields):
    # header
    col.write(field_name)

for idx, staffId in enumerate(filtered_data["Staff ID"]):
    col1, col2, col3, col4 = st.columns((1, 2, 2, 1))
    col1.write(str(staffId))
    col2.write(filtered_data["Name"][idx])
    col3.write(filtered_data["IAEA Profession"][idx])
    btn_placeholder = col4.empty()
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
st.session_state