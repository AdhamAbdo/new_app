import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the data
file_path = r'C:\Users\Adham\Desktop\Ceos\New folder (2)\CEOs - data .xlsx'  # Ensure the file path is correct
data = pd.read_excel(file_path)

# Function to calculate the percentage chance of becoming a CEO
def calculate_ceo_chance(user_data, dataset):
    total_ceos = len(dataset)
    match_ceos = len(dataset[(dataset['التخصص'] == user_data['التخصص']) & 
                             (dataset['الجامعة'] == user_data['الجامعة']) & 
                             (dataset['دولة التخرج'] == user_data['دولة التخرج']) & 
                             (dataset['آخر مؤهل'] == user_data['آخر مؤهل'])])
    chance = (match_ceos / total_ceos) * 100
    return chance

# Streamlit app
st.title("CEO Predictor")

st.write("Enter your details to see your chances of becoming a CEO in the future and get insights about people like you.")

# User inputs
user_data = {}
user_data['الرئيس التنفيذي'] = st.text_input("Your Name")
user_data['التخصص'] = st.selectbox("Major", options=data['التخصص'].unique())
user_data['الجامعة'] = st.selectbox("University", options=data['الجامعة'].unique())
user_data['دولة التخرج'] = st.selectbox("Graduation Country", options=data['دولة التخرج'].unique())
user_data['آخر مؤهل'] = st.selectbox("Highest Qualification", options=data['آخر مؤهل'].unique())
user_data['السنوات قبل التعيين'] = st.slider("Years Before Appointment", min_value=int(data['السنوات قبل التعيين'].min()), max_value=int(data['السنوات قبل التعيين'].max()), value=int(data['السنوات قبل التعيين'].mean()))
user_data['السنوات قبل التعيين في نفس الجهة'] = st.slider("Years Before Appointment in the Same Entity", min_value=int(data['السنوات قبل التعيين في نفس الجهة'].min()), max_value=int(data['السنوات قبل التعيين في نفس الجهة'].max()), value=int(data['السنوات قبل التعيين في نفس الجهة'].mean()))

# Calculate chance
chance = calculate_ceo_chance(user_data, data)

# Show the results in a donut chart
fig = go.Figure(data=[go.Pie(labels=['Chance to be CEO', 'Others'], values=[chance, 100 - chance], hole=.4)])
fig.update_traces(marker=dict(colors=['#2E91E5', '#E5ECF6']))
fig.update_layout(title_text='Chance to be a CEO in the Future')
st.plotly_chart(fig)

# Provide insights in cards
total_ceos = len(data)
field_match = len(data[data['التخصص'] == user_data['التخصص']])
country_match = len(data[data['دولة التخرج'] == user_data['دولة التخرج']])

st.write("### Insights")
st.markdown(f"""
<div style="display: flex;">
    <div style="flex: 1; padding: 10px; margin: 10px; border: 1px solid #ddd; border-radius: 5px;">
        <h3>Education Field</h3>
        <p>{field_match / total_ceos * 100:.2f}% of people have the same education field as you ({user_data['التخصص']}).</p>
    </div>
    <div style="flex: 1; padding: 10px; margin: 10px; border: 1px solid #ddd; border-radius: 5px;">
        <h3>Graduation Country</h3>
        <p>{country_match / total_ceos * 100:.2f}% of CEOs are from {user_data['دولة التخرج']}.</p>
    </div>
</div>
""", unsafe_allow_html=True)
