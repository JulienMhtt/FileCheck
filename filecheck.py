import pandas as pd
import plotly.express as px

# Create a class that will read a csv file, return the shape, the columns name,
class FileCheck:

    # Initialize the class
    def __init__(self, file):
      self.file = file



    # Read the csv file
    def file_read(self):
      df = pd.read_csv(self.file)
      self.df = df
      return self.df



    # Returns the file shape
    def file_shape(self):
      self.shape = self.df.shape
      return self.shape



    # Returns the file columns
    def file_columns(self):
      self.columns = self.df.columns
      return self.columns



    # Returns a sample of the file
    def file_sample(self):
      self.sample = self.df.sample(n=min(10, len(self.df)))
      return self.sample
    


    # Returns informations about duplicated values
    def file_duplicates(self):
      self.duplicates = self.df[self.df.duplicated(keep=False)]
      return self.duplicates


    # Return informations about the columns
    def file_stats(self):
      df_file_stats = pd.DataFrame(self.columns, columns=["Column_name"])

      # Types
      df_file_stats["Type"] = df_file_stats["Column_name"].apply(lambda col: pd.api.types.infer_dtype(self.df[col]))

      # Nb of missing values
      df_file_stats["Nb_missing_values"] = df_file_stats["Column_name"].apply(lambda col: self.df[col].isnull().sum())

      # Nb of unique values
      df_file_stats["Nb_unique_values"] = df_file_stats["Column_name"].apply(lambda col: self.df[col].nunique())

      # Can be unique key
      df_file_stats["Can_be_unique_key"] = df_file_stats["Nb_unique_values"] == self.df.shape[0]

      # Stats
      df_file_stats["Min"] = df_file_stats["Column_name"].apply(lambda col: self.df[col].min() if pd.api.types.is_numeric_dtype(self.df[col]) else None)
      df_file_stats["Max"] = df_file_stats["Column_name"].apply(lambda col: self.df[col].max() if pd.api.types.is_numeric_dtype(self.df[col]) else None)
      df_file_stats["Mean"] = df_file_stats["Column_name"].apply(lambda col: self.df[col].mean() if pd.api.types.is_numeric_dtype(self.df[col]) else None)
      df_file_stats["Median"] = df_file_stats["Column_name"].apply(lambda col: self.df[col].mean() if pd.api.types.is_numeric_dtype(self.df[col]) else None)

      # Sample
      df_file_stats["Sample"] = df_file_stats["Column_name"].apply(lambda col: ', '.join(map(str, self.df[col].sample(n=min(5, self.df[col].count())).tolist())) if not self.df[col].empty else '')

      self.file_stats = df_file_stats

      return self.file_stats
 
    # Return a missing value graph
    def graph_missing(self):
      fig = px.bar(self.file_stats, y='Column_name', x='Nb_missing_values')

      return fig
    

    # Correlation between columns
    def graph_correlation(self):
      numeric_df = self.df.select_dtypes(include='number')
      correlation_matrix = numeric_df.corr()
      
      fig = px.imshow(correlation_matrix)

      return fig


    # Box plot
    def graph_box_plot(self, columns):
        fig = px.box(self.df, y=columns)
        return fig
    
