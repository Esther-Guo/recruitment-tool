#######################
# Import libraries
from math import ceil
import numpy
import streamlit as st
import pandas as pd
# import altair as alt
import plotly.express as px
# import streamlit_shadcn_ui as ui
# import plotly.graph_objects as go
#######################
# Page configuration
st.set_page_config(
    page_title="IAEA Department of Safeguards Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

# alt.themes.enable("dark")

RAINBOW_COLORS = [
    "#F94144",
    "#F9844A",
    "#43AA8B",
    "#277DA1",
    "#F9C74F",
    "#90BE6D",
    "#4D908E",
    "#F8961E",
    "#F3722C",
    "#577590"
]

css ='''
<style>
    .stApp {
        background-image: url("https://upload.wikimedia.org/wikipedia/commons/1/1e/International_Atomic_Energy_Agency_Logo.svg");
        background-position: 95% 50px; /* Positions the background image at the top right corner */
        background-repeat: no-repeat; 
        background-size: 100px 100px;
        background-color: #599fe6;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    button[data-baseweb="tab"] > div > p {
        font-size: 20px
    }

</style>
'''
st.markdown(css, unsafe_allow_html=True)


## set image as background
# import base64

# def get_base64_of_bin_file(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# def set_gif_as_page_bg(png_file):
#     bin_str = get_base64_of_bin_file(png_file)
#     page_bg_img = '''
#     <style>
#     .stApp {
#     background-image: url("data:image/gif;base64,%s");
#     background-size: cover;
#     }
#     </style>
#     ''' % bin_str
    
#     st.markdown(page_bg_img, unsafe_allow_html=True)
#     return

# set_gif_as_page_bg('live_background.gif')

#######################
# Load data
df_overview = pd.read_csv('data/staff-info.csv')

if 'generational' not in st.session_state:
    st.session_state['generational'] = ''
    
if 'profession' not in st.session_state:
    st.session_state['profession'] = ''

if 'nationality' not in st.session_state:
    st.session_state['nationality'] = ''

if 'search_text' not in st.session_state:
    st.session_state['search_text'] = ''
if st.session_state.search_text:
    st.session_state.search_text = ""
#######################


st.title('Department of Safeguards Dashboard')


def style_button(tab_idx:int, n_element:int, color:str, size: int):
    js = fr'''
    <script>
    // Find all tabs
    const tabs = window.parent.document.querySelectorAll('[data-baseweb="tab-panel"]');
    // Find all the buttons
    var buttons = tabs[{tab_idx}].getElementsByClassName("stButton");
    
    // Select only one button
    var button = buttons[{n_element}].getElementsByTagName("button")[0];

    // Modify the button
    button.style.backgroundColor = '{color}';
    button.style.border = 'none';
    button.style.width =  `{size}px`;
    button.style.height = `{size}px`;
    button.style.borderRadius = '50%'; 
    button.style.color = 'white'
    button.querySelector('p').style.fontSize = '22px'


    button.style.position = 'relative';
    button.style.top = '10px';
    button.style.left = '20px';

    </script>
    '''
    st.components.v1.html(js, width=0, height=0)

def add_pfp(tab_idx:int, n_element:int):
    js = fr'''
    <script>
    // Find all tabs
    const tabs = window.parent.document.querySelectorAll('[data-baseweb="tab-panel"]');
    // Find all the buttons
    var buttons = tabs[{tab_idx}].getElementsByClassName("stButton");
    
    // Select only one button
    var button = buttons[{n_element}].getElementsByTagName("button")[0];

    // Create image element
    var img1 = document.createElement('img');
    var img2 = document.createElement('img');
    var img3 = document.createElement('img');

    // Set the source of the image (replace with your image URL)
    img1.src = 'https://majors.engin.umich.edu/wp-content/uploads/2019/08/ners-alum-kristine-madden.png';
    img1.style.width =  `90px`;

    img2.src = 'https://majors.engin.umich.edu/wp-content/uploads/2019/08/ners-alum-xiaojin-shen.png';
    img2.style.width =  `60px`;

    img3.src = 'https://majors.engin.umich.edu/wp-content/uploads/2019/09/ners-alum-joel-kulesza.png';
    img3.style.width =  `70px`;

    // Set the style of the image to position it relative to the button
    img1.style.position = 'absolute'; // Position the image absolutely with respect to the button
    img1.style.top = '20%'; // Adjust as needed
    img1.style.left = '25%'; // Adjust as needed
    img1.style.transform = 'translate(-50%, -50%)'; // Center the image relative to the button

    img2.style.position = 'absolute'; // Position the image absolutely with respect to the button
    img2.style.top = '15%'; // Adjust as needed
    img2.style.left = '60%'; // Adjust as needed
    img2.style.transform = 'translate(-50%, -50%)'; // Center the image relative to the button

    img3.style.position = 'absolute'; // Position the image absolutely with respect to the button
    img3.style.top = '90%'; // Adjust as needed
    img3.style.left = '80%'; // Adjust as needed
    img3.style.transform = 'translate(-50%, -50%)'; // Center the image relative to the button

    // Append the image to the button
    button.appendChild(img1);
    button.appendChild(img2);
    button.appendChild(img3);


    </script>
    '''
    st.components.v1.html(js, width=0, height=0)

######################
# Dashboard Main Panel
    

search_text = st.text_input(
        "Search", label_visibility="collapsed", placeholder="Search Staff"
    )
if search_text:
    st.session_state['search_text'] = search_text
    st.switch_page("pages/🌍_Staff_Details.py")

# Tabs
# tab1, tab2, tab3 = st.tabs([':sunglasses: **Generational**', ':globe_with_meridians: **Nationality**', ':office: **IAEA Profession**']);
tab1, tab2, tab3, tab4, tab5 = st.tabs(['**IAEA Profession**', '**Nationality**', '**Academic**', '**Pre-IAEA Work Experience**', '**Generational**'])

# st.write("Selected:", tabValue)

##### IAEA Profession
with tab1:
    profession_distribution = df_overview['IAEA Profession'].value_counts(sort=False)
    profession_list = profession_distribution.index.tolist()

    ## calculate bubble size
    # Convert the Series to a DataFrame
    df_profession = profession_distribution.reset_index()
    df_profession.columns = ['Profession', 'Count']

    # Calculate proportions
    min_count, max_count = df_profession['Count'].min(), df_profession['Count'].max()
    range_min, range_max = 250, 300

    # Apply linear interpolation to map the counts to your desired range
    df_profession['Size'] = df_profession['Count'].apply(
        lambda x: ((x - min_count) / (max_count - min_count)) * (range_max - range_min) + range_min
        if max_count > min_count else range_min
    )

    row1 = st.columns(3)
    row2 = st.columns(3)

    # for col in row1 + row2:
    #     tile = col.container(height=120)
    #     tile.title(":balloon:")

    for i, profession in enumerate(profession_list):
            size_value = df_profession.loc[df_profession['Profession'] == profession, 'Size'].values[0].astype(numpy.int64)
            if i<3:
                tile = row1[i].container()
            else:
                tile = row2[i%3].container()
            with tile:
                btn = st.button(profession, use_container_width=True, key=profession)
            # st.color_picker("Color the button", "#9988dd", key=f"color_{i}")
                style_button(0, i, RAINBOW_COLORS[i], size_value)
                if (i==0):
                    add_pfp(0, i)
                if btn:
                    st.session_state['profession'] = profession
                    st.session_state['generational'] = ''
                    st.switch_page("pages/🌍_Staff_Details.py")



#### 
card_template = """
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
                    <div class="card text-dark bg-light mb-3" style="height: 250px">
                        <img src="{}" class="card-img-top mx-auto mt-3" alt="avatar" style="width: 120px"> <!-- Adjusted class for centering and margin -->
                        <div class="card-body d-flex flex-column align-items-center">
                            <p style="font-size: 20px">{}</p>
                            <p>{}</p>
                        </div>
                    </div>
            """
gender_text = "She/her"
avartar_url = "https://avatar.iran.liara.run/public/girl"

detail_template = """
                    <div style="display: flex; flex-direction: column;">
                        <p>Nationality: {}</p>
                        <p>Pre-IAEA Experience: {}</p>
                        <p>Generational: {}</p>
                    </div>
            """

def style_country_btn(n_element:int, flag_url):
    js = fr'''
    <script>
    // Find all tabs
    const tabs = window.parent.document.querySelectorAll('[data-baseweb="tab-panel"]');
    // Find all the buttons
    var buttons = tabs[1].getElementsByClassName("stButton");
    
    // Select only one button
    var button = buttons[{n_element}].getElementsByTagName("button")[0];

    // Modify the button
    button.style.backgroundImage = `url({flag_url})`;
    button.style.backgroundRepeat = 'no-repeat';
    button.style.backgroundSize = '150px 100px';
    button.style.border = 'none';
    button.style.width =  `150px`;
    button.style.height = `100px`;

    </script>
    '''
    st.components.v1.html(js, width=0, height=0)

country_flag_df = pd.read_csv('data/countries_continents_codes_flags_url.csv')
def get_flag(country_code):
    result = country_flag_df.loc[country_flag_df['alpha-3'] == country_code, 'image_url'].iloc[0]
    
    # If no match is found, return None
    return result if not pd.isna(result) else None

##### Nationality
with tab2:
    col1, col2 = st.columns([1, 3])
    filtered_data = df_overview.copy()

    col1.subheader("Country")
    country_options = list(df_overview['Nationality'].unique())
    for i, country in enumerate(country_options):
        country_btn = col1.button(country, key=country)
        courtry_iso = df_overview.loc[df_overview['Nationality'] == country, 'iso_alpha'].iloc[0]
        flag_url = get_flag(courtry_iso)
        # st.write(flag_url)
        style_country_btn(i, flag_url)
        if country_btn:
            filtered_data = filtered_data[filtered_data['Nationality'] == country]
            filtered_data = filtered_data.reset_index(drop=True)
    
    numOfStaff = len(filtered_data)
    numOfRows =  ceil(numOfStaff/3)

    with col2:
        itemIdx = 0
        for rowIdx in range(0, numOfRows):
            row = st.columns(3)
            for colIdx in range(0, 3):
                if itemIdx <= numOfStaff-1:
                    profile = row[colIdx].container(border=False)
                    staffDf = filtered_data.iloc[itemIdx]
                    if staffDf["Gender"] == "Male":
                        gender_text = "He/him"
                        avartar_url = "https://avatar.iran.liara.run/public/boy"
                    profile.markdown(
                        card_template.format(
                            avartar_url, 
                            staffDf["Name"], 
                            staffDf["IAEA Profession"]
                            ), 
                            unsafe_allow_html=True
                        )
                    expander = profile.expander("More")
                    expander.markdown(detail_template.format(
                            staffDf["Nationality"], 
                            staffDf["Pre-IAEA Work Experience"], 
                            staffDf["Generational"]
                            ), 
                            unsafe_allow_html=True)
                    itemIdx += 1
    #### map + selection box
    # nationality_distribution = df_overview['Nationality'].value_counts().reset_index()
    # nationality_distribution.columns = ['Nationality', 'count']
    # choropleth = px.choropleth(nationality_distribution, 
    #                     locations="Nationality",
    #                     locationmode="country names",
    #                     color="count",
    #                     color_continuous_scale="blues", # https://plotly.com/python/builtin-colorscales/
    #                     hover_name="Nationality",
    #                     projection="natural earth",
    #                     basemap_visible=False,
    #                     width=1000, #need to use both width and height to set size
    #                     height=500
    #                     )
    # choropleth.update_layout(geo=dict(showcoastlines=True))
    # st.plotly_chart(choropleth, use_container_width=True)

    # nationality_options = list(df_overview['Nationality'].unique())
    # st.session_state["nationality"] = st.selectbox("Select Country", nationality_options, index=None)
    # if st.session_state["nationality"]:
    #     st.switch_page("pages/🌍_Staff_Details.py")

##### Academic
with tab3:
    col1, col2 = st.columns([1, 3])
    filtered_data = df_overview.copy()

    col1.subheader("Degree")
    degree_options = list(df_overview['Academic'].unique())[:8]
    for degree in degree_options:
        degree_btn = col1.button(degree, key=degree)
        if degree_btn:
            filtered_data = filtered_data[filtered_data['Academic'] == degree]
            filtered_data = filtered_data.reset_index(drop=True)
    
    numOfStaff = len(filtered_data)
    numOfRows =  ceil(numOfStaff/3)

    
    with col2:
        itemIdx = 0
        for rowIdx in range(0, numOfRows):
            row = st.columns(3)
            for colIdx in range(0, 3):
                if itemIdx <= numOfStaff-1:
                    profile = row[colIdx].container(border=False)
                    staffDf = filtered_data.iloc[itemIdx]
                    if staffDf["Gender"] == "Male":
                        gender_text = "He/him"
                        avartar_url = "https://avatar.iran.liara.run/public/boy"
                    profile.markdown(
                        card_template.format(
                            avartar_url, 
                            staffDf["Name"], 
                            staffDf["IAEA Profession"]
                            ), 
                            unsafe_allow_html=True
                        )
                    expander = profile.expander("More")
                    expander.markdown(detail_template.format(
                            staffDf["Nationality"], 
                            staffDf["Pre-IAEA Work Experience"], 
                            staffDf["Generational"]
                            ), 
                            unsafe_allow_html=True)
                    itemIdx += 1

#### Pre-IAEA Work Experience
with tab4:
    col1, col2 = st.columns([1, 3])
    filtered_data = df_overview.copy()

    col1.subheader("Work Experience")
    exp_options = list(df_overview['Pre-IAEA Work Experience'].unique())
    # col1.write(exp_options)
    for exp in exp_options:
        exp_btn = col1.button(exp, key=exp)
        if exp_btn:
            filtered_data = filtered_data[filtered_data['Pre-IAEA Work Experience'] == exp]
            filtered_data = filtered_data.reset_index(drop=True)
    
    numOfStaff = len(filtered_data)
    numOfRows =  ceil(numOfStaff/3)

    
    with col2:
        itemIdx = 0
        for rowIdx in range(0, numOfRows):
            row = st.columns(3)
            for colIdx in range(0, 3):
                if itemIdx <= numOfStaff-1:
                    profile = row[colIdx].container(border=False)
                    staffDf = filtered_data.iloc[itemIdx]
                    if staffDf["Gender"] == "Male":
                        gender_text = "He/him"
                        avartar_url = "https://avatar.iran.liara.run/public/boy"
                    profile.markdown(
                        card_template.format(
                            avartar_url, 
                            staffDf["Name"], 
                            staffDf["IAEA Profession"]
                            ), 
                            unsafe_allow_html=True
                        )
                    expander = profile.expander("More")
                    expander.markdown(detail_template.format(
                            staffDf["Nationality"], 
                            staffDf["Pre-IAEA Work Experience"], 
                            staffDf["Generational"]
                            ), 
                            unsafe_allow_html=True)
                    itemIdx += 1

#### Generational
with tab5:
    diversity_distribution = df_overview['Generational'].value_counts(sort=False)
    generations_list = diversity_distribution.index.tolist()

    ## calculate bubble size
    # Convert the Series to a DataFrame
    df_diversity = diversity_distribution.reset_index()
    df_diversity.columns = ['Generational', 'Count']

    # Calculate proportions
    min_count, max_count = df_diversity['Count'].min(), df_diversity['Count'].max()
    range_min, range_max = 150, 300

    # Apply linear interpolation to map the counts to your desired range
    df_diversity['Size'] = df_diversity['Count'].apply(
        lambda x: ((x - min_count) / (max_count - min_count)) * (range_max - range_min) + range_min
        if max_count > min_count else range_min
    )

    row1 = st.columns(3)
    row2 = st.columns(3)

    # for col in row1 + row2:
    #     tile = col.container(height=120)
    #     tile.title(":balloon:")

    for i, generation in enumerate(generations_list):
            size_value = df_diversity.loc[df_diversity['Generational'] == generation, 'Size'].values[0].astype(numpy.int64)
            if i<3:
                tile = row1[i].container()
            else:
                tile = row2[i%3].container()
            with tile:
                btn = st.button(generation, use_container_width=True, key=generation)
            # st.color_picker("Color the button", "#9988dd", key=f"color_{i}")
                style_button(4, i, RAINBOW_COLORS[i], size_value)
                if btn:
                    st.session_state['generational'] = generation
                    st.session_state['profession'] = ''
                    st.switch_page("pages/🌍_Staff_Details.py")









#######################

    
# with st.expander("testing", expanded=True):
#     st.write('''
#         - Data: [Department of Safeguards]().
#         - :orange[**Diversity**]: staff are from varied backgrounds, education, career paths, and ages
#         ''')
