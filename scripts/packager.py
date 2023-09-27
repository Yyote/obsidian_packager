import os
import re
import shutil



# Specify the paths and directories
markdown_file_path = '/your/path/to/file/name' + '.md'
source_directory = '/path/to/your/vault/'
target_directory = '/path/to/destination/'
parsing_depth = 6
















def get_file_type(path):
    valid_file_types = [
        '.md', '.canvas', '.pdf', '.png', '.jpg', '.jpeg',
        '.mp4', '.mp3', '.word', '.xls', '.zip', '.tar',
        '.cpp', '.py', '.cc', '.ipynb', '.nb', '.ggb', '.xml',
        '.launch', '.txt', '.cfg'
    ]

    for i in range(len(valid_file_types)):
        # print(f"File is {valid_file_types[i]} = {valid_file_types[i] in path[-6:]}")
        if valid_file_types[i] in path[-6:]:
            return True, valid_file_types[i]
    return False, None


def format_file_path(file_path):
    # Check if the path is already properly formatted
    formatted_path = file_path.replace(' ', r'\ ')
    if not any(char == '\\' for char in formatted_path):
        return formatted_path
    else:
        return file_path



def extract_filenames_from_markdown(file_path):
    with open(file_path, 'r') as markdown_file:
        
        content = None
        try:
            content = markdown_file.read()
        except: 
            # print(f"\n\n\ncatn decode {file_path}\n\n\n")
            pass
    
    # Define regex patterns to match markdown links
    pattern = r'\[\[([\w\s.-]+?)(?:\|[\w\s.-]+)?\]\]|\!\[\[([\w\s.-]+?)(?:\|[\w\s.-]+)?\]\].(pdf|png|jpg|jpeg|mp4|mp3|word|xls|zip|tar|cpp|py|cc|ipynb|md)'
    
    # pattern = r'(!?)\[\[([+\w\.,\-_()]+)(?:#([+\w\.,\-_()]+))?\]\]'

    
    filenames = []
    if (content != None):
        # Extract filenames from markdown content
        filenames = re.findall(pattern, content)
        filenames = [file[0] or file[1] for file in filenames if file[0] or file[1]]

    return filenames






def concatenate_alias(string):
    previous_symbol = None
    current_symbol = None
    
    link_pos = {
        'alias_pos': []
        }
    
    for i in range(len(string)):
        previous_symbol = current_symbol
        current_symbol = string[i]
        
        if previous_symbol is not None:
            if current_symbol == '|':
                link_pos['alias_pos'].append(i)
    
    if len(link_pos['alias_pos']) > 0:
        string_tmp = string[0:link_pos['alias_pos'][0]]
        return string_tmp
    return string


def parse_filenames_from_markdown(file_path):
    with open(file_path, 'r') as markdown_file:
        
        content = None
        try:
            content = markdown_file.read()
        except: 
            # print(f"\n\n\ncatn decode {file_path}\n\n\n")
            pass
        
        filenames = []
        if (content != None):
            # Extract filenames from markdown content
            previous_symbol = None
            current_symbol = None
            link_started = False
            link_finished = False
            
            link_pos = {
                'start_pos': [],
                'end_pos': []
                }
            
            for i in range(len(content)):
                previous_symbol = current_symbol
                current_symbol = content[i]
                
                
                if (previous_symbol != None):
                    if link_started and previous_symbol == "[" and current_symbol == "[":
                        link_pos['start_pos'][len(link_pos['start_pos']) - 1] = i + 1
                    if not link_started:
                        link_started = previous_symbol == "[" and current_symbol == "["
                        if link_started:
                            link_pos['start_pos'].append(i + 1)
                    if not link_finished:
                        link_finished = link_started and previous_symbol == "]" and current_symbol == "]"
                    if link_finished:
                        link_pos['end_pos'].append(i - 1)
                        link_started = False
                        link_finished = False
                
            print(f"start len: {len(link_pos['start_pos'])}\nend len: {len(link_pos['end_pos'])}")
            for i in range(len(link_pos['start_pos'])):
                filenames.append(content[link_pos['start_pos'][i]:link_pos['end_pos'][i]])
                
            for i in range(len(filenames)):
                
                filenames[i] = concatenate_alias(filenames[i])
                
            
        return filenames



def add_md_extension(filename):
    got_extension, type_ = get_file_type(filename)
    if type_ is None:
        return filename + ".md"
    return filename
    




def find_file_paths_in(directory, searched_filenames):
    files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for name in searched_filenames:
            if add_md_extension(name) in filenames:
                final_path = dirpath + "/" + add_md_extension(name)
                if "//" in final_path:
                    final_path = dirpath + add_md_extension(name)
                if ".trash" not in final_path:
                    files.append((final_path, add_md_extension(name)))
    return files



def copy_files(filenames, source_directory, target_directory, additional_file_path=None):
    source_paths = find_file_paths_in(source_directory, filenames)
    for files in source_paths:
        source_file_path = files[0]
        target_file_name = files[1]
        # print(target_file_name)
        # print(os.path.exists(source_file_path))
        if os.path.exists(source_file_path) and not os.path.exists(target_directory + target_file_name):
            dst_path = os.path.join(target_directory, target_file_name)
            shutil.copy(source_file_path, dst_path)
            print(target_file_name)
        elif not os.path.exists(source_file_path):
            print(f"{source_file_path} does not exist.")
        elif (os.path.exists(target_directory + target_file_name)):
            pass
            # print(f"Current file {source_file_path} has already been copied - {target_directory + target_file_name}.")
        else:
            print(f"Something went wrong.")
        if (additional_file_path != None and os.path.exists(additional_file_path)):
            name = os.path.basename(additional_file_path)
            if (not os.path.exists(target_directory + name)):
                shutil.copy(additional_file_path, target_directory + name)
    
    for i in range(len(source_paths)):
        source_paths[i] = source_paths[i][0]
    return source_paths


def parse_recurse_copy_files(parse_file_path, source_dir, target_dir, max_depth, current_depth, parsed_files=[], going_deep=False):
    if (max_depth > current_depth):
        # Extract filenames from the markdown file
        print(f"PARSING THE {parse_file_path} FILE")
        filenames = parse_filenames_from_markdown(parse_file_path)
        # print(filenames)

        source_paths = None
        # Copy files to the target directory
        if (not going_deep):
            source_paths = copy_files(filenames, source_directory, target_directory, additional_file_path=markdown_file_path)
        else:
            source_paths = copy_files(filenames, source_directory, target_directory)

        # Print the list of copied file paths
        copied_file_paths = [os.path.join(target_directory, add_md_extension(filename)) for filename in filenames]
        parsed_files.append(parse_file_path)
        if len(source_paths) > 0:
            for path in source_paths:
                # print(source_paths)
                if not path in parsed_files:
                    print(f"{path} is not parsed. Parsing...")
                    parse_recurse_copy_files(path, source_dir, target_dir, max_depth, current_depth + 1, parsed_files, True)
    



##############################
# WORKING ZONE



# print('Copied file paths:', copied_file_paths)

parse_recurse_copy_files(markdown_file_path, source_directory, target_directory, parsing_depth, 1)

