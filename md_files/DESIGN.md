Overview:

This document is an in-depth review of the design decisions that serve as
the foundation for the "NihonGO!" web application. While some of these design
decisions are aesthetic, many decisions have a technical basis; line numbers
and the name of the file being discussed will be included when applicable. In
general, this document organizes design decisions from "higher level and less
technical" to "low level and more technical".


Website Home Page: Lack of Username/Password Requirement
Where: Click on the corresponding link after running "flask run" in 
application.py

While "NihonGO!"" is largely based on the Problem Set 8 distribution code, 
which had a username and password requirement, this program does not requirement
login information. In general, unlike a finance application, this application
contains little to no sensitive information. Even if the user uploads a text
file to translate that has sensitive information, the website itself does not
store these uploads. Additionally, it was decided that, as a translation app,
"NihonGO!" should be accessible to as many people as possible with an easy-to-
use user interface. Thus, the username/password requirement is not included.


Website Home Page: Language 
Where: Click on the corresponding link after running "flask run" in 
application.py

The website home page has text in both English and Japanese, as the program is
designed to accommodate users who are fluent in either language. In short,
many people who will potentially use this program likely do not speak
English and Japanese, so the program is designed with that assumption in mind.


Website Home Page: Japanese->English Translations and Kanji
Where: Click on the corresponding link after running "flask run" in 
application.py. This note applies to Japanese->English translations for both
strings and files.

For Japanese inputs, only the kanji version of words, when applicable, is
accepted. The program is designed this way because the kanji version of words,
while more advanced linguistically, is also more common in Japanese society.
Just as users fluent in English should be able to translate text into Japanese,
those fluent in Japanese should be able to use this application to 
receive English output without using more elementary and less common 
versions of Japanese words. While including multiple versions, both advanced
and elementary, of Japanese words was considered, the former ended upload
being the primary focus due to running time concerns. The program currently
has to search a dictionary of over 50,000 English and Japanese words. Including
multiple versions of Japanese words could potentially double or triple that
number at least.


Core Translation Logic: General
Where: Execute "phpliteadmin words.db" in terminal window to view SQLite 
Database. Elements of this database are called on lines 65, 104, 132, 151, 183, 
202 of "application.py"

Using the Google Translate API or a Python library with translation
functions was certainly possible instead of building the translation logic. 
However, relying on one of these more advanced algorithms entirely would have
significantly reduced the work required for this project. Thus, as the program
creator, I decided to design the project based on my own programming knowledge
(and how far I could push and develop that knowledge) rather than relying on
another individual or company's Machine Learning capabilities, for example.

Whereas Google Translate seems to use Machine Learning to teach the program 
the nuances of language over numerous iterations, "NihonGO!" utilizes SQLite
as the core mechanism for its translation function. While there are differences
between the "English->Japanese" and "Japanese->English" translation functions
(which will be discussed below), both functions generally follow the same logic:

1.) The user inputs a string or uploads a text file
2.) That string or text file is turned into a list of its corresponding words
3.) Each word, in a loop, is passed as the "where" component in a SQL
    query that pulls the matching word in the opposite language
    
    a.) i.e. "JPword = db.execute("SELECT Japanese FROM E_J WHERE 
              English=:English", English='day'" yields "日"

4.) Each translated word is appended to a new list
5.) This list in joined together to form the final translated string.

The SQLite database has over 50,000 of the most common English words and their
Japanese translations. I found the Japanese translations by organizing the list
of English words in Google Sheets and using the GOOGLETRANSLATE function. Please
note that while I did use Google Translate to develop my English-Japanese 
dictionary, again, I did not want to rely on it entirely in place of building 
my own logic or Python code in this case. In other words, the Python code
I developed is what allows the English-Japanese dictionary to be utilized
effectively.


Core Translation Logic: English->Japanese and Japanese->English Differences
Where: Lines 50 - 125 of "application.py" - English->Japanese Translation Code
       Lines 126 - 225 of "application.py" - Japanese->English Translation Code

Please note that the core translation logic for English->Japanese strings
and English->Japanese text files is nearly identical. The logic for the Japanese
->English strings and Japanese->English text files is also very similar. Due to 
this fact, I considered making this logic its own function and simply calling 
that function in both the English->Japanese string section and the English->
Japanese file section, for example. I would have then done the same for the 
Japanese->English code sections. However, using a variable from a for loop 
inside of a SQL query complicated this endeavor. Ultimately, it was decided that 
it was more practical design wise to fully write out the necessary translation 
code in both the string section and the file section for each respective language 
even though the code is very similar.

Unlike the Japanese->English functionality (discussed below), the 
English->Japanese translation logic first separates English words into a list
using both white space and punctuation as the separators (using the re library). 
This logic greatly reduces the time it takes for the English->Japanese 
translation code to execute. 

The alternative to separating by white space would involve looping over possible 
substrings of the initial text provided by the user. Anytime a substring matches
a word in the SQLite English-Japanese dictionary, it can be considered valid
and is then appended to a list. This process was necessary for the Japanese->
English sections of code because Japanese traditionally does not have spaces
between words and phrases. This process does increase the time for Japanese->
English translation functions to run; after all, each word has to be identified
in a dictionary of over 50,000 words before it can be considered eligible to
add to the list for translation. However, without incorporating this logic,
using a SQLite English-Japanese dictionary for translation may not have been
possible. A more detailed example of this process is described below:

1). Consider the string "美味しい魚" (which means "Delicious fish" in English)
2). Despite the fact that this Japanese phrase consists of two English words,
    it does not appear that splitting by any basic element (i.e. punctuation
    or space) is possible.
3.) "NihonGO!" has a nested loop, which first views every possible substring
    relative to the first character. For example, first it will check if
    "美味しい魚" is in the dictionary. If it is not, then the program checks
    if "美味しい" is in the dictionary. If it is, the first character after this
    word (魚) becomes the new character that every subsesquent character is 
    compared to. Since there are no subsequent characters after "魚" in this
    case and "魚" is in the dictionary on its own, "魚" is also added to the 
    the list.
4.) The list is then ['美味しい', '魚']. Each of these words is then passed to
    the Japanese-English dictionary in a loop in order to append the Equivalent
    English words to a new list.
5.) Lines 208-213 (using the re and nltk libraries) ensure that any punctuation
    is spaced correctly in the new English phrase and that every sentence
    begins with a capital letter