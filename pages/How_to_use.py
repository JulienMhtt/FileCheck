import streamlit as st

st.title("How to use")

st.write("### **Steps**")
st.markdown("""
            1. Select you file type.
            2. If your file type is **xlsx**, add the sheet name, by default, the first file sheet is used.
            3. Use the "Browse file" tool to select **one or more files**. \n
            /!\ For now, only csv file with comma separted values are supported /!\ \n 
            4. You can now analyse the quality of your file(s)         
            """)
st.write("\n")


st.write("### **How to understand the results**")
tab1, tab2, tab3 = st.tabs(["Overview", "Stats", "Graph view"])

with tab1:

    st.markdown("""
                - **Shape** \n
                The number of columns and rows. \n
                ---
                - **Columns name** \n
                The name of the columns. (Thanks for this precious description)\n
                ---
                - **File sample** \n
                A sample of 10 rows.\n
                ---
                - **Duplicated rows** \n
                A list of your duplicated values, you can download this list as a csv file.\n
    """)

with tab2:
    st.markdown("""
                - **Type** \n
                Column type using "infer_dtype()" that deduce column types as csv file don't store column types.\n
                ---
                - **Nb_missing_values** \n
                The number of missing values.\n
                ---
                - **Nb_unique_values** \n
                The number of unique values.\n
                ---
                - **Can_be_unique_key** \n
                If Nb_unique_values is egal to the the lenght of the file, then a column might be considered as a unique key.\n
                ---
                - **Min** & **Max** \n
                Minimum and maximum value, only for numeric values.\n
                ---
                - **Mean** & **Median** \n
                Mean and median of a serie.\n
                ---
                - **Sample** \n
                Data sample.

    """)

    with tab3:
        st.write("On each graph, you can **zoom in** by selectinning an area and double click to **cancel**.")
        st.write("\n")

        st.markdown("""
                    - **Missing values** \n
                    A graphical representation of the missing values in the file.\n
                    ---
                    - **Correlation between columns** \n
                    Only for numerical values, can show correlation between columns that we won't be able to see without visual representation.\n
                    ---
                    - **Box plot** \n
                    Select one or more columns to visualy analyse and compare min, max, Q1 to Q4, median, lower & upper fence and outliers.\n
                    
        """)
        
        