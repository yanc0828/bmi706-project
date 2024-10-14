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
    st.write("The National Health and Nutrition Examination Survey (NHANES) dataset is a large, publicly available dataset that contains detailed health and nutrition information collected from a representative sample of the U.S. population.")

def task1():

    st.write("## Temporal Patterns")

    year = st.slider(
        "Year", min_value=1999, max_value=2018, value=2015)
    subset = df[df["Year"] <= year]

    drugs = ['Alcohol', 'Marijuana or hashish', 'Cocaine', 'Heroin', 'Methamphetamine', 'Injection of illegal drug']
    drug = st.selectbox("Select drug", drugs, index=1)
    subset = subset[["ID", "Year", drug]]
    cols = ["ID", "Year", "Use"]
    subset.columns = cols
    subset = subset[subset['Use'] != "Don't know"]

    if subset.empty:
        st.write("No data available for selected year range")
    else:
        if drug == "Alcohol":

            subset = subset[subset['Use'] < 366]
            subset = subset[subset['Use'] > 0]

            year_selection = alt.selection_single(
                fields=['Year']
            )

            chart = alt.Chart(subset).mark_line(point=True).encode(
                x=alt.X("Year:N"),
                y=alt.Y("count(Use)", title="Frequency"),
                tooltip=["Year", "count(Use)"],
            ).properties(
                title=f"Alcohol usage from 1999 to {year}",
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
            chart = alt.Chart(subset).mark_line(point=True).encode(
                x=alt.X("Year:N"),
                y=alt.Y("count(Use)", title="Frequency"),
                color = alt.Color("Use:N"),
                tooltip=["Year", "count(Use)"],
            ).properties(
                title=f"{drug} usage from 1999 to {year}",
            )

            st.altair_chart(chart, use_container_width=True)

            if drug != "Injection of illegal drug":
                st.write("No data from 1999 to 2005")

def task2():
    st.write("## Demographic Patterns")
    # add chart

def task3():
    st.write("## Mortality Patterns")
    # add chart
    conditions = ["Alcohol", "Marijuana or hashish", "Cocaine", "Heroin", "Methamphetamine", "Injection of illegal drug"]

    selected_conditions = st.multiselect("Conditions", conditions, default = conditions) # multi-select widge
    subset = df[["Mortality"] + selected_conditions]

    df_grouped = subset.melt(id_vars='Mortality', value_vars=selected_conditions, var_name='Substance', value_name='Usage')
    df_grouped = df_grouped[df_grouped['Usage'].isin(['Yes', 'No'])]  # Remove data when Usage = "Don't Know" or "Refused"

    if df_grouped.empty:
      st.write("No data available for the selected condition")
    else:
      
      alt.data_transformers.enable(max_rows=210000)
      
      # Create an altair selector
      legend_selection = alt.selection_single(
          fields=['Mortality'],
          bind='legend',
          name="Mortality"
      )
      
      # Create a grouped bar plot using Altair
      chart = alt.Chart(df_grouped).mark_bar().encode(
          x=alt.X('Usage:N', title='Substance Usage'),
          y=alt.Y('count():Q', title='Number of respondents'),
          color='Mortality:N',
          column=alt.Column('Substance:N', title='Substance', spacing=5),
          opacity=alt.condition(
              legend_selection,  # If the cancer type is selected
              alt.value(1),      # Full opacity for selected cancer
              alt.value(0.3)     # Lighter opacity (0.3) for unselected cancer types
              )
          ).add_selection(
              legend_selection
              ).properties(
                  width=90,  
                  height=300  
                  ).configure_bar(
                      size=20  # Adjust the size of individual bars (smaller value means thinner bars)
                      ).configure_facet(
                          spacing=5  # Adjust the spacing between columns (grouped bar spacing)
                          )
      
      st.altair_chart(chart, use_container_width=True)

def task4():
    st.write("## Health Patterns")
    # add chart


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
