import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from filecheck import FileCheck

st.set_page_config(layout="wide")

st.title("File check app")

# Sidebar
st.sidebar.title("Upload your file(s)")

# File type selection
## User input file type
file_type_options = ["csv", "tsv", "xlsx"]
selected_type = st.sidebar.radio("Choose a file type", options=file_type_options)

# Sheet management Excel
xlsx_sheet=0
xlsx_skiprows=None
if selected_type == "xlsx":
    ## User input sheet name
    xlsx_sheet_input = st.sidebar.text_input("Sheet name (optional)")
    if xlsx_sheet_input:
        xlsx_sheet = xlsx_sheet_input
    else:
        xlsx_sheet = 0

    ## User input skiprow
    xlsx_skiprows_input = st.sidebar.text_input("How many rows to skip ? (optional)")
    if xlsx_skiprows_input:
        try:
            xlsx_skiprows = int(xlsx_skiprows_input)
        except ValueError:
            st.sidebar.error("Please enter a valid number for rows to skip.")
    else:
        xlsx_skiprows = None

# File Uploader
uploaded_files = st.sidebar.file_uploader("upload_file", type=selected_type, accept_multiple_files=True, label_visibility='hidden')



if uploaded_files:
    file_names = [uploaded_file.name for uploaded_file in uploaded_files]
    ## User input navigation between loaded files
    selected_file = st.sidebar.radio("**Select a file to display**", file_names)

    for uploaded_file in uploaded_files:
        if uploaded_file.name == selected_file:
            # Create an instance of Filecheck
            file_check = FileCheck(uploaded_file)



            # Read the file
            try: 
                df = file_check.file_read(sheet_name=xlsx_sheet, skiprows=xlsx_skiprows)
                st.write(f"The file **{uploaded_file.name}** is completely loaded")
                st.write(" \n")
            except ValueError:
                if selected_type == "xlsx":
                    st.error("This sheet DOES NOT exists")
                else :
                    st.error("Error while processing file")
                break
                

            # Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Stats", "Graph view", "Sandbox UK"])


            # TAB 1 OVERVIEW
            with tab1:

                # Display the shape
                shape = file_check.file_shape()
                st.write("### **Shape**")
                st.write(f"This file has {shape[1]} columns and {shape[0]} rows")
                st.write(" \n")



                # Columns name
                columns = file_check.file_columns()
                columns_list = columns.tolist()
                columns_string = ", ".join(columns_list)

                st.write(f"### **Columns name**")
                st.write(columns_string)
                st.write(" \n")
            


                # File sample
                sample = file_check.file_sample()

                st.write("### **File sample**")
                st.dataframe(sample)
                st.write(" \n")



                # File duplicates
                st.write("### **Duplicated rows**")

                ## User input columns duplicates
                selected_columns_duplicates = st.multiselect("**Please select the columns to manage duplicates the way you want**", columns_list, key=f"multiselect_duplicates_{uploaded_file.name}")

                ## Full duplicates
                if not selected_columns_duplicates:
                    duplicates = file_check.file_duplicates()
                    st.write("Full duplicate applied when no selection made.")

                ## Subset duplicates
                else:
                    duplicates = file_check.file_duplicates(selected_columns_duplicates)
                
                if not duplicates.empty:
                    st.write(duplicates)
                else:
                    st.success("There is no duplicated values")

                st.write(" \n")


            # TAB 2 STATS
            with tab2:

                # File stats
                file_stats = file_check.file_stats()

                st.write("### **Here is some stats**")
                st.write(file_stats[["Column_name", "Type", "Nb_missing_values", "Nb_unique_values", "Can_be_unique_key", "Sample"]])
                st.write("")

                st.write("### **Detailed Column Stats**")
    
                def display_column_details(file_stats, df):
                    for index, row in file_stats.iterrows():
                        col_name = row["Column_name"]
                        col_type = row["Type"]
                        nb_missing = row["Nb_missing_values"]
                        percent_missing = row["%_missing_values"]
                        nb_unique = row["Nb_unique_values"]
                        percent_unique = row["%_unique_values"]
                        min_value = row["Min_value"]
                        max_value = row["Max_value"]
                        mean_value = row["Mean"]
                        median_value = row["Median"]
                        min_length = row["Min_length"]
                        max_length = row["Max_length"]
                        sample_values = row["Sample"]

                        st.write(f"#### **{col_name}**")
                        col1, col2, col3 = st.columns([1, 1, 1.5], gap="large")
                        with col1:
                            st.markdown(f"<p style='margin: 0'><b>Type:</b> <span style='float: right;'>{col_type}</span></p>", unsafe_allow_html=True)
                            st.write("")
                            st.markdown(f"<p style='margin: 0'><b>Missing values:</b> <span style='float: right;'>{nb_missing}</span></p>", unsafe_allow_html=True)
                            st.markdown(f"<p style='margin: 0'><b>% Missing values:</b> <span style='float: right;'>{percent_missing:.2f}%</span></p>", unsafe_allow_html=True)
                            st.write("")
                            st.markdown(f"<p style='margin: 0'><b>Unique values:</b> <span style='float: right;'>{nb_unique}</span></p>", unsafe_allow_html=True)
                            st.markdown(f"<p style='margin: 0'><b>% Unique values:</b> <span style='float: right;'>{percent_unique:.2f}%</span></p>", unsafe_allow_html=True)
                            st.write("")
                            if row["Type"] == "integer":
                                st.markdown(f"<p style='margin: 0'><b>Min value:</b> <span style='float: right;'>{min_value}</span></p>", unsafe_allow_html=True)
                                st.markdown(f"<p style='margin: 0'><b>Max value:</b> <span style='float: right;'>{max_value}</span></p>", unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"<p style='margin: 0'><b>Min length:</b> <span style='float: right;'>{min_length}</span></p>", unsafe_allow_html=True)
                            st.markdown(f"<p style='margin: 0'><b>Max length:</b> <span style='float: right;'>{max_length}</span></p>", unsafe_allow_html=True)
                            st.write("")
                            if row["Type"] == "integer":
                                st.markdown(f"<p style='margin: 0'><b>Mean:</b> <span style='float: right;'>{mean_value}</span></p>", unsafe_allow_html=True)
                                st.markdown(f"<p style='margin: 0'><b>Median:</b> <span style='float: right;'>{median_value}</span></p>", unsafe_allow_html=True)
                                st.write("")
                                st.markdown(f"<p style='margin: 0'><b>Sample values:</b> <span style='float: right;'>{sample_values}</span></p>", unsafe_allow_html=True)
                        with col3:
                            if row["Type"] == "string":
                                text = " ".join(df[col_name].dropna().astype(str))
                                try:
                                    wordcloud = WordCloud(width=200, height=100).generate(text)
                                    plt.figure(figsize=(10, 5))
                                    plt.imshow(wordcloud, interpolation='bilinear')
                                    plt.axis('off')
                                    st.pyplot(plt)
                                except ValueError:
                                    st.error(f"{col_name} CANNOT get word cloud")

                            if row["Type"] == "integer":
                                fig_histo_stats_integer = file_check.count_stats_integer(col_name)
                                st.plotly_chart(fig_histo_stats_integer)
                        st.markdown("<hr>", unsafe_allow_html=True)

                # Display detailed column stats
                display_column_details(file_stats, df)



            # TAB 3 GRAPHS
            with tab3:

                # Missing value graph
                missing_value_graph = file_check.graph_missing()

                st.write("### **Missing Values by Column**")
                st.plotly_chart(missing_value_graph)
                st.write(" \n")


                # Correlation graph
                correlation_graph = file_check.graph_correlation()

                st.write("### **Correlation between columns**")
                st.plotly_chart(correlation_graph)
                st.write(" \n")


                # Box plot
                st.write("### **Box plot**")

                ## User input box plot columns selection
                numeric_columns = df.select_dtypes(include='number').columns.tolist()
                selected_columns = st.multiselect("**Please select columns to include in the box plot**", numeric_columns, key=f"multiselect_boxplot{uploaded_file.name}")

                if selected_columns:
                    box_plot_graph = file_check.graph_box_plot(selected_columns)

                    st.plotly_chart(box_plot_graph)
                
                st.write(" \n")

            # TAB 4 SANDBOX UNIQUE KEY
            with tab4:
                st.write("### **Unique Key Test**")

                ## User input sandbox unique key column selection
                selected_columns_uk = None
                selected_columns_uk_input = st.multiselect("**Select column to check the unicity of the combinaison**", columns_list, key=f"multiselect_uk_{uploaded_file.name}")

                if selected_columns_uk_input:
                    uk_or_not = file_check.sandbox_uk(selected_columns_uk_input)
                    if uk_or_not:
                        st.success("This combination creates a Unique Key")
                    else:
                        st.error("This combination **DOES NOT** create a Unique Key")


else :
    st.sidebar.write("**Please upload your file(s).**")

    st.markdown("""
                
### **Hi there,**
This tool had been created to help you check the quality of your files.
\n
To understand how it works,
- pleaser reach the page **"How to use"**
                             
To get the last information like the last updates and future features, 
- reach the page **"News"**
                            
If you find any errors or think about a feature, 
- reach the page **"Contact"**
""")
