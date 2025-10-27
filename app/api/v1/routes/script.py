# File Location: Job Tracker/app/api/v1/routes/script.py
import os

# Get the absolute path of the current script's directory
curr_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the top-level directory of your project (this part won't be visible)
top_dir = "/Users/rahulbharti/Desktop/Backend_project"

# Print the current directory of the script
print(f"Current script directory: {curr_dir}")

# Loop through all files in the current directory
for file_name in os.listdir(curr_dir):
    # Check if the file is a Python file
    if file_name.endswith(".py"):
        # Get the full path of the file
        full_file_path = os.path.join(curr_dir, file_name)
        
        # Calculate the relative file path from top_dir
        relative_file_path = os.path.relpath(full_file_path, top_dir)

        with open(full_file_path, "r+") as f:
            lines = f.readlines()  # Read all lines of the file
            
            # Check if the file already has a location comment at the top
            if len(lines)==0 or not lines[0].startswith("# File Location:"):
                # Insert the location comment at the very beginning (relative path from top_dir)
                lines.insert(0, f"# File Location: {relative_file_path}\n")

                # Move the file pointer back to the beginning
                f.seek(0)

                # Write the modified lines back into the file
                f.writelines(lines)

print("File locations added to Python files in the directory.")
