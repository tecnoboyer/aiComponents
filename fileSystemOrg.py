import os
import pandas as pd
from datetime import datetime

class FileOrganizer:
    def __init__(self, base_directory):
        self.base_directory = base_directory
    
    def organize_file(self, file_path):
        # Generate today's date as a subdirectory name
        today_date = datetime.now().strftime('%Y-%m-%d')
        new_directory = os.path.join(self.base_directory, today_date, 'newDirect_named')
        os.makedirs(new_directory, exist_ok=True)  # Create directory if it doesn't exist
        
        # Define the new file path
        new_file_path = os.path.join(new_directory, 'newFile_named.csv')
        
        # Move the file to the new directory
        os.rename(file_path, new_file_path)
        print(f"File moved to {new_file_path}")

# Define the directory and file name
directory = os.getcwd()
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
file_name = f'output_{timestamp}.csv'
file_path = os.path.join(directory, file_name)

# Load the CSV file
df = pd.read_csv(file_path)

description_column = df.columns[1]  # Second column

grouped_df = df.groupby(description_column).size().reset_index(name='Count')

grouped_df.to_csv(file_path, index=False)
print(f"Data saved to {file_path}")

# Organize the file
organizer = FileOrganizer(directory)
organizer.organize_file(file_path)
