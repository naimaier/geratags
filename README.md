# geratags
Tool that generate tags for tridium's supervisory system.

# building
Build exe with pyinstaller:
```pyinstaller --onefile --noconsole --icon=icon.ico geratags.py```

# using
This is a very specific software, that uses very specific input files to generate a very specific output file. And it will only be useful for the case it was intended to.
This software generates a *settings.json* file to remember last settings, so it's advisable to use it inside a folder.

## the input file
The input file must be a *.CSV* file with 2 columns, the first being the component's name (with dashes) and the second it's ID.
```
700-TT-01;750
700-TT-02;751
700-TT-03;752
```

## the template file
The template file must be a *.txt* file. 
Use the wildcard **$** where you want the software to include the component's name without dashes.

## the output files
The software will generate one .mne file for each row of the input file, where the file name will be the component's name without dashes.
Each output file will have these two lines:
```
#ID:763
#Name:"700-LT-01"
```
followed by whatever is written in the template file, replacing the wildcard **$** with the **component's name without dashes**.
