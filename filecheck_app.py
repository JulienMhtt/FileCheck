import streamlit as st
from filecheck import FileCheck

st.title("File check app")

# Sidebar
st.sidebar.title("Upload your file(s)")

# File type selection
file_type_options = ["csv", "tsv", "xlsx", "json", "parquet"]
selected_type = st.sidebar.radio("Choose a file type", options=file_type_options)

# Sheet management Excel
xlsx_sheet=None
if selected_type == "xlsx":
    xlsx_sheet = st.sidebar.text_input("Sheet name (optional)")

# File Uploader
uploaded_files = st.sidebar.file_uploader("upload_file", type=selected_type, accept_multiple_files=True, label_visibility='hidden')



if uploaded_files:

    file_names = [uploaded_file.name for uploaded_file in uploaded_files]
    selected_file = st.sidebar.radio("**Select a file to display**", file_names)

    for uploaded_file in uploaded_files:
        if uploaded_file.name == selected_file:
            # Create an instance of Filecheck
            file_check = FileCheck(uploaded_file)



            # Read the file
            try: 
                df = file_check.file_read(xlsx_sheet)
                st.write(f"The file **{uploaded_file.name}** is completely loaded")
                st.write(" \n")
            except ValueError:
                if selected_type == "xlsx":
                    st.write("Sheet not found")
                else :
                    st.write("Error while processing file")
                break
                

            # Tabs
            tab1, tab2, tab3 = st.tabs(["Overview", "Stats", "Graph view"])


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
                duplicates = file_check.file_duplicates()

                st.write("### **Duplicated rows**")
                if not duplicates.empty:
                    st.write(duplicates)
                else:
                    st.write("There is no duplicated values")

                st.write(" \n")


            # TAB 2 STATS
            with tab2:

                # File stats
                file_stats = file_check.file_stats()

                st.write("### **Here is some stats**")
                st.write(file_stats)
                st.write(" \n")



            # TAB 3 GRAPHS
            with tab3:

                # Missing value graph
                missing_value_graph = file_check.graph_missing()

                st.write("### **Missing values**")
                st.plotly_chart(missing_value_graph)
                st.write(" \n")


                # Correlation graph
                correlation_graph = file_check.graph_correlation()

                st.write("### **Correlation between columns**")
                st.plotly_chart(correlation_graph)
                st.write(" \n")


                # Box plot
                # Tick box selection
                st.write("### **Box plot**")
                numeric_columns = df.select_dtypes(include='number').columns.tolist()
                selected_columns = st.multiselect("**Please select columns to include in the box plot**", numeric_columns, key=f"multiselect_{uploaded_file.name}")

                if selected_columns:
                    box_plot_graph = file_check.graph_box_plot(selected_columns)

                    st.plotly_chart(box_plot_graph)
                

                st.write(" \n")

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

