# obsidian_packager

This is a program that allows you to export a tree of files from your Obsidian vault. 

## Usage

In scripts directory there is a packager.py file. In the beginning of the file you can see 4 variables:

```
markdown_file_path = '/your/path/to/file/name' + '.md'
source_directory = '/path/to/your/vault/'
target_directory = '/path/to/destination/'
parsing_depth = 6
```

Thees variables are everything you need to specify to start working.

- `markdown_file_path` - is a path to the file that starts the tree
- `source_directory` - is where your vault lies
- `target_directory` - is where you want to copy your files
- `parsing_depth` - is the maximum depth of parsing the links that limits the script in going further into your vault then you want

> **Warning!** All of the 3 paths must exist beforehand, else the script will throw errors!

After specifying the variables just run the script and see magic happen.