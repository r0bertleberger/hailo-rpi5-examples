import sys

if len(sys.argv) < 3:
	print("pas assez 'arguments")
else:
	file_path = sys.argv[1]
	stop_string = sys.argv[2]

def remove_lines_after(file_path, stop_string):
    """
    Removes all lines in the file after the specified string (including the line with the string).
    """
    try:
        # Read the file content
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Find the stopping point
        new_lines = []
        for line in lines:
            if stop_string in line:
                break
            new_lines.append(line)
        
        # Write back the modified content
        with open(file_path, 'w') as file:
            file.writelines(new_lines)
        
        print(f"Updated file: {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


remove_lines_after(file_path, stop_string)
