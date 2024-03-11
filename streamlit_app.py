#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
# import streamlit_shadcn_ui as ui
import plotly.graph_objects as go

#######################
# Page configuration
st.set_page_config(
    page_title="IAEA Department of Safeguards Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


#######################
# Load data
df_reshaped = pd.read_csv('data/us-population-2010-2019-reshaped.csv')
df_overview = pd.read_csv('data/staff-info.csv')


#######################
# Sidebar
with st.sidebar:
    # Default selection for filters
    default_option = "All"

    nationality_options = [default_option] + list(df_overview['Nationality'].unique())
    nationality_filter = st.sidebar.selectbox("Select Nationality:", nationality_options, index=nationality_options.index(default_option))
    
    profession_options = [default_option] + list(df_overview['IAEA Profession'].unique())
    profession_filter = st.sidebar.selectbox("Select Profession:", profession_options, index=profession_options.index(default_option))
    
    academic_options = [default_option] + list(df_overview['Academic'].unique())
    academic_filter = st.sidebar.selectbox("Select Academic Background:", academic_options, index=academic_options.index(default_option))
    
    # Filter data
    filtered_data = df_overview.copy()
    if nationality_filter != default_option:
        filtered_data = filtered_data[filtered_data['Nationality'] == nationality_filter]

    if profession_filter != default_option:
        filtered_data = filtered_data[filtered_data['IAEA Profession'] == profession_filter]

    if academic_filter != default_option:
        filtered_data = filtered_data[filtered_data['Academic'] == academic_filter]


st.title('🏂 IAEA Department of Safeguards Dashboard')

# ui.tabs(options=['PyGWalker', 'Graphic Walker', 'GWalkR', 'RATH'], default_value='PyGWalker', key="kanaries")

selected_year = 2019
df_selected_year = df_reshaped[df_reshaped.year == selected_year]
df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

selected_color_theme = 'blues'
#######################
# Plots


# Donut chart
def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=90, cornerRadius=50).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=260, height=260)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=64, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=90, cornerRadius=40).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=260, height=260)
  return plot_bg + plot + text



#######################
# Dashboard Main Panel
# col = st.columns((1.5, 4.5, 2), gap='medium')

# with col[0]:

## gender
if len(filtered_data):
    st.markdown('### Diversity')
    gender_distribution = filtered_data['Gender'].value_counts()
    female_portion = gender_distribution.get("Female", 0)
    male_portion = gender_distribution.get("Male", 0)

    donut_chart_female = make_donut(round(female_portion/len(filtered_data)*100), 'Inbound Migration', 'blue')
    donut_chart_male = make_donut(round(male_portion/len(filtered_data)*100), 'Outbound Migration', 'orange')

    gender_col = st.columns((0.2, 1, 1, 0.2))
    with gender_col[1]:
        st.markdown('##### She / her')
        st.altair_chart(donut_chart_female)
    with gender_col[2]:
        st.markdown('##### He / him')
        st.altair_chart(donut_chart_male)

    ## generation
    diversity_distribution = filtered_data['Generational'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=diversity_distribution.index, 
                                values=diversity_distribution.values, 
                                hole=.3, 
                                marker_colors=px.colors.sequential.Blues,
                                textfont_size=32,
                                )])
    # st.write('Generation')
    # Set the figure size
    fig.update_layout(height=500, width=500) 
    st.plotly_chart(fig, use_container_width=True)

else:
    st.markdown('### No Data')

# with col[1]:
if nationality_filter == default_option:
    st.markdown('### Nationality')
    nationality_distribution = filtered_data['Nationality'].value_counts().reset_index()
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
    
    

# with col[2]:
if len(filtered_data):
    st.markdown('### Pre-IAEA Work Experience')

    # Calculate work experience background distribution
    experience_distribution = filtered_data['Pre-IAEA Work Experience'].value_counts()

    # Plot bar chart
    fig = px.bar(experience_distribution, x=experience_distribution.index, y=experience_distribution.values)
    fig.update_layout(xaxis_title="Experience", yaxis_title="Number of Staff")
    st.plotly_chart(fig, use_container_width=True)
    
with st.expander('About', expanded=True):
    st.write('''
        - Data: [Department of Safeguards]().
        - :orange[**Diversity**]: staff are from varied backgrounds, education, career paths, and ages
        ''')
