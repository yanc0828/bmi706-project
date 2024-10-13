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
    st.write(df.head())  # Display the first few rows
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
        st.write("No data available for the selected drug or year range")
    else:
        if drug == "Alcohol":

            subset = subset[subset['Use'] < 366]

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
                y=alt.Y("count(Use)", title="Frequency"),
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

def task2():
    st.write("## Demographic Patterns")
    # add chart

def task3():
    st.write("## Mortality Patterns")
    # add chart

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

