#!/bin/bash

# Define the path to the answer folder
ANSWER_FOLDER="answer"

# Define the files to check for
FILE1="clickme.exe"
FILE2="document.pdf.exe"

# Define the website link to display
WEBSITE_LINK="http://192.168.8.111:8000/company.html"

# Check if the answer folder exists
if [ ! -d "$ANSWER_FOLDER" ]; then
    echo "Error: The answer folder does not exist."
    exit 1
fi

# Check if both files are in the answer folder
if [ -f "$ANSWER_FOLDER/$FILE1" ] && [ -f "$ANSWER_FOLDER/$FILE2" ]; then
    echo "Congratulations! You've found the suspicious files."
    echo "Access the company website at: $WEBSITE_LINK"
    
    # Optional: You can open the browser automatically
    # Uncomment one of these lines based on your operating system:
    # open "$WEBSITE_LINK"  # macOS
    # xdg-open "$WEBSITE_LINK"  # Linux
    # start "$WEBSITE_LINK"  # Windows (if using Git Bash or similar)
else
    echo "The suspicious files have not been found yet."
    
    # Optional: You can provide more detailed feedback
    if [ ! -f "$ANSWER_FOLDER/$FILE1" ]; then
        echo "Missing: $FILE1"
    fi
    if [ ! -f "$ANSWER_FOLDER/$FILE2" ]; then
        echo "Missing: $FILE2"
    fi
fi
