import pandas as pd
import plotly.express as px

class FileCheck:
    """
    A class for performing various checks and visualizations on a file (CSV, TSV, XLSX).

    -------
    Methods
    -------
    file_read(sheet_name=0, skiprows=None):
        Reads the file into a DataFrame.
    file_shape():
        Returns the shape of the DataFrame.
    file_columns():
        Returns the columns of the DataFrame.
    file_sample():
        Returns a sample of the DataFrame.
    file_duplicates(column=None):
        Returns duplicated rows in the DataFrame.
    file_stats():
        Returns statistics about the DataFrame columns.
    graph_missing():
        Returns a bar chart of missing values as a percentage.
    graph_correlation():
        Returns a heatmap of the correlation between numeric columns.
    graph_box_plot(columns):
        Returns a box plot of the specified columns.
    sandbox_uk(column_list):
        Checks if the combination of specified columns is unique.
    """

    def __init__(self, file):
      """
      Initializes the FileCheck class with the provided file.
      
      Parameters
      ----------
      file : file-like object
          The file to be analyzed.
      """

      self.file = file



    def file_read(self, sheet_name=0, skiprows=None):
        """
        Reads the file into a DataFrame based on the file extension.
        
        Parameters
        ----------
        sheet_name : str or int, optional
            The sheet name or index to read from if the file is an Excel file. Default is 0.
        skiprows : int, optional
            The number of rows to skip at the start of the file. Default is None.
        
        Returns
        -------
        pd.DataFrame
            The DataFrame created from the file.
        """

        if self.file.name.endswith('.csv'):
            self.df = pd.read_csv(self.file)
        elif self.file.name.endswith('.tsv'):
            self.df = pd.read_csv(self.file, sep='\t')
        elif self.file.name.endswith('.xlsx'):
            self.df = pd.read_excel(self.file, sheet_name=sheet_name, skiprows=skiprows)
            if self.df is dict:
              self.df = pd.DataFrame.from_dict(self.df)
        return self.df



    def file_shape(self):
      """
      Returns the shape of the DataFrame.
      
      Returns
      -------
      tuple
          The shape of the DataFrame (number of rows, number of columns).
      """

      self.shape = self.df.shape
      return self.shape



    def file_columns(self):
      """
      Returns the columns of the DataFrame.
      
      Returns
      -------
      pd.Index
          The columns of the DataFrame.
      """

      self.columns = self.df.columns
      return self.columns



    def file_sample(self):
      """
      Returns a sample of the DataFrame.
      
      Returns
      -------
      pd.DataFrame
          A sample of the DataFrame.
      """

      self.sample = self.df.sample(n=min(10, len(self.df)))
      return self.sample
    


    def file_duplicates(self, column=None):
      """
      Returns duplicated rows in the DataFrame.
      
      Parameters
      ----------
      column : list of str, optional
          The column to check for duplicates. If None, checks all columns. Default is None.
      
      Returns
      -------
      pd.DataFrame
          Duplicated rows in the DataFrame.
      """

      if column:
        self.duplicates = self.df[self.df.duplicated(keep=False, subset=column)]
      else:
         self.duplicates = self.df[self.df.duplicated(keep=False)]
      return self.duplicates



    def file_stats(self):
      """
      Returns statistics about the DataFrame columns.
      
      Returns
      -------
      pd.DataFrame
          A DataFrame with statistics about the columns, including type, number of missing values,
          number & percentage of unique values, whether the column can be a unique key, the minimum & maximum values, the mean & median,
          the minimum and maximum lenght and a data sample.
      """

      df_file_stats = pd.DataFrame(self.columns, columns=["Column_name"])

      # Types
      df_file_stats["Type"] = df_file_stats["Column_name"].apply(lambda col: pd.api.types.infer_dtype(self.df[col]))

      # Nb & % of missing values
      df_file_stats["Nb_missing_values"] = df_file_stats["Column_name"].apply(lambda col: self.df[col].isnull().sum())
      df_file_stats["%_missing_values"] = (df_file_stats["Column_name"].apply(lambda col: self.df[col].isnull().sum())/self.shape[0]) * 100

      # Nb & % of unique values
      df_file_stats["Nb_unique_values"] = df_file_stats["Column_name"].apply(lambda col: self.df[col].nunique())
      df_file_stats["%_unique_values"] = (df_file_stats["Column_name"].apply(lambda col: self.df[col].nunique())/self.shape[0]) * 100

      # Can be unique key
      df_file_stats["Can_be_unique_key"] = df_file_stats["Nb_unique_values"] == self.df.shape[0]

      # Stats
      df_file_stats["Min_value"] = df_file_stats["Column_name"].apply(lambda col: self.df[col].dropna().min() if pd.api.types.is_numeric_dtype(self.df[col]) else None)
      df_file_stats["Max_value"] = df_file_stats["Column_name"].apply(lambda col: self.df[col].dropna().max() if pd.api.types.is_numeric_dtype(self.df[col]) else None)
      df_file_stats["Mean"] = df_file_stats["Column_name"].apply(lambda col: self.df[col].dropna().mean() if pd.api.types.is_numeric_dtype(self.df[col]) else None)
      df_file_stats["Median"] = df_file_stats["Column_name"].apply(lambda col: self.df[col].dropna().mean() if pd.api.types.is_numeric_dtype(self.df[col]) else None)

      # Length of values
      df_file_stats["Min_length"] = df_file_stats["Column_name"].apply(lambda col: self.df[col].dropna().apply(lambda x: len(str(x))).min())
      df_file_stats["Max_length"] = df_file_stats["Column_name"].apply(lambda col: self.df[col].dropna().apply(lambda x: len(str(x))).max())

      # Sample
      df_file_stats["Sample"] = df_file_stats["Column_name"].apply(lambda col: ', '.join(map(str, self.df[col].sample(n=min(5, self.df[col].count())).tolist())) if not self.df[col].empty else '')

      self.file_stats = df_file_stats

      return self.file_stats




    def graph_missing(self):
      """
      Returns a bar chart of missing values as a percentage.
      
      Returns
      -------
      plotly.graph_objs._figure.Figure
          A bar chart showing the percentage of missing values for each column.
      """

      df_percent_missing_value = pd.DataFrame(self.file_stats[["Column_name", "Nb_missing_values"]])
      df_percent_missing_value["Percent_missing_values"] = (df_percent_missing_value["Nb_missing_values"]/self.shape[0]) * 100

      fig = px.bar(df_percent_missing_value, y='Column_name', x='Percent_missing_values')
      fig.update_xaxes(range=[0, 100], title_text="Percentage of missing values (%)")
      fig.update_yaxes(title_text="Column name")

      return fig
    


    def graph_correlation(self):
      """
      Returns a heatmap of the correlation between numeric columns.
      
      Returns
      -------
      plotly.graph_objs._figure.Figure
          A heatmap showing the correlation between numeric columns.
      """

      numeric_df = self.df.select_dtypes(include='number')
      correlation_matrix = numeric_df.corr()
      
      fig = px.imshow(correlation_matrix, color_continuous_scale='Reds')

      return fig



    def graph_box_plot(self, columns):
        """
        Returns a box plot of the specified columns.
        
        Parameters
        ----------
        columns : list of str
            The columns to be included in the box plot.
        
        Returns
        -------
        plotly.graph_objs._figure.Figure
            A box plot of the specified columns.
        """

        fig = px.box(self.df, y=columns)
        return fig
    


    def count_stats_integer(self, int_column):
      """
      Returns a bar chart of integer values in stats section.
      
      Returns
      -------
      plotly.graph_objs._figure.Figure
          A bar chart showing the effective of interger values.
      """

      count_values = self.df[int_column].value_counts().reset_index()
      count_values.columns = [int_column, "Count"]
      
      fig = px.bar(count_values, x=int_column, y="Count")
      fig.update_layout(width=600, height=300)
      return fig

 
    def sandbox_uk(self, column_list):
        """
        Checks if the combination of specified columns is unique.

        Parameters
        ----------
        column_list : list of str
            The columns to be checked for uniqueness.

        Returns
        -------
        bool
            True if the combination of columns is unique, False otherwise.
        """

        df_uk = pd.DataFrame()
        df_uk["combined_uk"] = self.df[column_list].astype(str).agg('_'.join, axis=1)

        unique_combined_uk_count = df_uk["combined_uk"].nunique()

        if unique_combined_uk_count == self.shape[0]:
          return True
        else:
          return False
          
    
