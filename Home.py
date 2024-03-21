#######################
# Import libraries
import numpy
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import streamlit_shadcn_ui as ui
import plotly.graph_objects as go

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
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)

#######################
# Load data
df_overview = pd.read_csv('data/staff-info.csv')


#######################
# Sidebar
# with st.sidebar:
#     # Default selection for filters
#     default_option = "All"

#     nationality_options = [default_option] + list(df_overview['Nationality'].unique())
#     nationality_filter = st.sidebar.selectbox("Select Nationality:", nationality_options, index=nationality_options.index(default_option))
    
#     profession_options = [default_option] + list(df_overview['IAEA Profession'].unique())
#     profession_filter = st.sidebar.selectbox("Select Profession:", profession_options, index=profession_options.index(default_option))
    
#     academic_options = [default_option] + list(df_overview['Academic'].unique())
#     academic_filter = st.sidebar.selectbox("Select Academic Background:", academic_options, index=academic_options.index(default_option))
    
#     # Filter data
#     filtered_data = df_overview.copy()
#     if nationality_filter != default_option:
#         filtered_data = filtered_data[filtered_data['Nationality'] == nationality_filter]

#     if profession_filter != default_option:
#         filtered_data = filtered_data[filtered_data['IAEA Profession'] == profession_filter]

#     if academic_filter != default_option:
#         filtered_data = filtered_data[filtered_data['Academic'] == academic_filter]

#     filtered_data = filtered_data.reset_index(drop=True)


st.title('🏂 IAEA Department of Safeguards Dashboard')

selected_color_theme = 'blues'

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

    button.style.position = 'relative';
    button.style.top = '10px';
    button.style.left = '20px';

    </script>
    '''
    st.components.v1.html(js, width=0, height=0)

######################
# Dashboard Main Panel
    


# Tabs
tab1, tab2, tab3 = st.tabs([':sunglasses: **Generational**', ':globe_with_meridians: **Nationality**', ':office: **IAEA Profession**']);

# st.write("Selected:", tabValue)
with tab1:
    diversity_distribution = df_overview['Generational'].value_counts(sort=False)
    generations_list = diversity_distribution.index.tolist()

    ## calculate bubble size
    # Convert the Series to a DataFrame
    df_diversity = diversity_distribution.reset_index()
    df_diversity.columns = ['Generational', 'Count']

    # Calculate proportions
    min_count, max_count = df_diversity['Count'].min(), df_diversity['Count'].max()
    range_min, range_max = 120, 200

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
                style_button(0, i, RAINBOW_COLORS[i], size_value)
                if btn:
                    st.session_state['generational'] = generation
                    st.session_state['profession'] = ''
                    st.switch_page("pages/Staff_Details.py")



with tab2:
    # st.markdown('### Nationality')
    nationality_distribution = df_overview['Nationality'].value_counts().reset_index()
    nationality_distribution.columns = ['Nationality', 'count']
    choropleth = px.choropleth(nationality_distribution, 
                        locations="Nationality",
                        locationmode="country names",
                        color="count",
                        color_continuous_scale=selected_color_theme,
                        hover_name="Nationality",
                        projection="natural earth")
    choropleth.update_layout(geo=dict(showcoastlines=True))
    st.plotly_chart(choropleth, use_container_width=True)

with tab3:
    profession_distribution = df_overview['IAEA Profession'].value_counts(sort=False)
    profession_list = profession_distribution.index.tolist()

    ## calculate bubble size
    # Convert the Series to a DataFrame
    df_profession = profession_distribution.reset_index()
    df_profession.columns = ['Profession', 'Count']

    # Calculate proportions
    min_count, max_count = df_profession['Count'].min(), df_profession['Count'].max()
    range_min, range_max = 120, 200

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
                style_button(2, i, RAINBOW_COLORS[i], size_value)
                if btn:
                    st.session_state['profession'] = profession
                    st.session_state['generational'] = ''
                    st.switch_page("pages/Staff_Details.py")












#######################

    
# with st.expander('About', expanded=True):
#     st.write('''
#         - Data: [Department of Safeguards]().
#         - :orange[**Diversity**]: staff are from varied backgrounds, education, career paths, and ages
#         ''')
