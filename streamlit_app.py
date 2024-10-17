import altair as alt
import pandas as pd
import streamlit as st

# load data

@st.cache
def load_data():
    df = pd.read_csv("nhanes_data_new.csv")
    return df

df = load_data()

# tasks

def main_page():
    st.write("## Dataset Preview")
    st.write(df.head())  # display the first few rows
    st.write("## About NHANES")
    st.write("The National Health and Nutrition Examination Survey (NHANES) is a program of studies designed to assess the health and nutritional status of adults and children in the United States. The survey is unique in that it combines interviews and physical examinations. NHANES is a major program of the National Center for Health Statistics (NCHS). NCHS is part of the Centers for Disease Control and Prevention (CDC) and has the responsibility for producing vital and health statistics for the Nation.")
    st.write("The NHANES program began in the early 1960s and has been conducted as a series of surveys focusing on different population groups or health topics. In 1999, the survey became a continuous program that has a changing focus on a variety of health and nutrition measurements to meet emerging needs. The survey examines a nationally representative sample of about 5,000 persons each year. These persons are located in counties across the country, 15 of which are visited each year.")
    st.write("The NHANES interview includes demographic, socioeconomic, dietary, and health-related questions. The examination component consists of medical, dental, and physiological measurements, as well as laboratory tests administered by highly trained medical personnel.")
    st.write("Findings from this survey will be used to determine the prevalence of major diseases and risk factors for diseases. Information will be used to assess nutritional status and its association with health promotion and disease prevention. NHANES findings are also the basis for national standards for such measurements as height, weight, and blood pressure. Data from this survey will be used in epidemiological studies and health sciences research, which help develop sound public health policy, direct and design health programs and services, and expand the health knowledge for the Nation.")
    st.write("NHANES website: https://www.cdc.gov/nchs/nhanes/about_nhanes.htm")

def task1():

    st.write("## Temporal Patterns")

    year = st.slider(
        "Year", min_value=1999, max_value=2018, value=[2003, 2015])
    subset = df[(df['Year'] >= year[0]) & (df['Year'] <= year[1])]

    drugs = ['Alcohol', 'Marijuana or hashish', 'Cocaine', 'Heroin', 'Methamphetamine', 'Injection of illegal drug']
    drug = st.selectbox("Select a Substance", drugs, index=1)
    subset = subset[["ID", "Year", drug]]
    cols = ["ID", "Year", "Use"]
    subset.columns = cols
    subset = subset[subset['Use'] != "Don't know"]

    if subset.empty:
        st.write("No data available for selected year range")
    else:
        if drug == "Alcohol":

            subset = subset[subset['Use'] <= 366]
            subset = subset[subset['Use'] > 0]

            year_selection = alt.selection_single(
                fields=['Year']
            )

            chart = alt.Chart(subset).mark_line(point=True).encode(
                x=alt.X("Year:N"),
                y=alt.Y("count(Use)", title="Frequency"),
                tooltip=["Year", "count(Use)"],
            ).properties(
                title=f"Alcohol usage from {year[0]} to {year[1]}",
            ).add_selection(
                year_selection
            )

            chart2 = alt.Chart(subset).mark_bar().encode(
                x=alt.X("Use:Q", bin=alt.Bin(step=5), title="# days have 4/5 drinks in past 12 months"),
                y=alt.Y("count(Use)", title="Frequency in selected year"),
                tooltip=["Use:Q", "count(Use)"],
            ).transform_filter(
                year_selection
            )

            final_chart = alt.vconcat(chart, chart2)
            st.altair_chart(final_chart, use_container_width=True)

        else:
            subset_users = subset[subset['Use'] == "Yes"]
            chart = alt.Chart(subset_users).mark_line(point=True).encode(
                x=alt.X("Year:N"),
                y=alt.Y("count(Use)", title="Frequency"),
                color = alt.Color("Use:N"),
                tooltip=["Year", "count(Use)"],
            ).properties(
                title=f"{drug} usage from {year[0]} to {year[1]}",
            )

            st.altair_chart(chart, use_container_width=True)

            if drug != "Injection of illegal drug" and year[0] < 2005:
                st.write(f"No data from {year[0]} to 2005")

