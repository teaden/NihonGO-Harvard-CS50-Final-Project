import os
import re
import string
import nltk

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from helpers import apology

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///words.db")


@app.route("/", methods=["GET", "POST"])
def index():
    """Show homepage"""
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Ensure user does not leave text field blank if translating a string
        if request.form.get("choice") == "stringchoice" and not request.form.get("input_text"):
            return apology("Please enter text that you would like to translate.")
        
        # Ensure user actually uploads a text file if translating a file
        if request.form.get("choice") == "filechoice" and not request.form.get("input_file"):
            return apology("Please upload a text file to translate.")
        
        # Ensure user cannot translate a string and a file at the same time
        if request.form.get("input_text") and request.form.get("input_file"):
            return apology("You may not translate both a string and a text file at the same time.")
        
        # Translates English string into Japanese string
        if request.form.get("choice") == "stringchoice" and request.form.get("language") == "JPchoice" and request.form.get("input_text"):
        
            # Splits words and punctuation from string into a list
            # https://stackoverflow.com/questions/39330619/how-to-split-sentence-including-punctuation
            p = re.compile(r"\w+(?:'\w+)*|[^\w\s]")
            initialText = p.findall(request.form.get("input_text"))
        
            # Initialize new list to hold translated elements from inputted string
            finalText = list()
        
            # Iterate over inputted string
            for i in range(len(initialText)):
            
                # Attempts to find Japanese word equivlanet in database
                try:
                    JPword = db.execute("SELECT Japanese FROM E_J WHERE English=:English", English=initialText[i].lower())
                    JPword = JPword[0]["Japanese"]
                    finalText.append(JPword)
            
                # If no Japanese element is found, word is appended as originally inputted
                except IndexError:
                    if initialText[i] in string.punctuation:
                        finalText.append(initialText[i] + " ")
                    else:
                        finalText.append(initialText[i])
        
            # Join list of translated elements into string
            translated = ''.join(finalText)
            
            # Render apology if user tries to translate Japanese into Japanese
            if translated == request.form.get("input_text"):
                return apology("Your request could not be processed. Please re-phrase and try again.")
            
            # Return translated text
            return render_template("output.html", translated=translated)
    
        # Translates English text file into Japanese text file
        if request.form.get("choice") == "filechoice" and request.form.get("language") == "JPchoice" and request.form.get("input_file"):

            # Splits words and punctuation from string into a list
            # https://stackoverflow.com/questions/39330619/how-to-split-sentence-including-punctuation
            p = re.compile(r"\w+(?:'\w+)*|[^\w\s]")
            with open(request.form.get("input_file"), "r") as f:
                fileText = f.read()
                initialText = p.findall(fileText)
        
                # Initialize new list to hold translated elements from inputted string
                finalText = list()
        
                # Iterate over inputted string
                for i in range(len(initialText)):
            
                    # Attempts to find Japanese word equivlanet in database
                    try:
                        JPword = db.execute("SELECT Japanese FROM E_J WHERE English=:English", English=initialText[i].lower())
                        JPword = JPword[0]["Japanese"]
                        finalText.append(JPword)
            
                    # If no Japanese element is found, word is appended as originally inputted
                    except IndexError:
                        if initialText[i] in string.punctuation:
                            finalText.append(initialText[i] + " ")
                        else:
                            finalText.append(initialText[i])
        
                # Join list of translated elements into string
                translated = ''.join(finalText)
                
                # Render apology if user tries to translate Japanese into Japanese
                if translated == fileText:
                    return apology("Your request could not be processed. Please re-phrase and try again.")
                
                # Return translated text
                return render_template("output.html", translated=translated)
    
        # Translates Japanese string into English string
        if request.form.get("choice") == "stringchoice" and request.form.get("language") == "ENchoice" and request.form.get("input_text"):
    
            # Declare and initialize necessary variables for translation
            initial = request.form.get("input_text").replace(" ", "")
            initialList = list()
            finalList = list()
            JPdict = db.execute("SELECT Japanese FROM E_J")
            JPlist = list()
        
            # Create a list of Japanese words in dictionary for reference
            for i in range(len(JPdict)):
                JPlist.append(JPdict[i]["Japanese"])
        
            # Add dictionary words from user inputted text to new list for translation
            i = 0
            while i < len(initial):
                for j in range(len(initial), -1, -1):
                    if initial[i:j] in JPlist:
                        initialList.append(initial[i:j])
                        i = j - 1
                        break
                i = i + 1
        
            # Translate each dictionary word from user inputted text
            for i in range(len(initialList)):
                ENword = db.execute("SELECT English FROM E_J WHERE Japanese=:Japanese", Japanese=initialList[i])
                ENword = ENword[0]["English"]
                finalList.append(ENword + " ")
            final = ''.join(finalList)
        
            # Correct spacing for punctuation and capitalize first word
            text = re.sub(r'\s([!"#$%&()*+,-./:;<=>?@[\]^_`{|}~"](?:\s|$))', r'\1', final).capitalize()

            # Capitalize the first letter of each subsequent sentence
            # https://stackoverflow.com/questions/26320697/capitalization-of-each-sentence-in-a-string-in-python-3
            sentences = nltk.sent_tokenize(text)
            
            # Join list of translated elements into string
            translated = ' '.join([s.replace(s[0], s[0].capitalize(), 1) for s in sentences])
            
            # Render apology if user inputted text not in dictionary
            if not translated:
                return apology("Your request could not be processed. Please re-phrase and try again.")
            
            # Return translated text
            else:
                return render_template("output.html", translated=translated)

        # Translates Japanese text file into English text file
        if request.form.get("choice") == "filechoice" and request.form.get("language") == "ENchoice" and request.form.get("input_file"):
            
            with open(request.form.get("input_file"), "r") as f:
                attempt = f.read()
                
                initial = attempt.replace(" ", "")
                initialList = list()
                finalList = list()
                JPdict = db.execute("SELECT Japanese FROM E_J")
                JPlist = list()
        
                # Create a list of Japanese words in dictionary for reference
                for i in range(len(JPdict)):
                    JPlist.append(JPdict[i]["Japanese"])
        
                # Add dictionary words from user inputted text to new list for translation
                i = 0
                while i < len(initial):
                    for j in range(len(initial), -1, -1):
                        if initial[i:j] in JPlist:
                            initialList.append(initial[i:j])
                            i = j - 1
                            break
                    i = i + 1
        
                # Translate each dictionary word from user inputted text
                for i in range(len(initialList)):
                    ENword = db.execute("SELECT English FROM E_J WHERE Japanese=:Japanese", Japanese=initialList[i])
                    ENword = ENword[0]["English"]
                    finalList.append(ENword + " ")
                final = ''.join(finalList)
        
                # Correct spacing for punctuation and capitalize first word
                text = re.sub(r'\s([!"#$%&()*+,-./:;<=>?@[\]^_`{|}~"](?:\s|$))', r'\1', final).capitalize()

                # Capitalize the first letter of each subsequent sentence
                # https://stackoverflow.com/questions/26320697/capitalization-of-each-sentence-in-a-string-in-python-3
                sentences = nltk.sent_tokenize(text)
        
                # Join list of translated elements into string
                translated = ' '.join([s.replace(s[0], s[0].capitalize(), 1) for s in sentences])
                
                # Render apology if user inputted text not in dictionary
                if not translated:
                    return apology("Your request could not be processed. Please re-phrase and try again.")
            
                # Return translated text
                else:
                    return render_template("output.html", translated=translated)
                
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("home.html")
        

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