def task2():
    st.write("## Demographic Patterns")
    # add chart
    substances = ["Alcohol", "Marijuana or hashish", "Cocaine", "Heroin", "Methamphetamine", "Injection of illegal drug"]
    demographics = ["ID", "Gender", "Age", "Race", "Income", "Education"]
    selected_substance = st.selectbox("Select a Substance", substances)
    subset = df[[selected_substance] + demographics]
    if selected_substance == "Alcohol":
        subset = subset[(subset["Alcohol"] > 0.0) & (subset["Alcohol"]<= 366.0)]
    else:
        subset = subset[subset[selected_substance]=="Yes"]

    if subset.empty:
      st.write("No data available for the selected substance usage")
    else:
        age_chart = alt.Chart(subset).mark_bar().encode(
            x=alt.X("Age:Q", bin=True),
            y=alt.Y('count(ID)', title="Frequency"),
            tooltip=["Age", "count(ID)"]
        ).properties(
            title=f"{selected_substance} users' age distribution",
            height=300,
            width=400
        )

        known_income = subset.dropna(subset=["Income"])
        income_chart = alt.Chart(known_income).mark_bar().encode(
            x=alt.X("Income:Q", bin=True),
            y=alt.Y('count(ID)', title="Frequency"),
            tooltip=["Income", "count(ID)"]
        ).properties(
            title=f"{selected_substance} users' income ratio to poverty distribution",
            height=300,
            width=400
        )
        bar_charts = alt.hconcat(age_chart, income_chart)
        st.altair_chart(bar_charts, use_container_width=True)

        gender_chart = alt.Chart(subset).mark_arc().encode(
            theta = "count(ID)",
            color = "Gender",
            tooltip=["Gender", "count(ID)"]
        ).properties(
            title=f"{selected_substance} users' gender distribution",
            height=250,
            width=250
        )

        race_chart = alt.Chart(subset).mark_arc().encode(
            theta = "count(ID)",
            color = "Race",
            tooltip=["Race", "count(ID)"]
        ).properties(
            title=f"{selected_substance} users' race distribution",
            height=250,
            width=250
        )
        education_chart = alt.Chart(subset).mark_arc().encode(
            theta = "count(ID)",
            color = "Education",
            tooltip=["Education", "count(ID)"]
        ).properties(
            title=f"{selected_substance} users' education distribution",
            height=250,
            width=250
        )

        pie_charts = alt.hconcat(gender_chart, race_chart, education_chart).resolve_scale(
            color='independent'
            )
        st.altair_chart(pie_charts, use_container_width=True)

def task3():
    st.write("## Mortality Patterns")
    # add chart
    conditions = ["Alcohol", "Marijuana or hashish", "Cocaine", "Heroin", "Methamphetamine", "Injection of illegal drug"]

    selected_conditions = st.multiselect("Substances", conditions, default = conditions) # multi-select widge
    subset = df[["Mortality"] + selected_conditions]

    df_grouped = subset.melt(id_vars='Mortality', value_vars=selected_conditions, var_name='Substance', value_name='Usage')
    df_grouped = df_grouped[df_grouped['Usage'].isin(['Yes', 'No'])]  # Remove data when Usage = "Don't Know" or "Refused"

    if df_grouped.empty:
      st.write("No data available for the selected substance usage")
    else:
      
      alt.data_transformers.enable(max_rows=210000)
      
      # Create an altair selector
      legend_selection = alt.selection_single(
          fields=['Mortality'],
          bind='legend',
          name="Mortality"
      )
      
      # Create a grouped bar plot using Altair
      chart = alt.Chart(df_grouped).mark_bar(size=30).encode(
          x=alt.X('Usage:N', title='Substance Usage'),
          y=alt.Y('count():Q', title='Number of respondents'),
          color='Mortality:N',
          column=alt.Column('Substance:N', title='Substance'),
          opacity=alt.condition(
              legend_selection,  # If the cancer type is selected
              alt.value(1),      # Full opacity for selected cancer
              alt.value(0.3)     # Lighter opacity (0.3) for unselected cancer types
              )
          ).add_selection(
              legend_selection
          ).properties(
              width=120
          )
      
      chart


def task4():
    st.write("## Health Patterns")
    # add chart
    substances = ["Alcohol", "Marijuana or hashish", "Cocaine", "Heroin", "Methamphetamine", "Injection of illegal drug"]
    health_conditions = ["Cancer or malignancy", "Congestive heart failure", "Coronary heart disease", "Angina/angina pectoris", "Heart attack"]
    
    # Create a dropdown for users to select a health condition
    selected_disease = st.selectbox("Select a Health Condition", health_conditions)

    subset = df[health_conditions + substances]
    subset.loc[subset['Alcohol'] <=366.0, 'Alcohol'] = "Yes"
    subset.loc[subset['Alcohol'] == 0.0, 'Alcohol'] = "No"
    subset.loc[subset['Alcohol'] == 999.0, 'Alcohol'] = "Don't know"
    subset.loc[subset['Alcohol'] == 777.0, 'Alcohol'] = "Don't know"

    df_grouped = subset.melt(id_vars=[selected_disease], value_vars=substances, var_name="Substance", value_name="Usage")
    df_grouped = df_grouped[df_grouped['Usage'].isin(['Yes', 'No'])]

    alt.data_transformers.enable(max_rows=1000000)

    # Create an altair selector
    legend_selection = alt.selection_single(
        fields=[df_grouped.columns[0]],
        bind='legend',
        name=df_grouped.columns[0]
      )

    # Create a grouped bar plot using Altair
    chart = alt.Chart(df_grouped).mark_bar(size=30).encode(
        x=alt.X('Usage:N', title='Substance Usage'),
        y=alt.Y('count():Q', title='Number of respondents'),
        color=alt.Color(f'{selected_disease}:N', title="Health Condition"),
        column=alt.Column('Substance:N', title='Substance'),
        opacity=alt.condition(
            legend_selection, 
            alt.value(1),      
            alt.value(0.3)     
            )
        ).add_selection(
            legend_selection
        ).properties(
            width=120
        )

    chart


# main page

st.title("NHANES Drug & Alcohol Explorer")

task = st.selectbox(
    "Please select a task", ["-----Please select a task-----", "Task 1: Temporal data", "Task 2: Demographic data", "Task 3: Mortality data", "Task 4: Health data"], 
    index=0
)

if task == "-----Please select a task-----":
    main_page()
elif task == "Task 1: Temporal data":
    task1()
elif task == "Task 2: Demographic data":
    task2()
elif task == "Task 3: Mortality data":
    task3()
elif task == "Task 4: Health data":
    task4()
