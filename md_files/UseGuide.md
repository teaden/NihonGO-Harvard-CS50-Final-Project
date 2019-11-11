Overview:

This document will serve as a guide regarding how to configure and use the 
"NihonGO!" application. This program is a web application that is able to 
translate text from English to Japanese and from Japanese to English. The user 
is able to supply a string by entering text manually into the provided textbox. 
However, the user can also upload a text file to translate.


Configuration:

The program is similar to the latter Problem Sets in that it is a web
application populated via Flask. As such, the user simply needs to open
the "application.py" file within the CS50 IDE and type and confirm "flask run"
in the command line. Simply click on the link that is subsequently produced
in the command line to access the website.


Website Layout:

All of the application's functions are based in the website home page. In
other words, the home page is the only page that the user needs to interact
with. The page contains text in both English and Japanese that greets the
user and establishes rules for how to maximize translation accuracy.

The website prompts the user to first select a language preference. "English->
Japanese" takes English input and yields output in Japanese. "Japanese->English"
takes Japanese input and yields output in English. The user must choose then 
choose a content type between "String," for which the user manually enters text 
to translate, and "File," for which the user must upload a text file to 
translate.


"English->Japanese" General Translation Guidelines and Rules:

The following rules apply regardless of whether or not the user inputs a
manually entered string or a text file. For input in English, the user should 
select the "English->Japanese" radio button and include appropriate spaces 
between words. For example, the "the phone rang" is acceptable, whereas 
"thephonerang" is not. The latter will result in an apology message to the user 
indicating that the user should re-phrase the input. Using a Japanese string or 
text file instead of English input when "English->Japanese" is selected will 
also result in this error. When one word is separated and recognizable in the 
case of "the" in "the phonerang", the program will yield a partial translation.


"Japanese->English" General Translation Guidelines and Rules:

The following rules also apply regardless of whether or not the user inputs a
manually entered string or a text file. For input in Japanese, the user may or 
may not use spaces between words and phrases. However, since the Japanese 
language tends to minimize spaces, it is recommended that the user do so as
well.

The most important note for "Japanese->English" translation is that only the
most common versions of words are accepted. In other words, when applicable,
use the version of a word that has kanji in it. Kanji characters are the most
advanced in the Japanese alphabet but also the most common. In other words,
"日" is the kanji character meaning "day" in English and is pronounced "nichi".
However, this Romanized version "nichi" or the hiragana version "にち" are not
accepted since a more common version of the word (the kanji version "日"). 
It is important to note that the most common version of a Japanese word does
not always contain kanji. For example, "こんにちは", meaning "hello" in English,
only contains hiragana characters.

Luckily, if you wish to manually type Japanese text to translate in a string
format, Japanese keyboards (which can be found on a Mac under "Settings", then
"Keyboard", then "Input Sources") typically produce the version of a word with
kanji, when applicable, automatically. In other words, typing "にち" on a 
Japanese keyboard will automatically yield "日".

If you are still confused, you do not have to worry about manually entering
text in a string format to use "Japanese->English" translation. Included with
this program are a variety of English and Japanese sample text files that can
be translated. File translation will be described in further detail in a
subsequent section.


"English->Japanese" and "Japanese->English" String Translations:

If you wish to manually enter text to translate, please select the "String"
radio button on the website home page. Simply following the general guidelines 
listed above for English input and Japanese input respectively will allow the
user to maximize accuracy for string translations.


"English->Japanese" and "Japanese->English" File Translations:

If you wish to translate a text file, please select the "File"
radio button on the website home page. Included with this program are sample
text files that you can translate. These files are as follows (with underscores
instead of spaces): "ENG 100 Common English Words", "ENG Let It Be The Beatles",
"ENG Robert Frost", "JP Kanji List", "JP Passage", "JP Vocabulary". The "ENG"
files are designed to be used for "English->Japanese" file translations, and
the "JP" files are designed to be used for "Japanese->English" file
translations.

Clicking the "Choose File" button will prompt the user to upload a file from
his or her computer. You can download the aforementioned files to your computer.
Please note that these files must also exist in the same folder as the program
in order for the program to reference the files. If you attempt to upload a file
that is not in the same folder as the program, this action will result in an
Internal Server Error. If you wish to translate a file that is not already
included with the program, simply drag that file from your files to the 
"nihongo" directory in CS50 IDE.


Other Errors: "Your request could not be processed. Please re-phrase and try 
again."

If the user follows the above guidelines and still sees the above apology when 
attempting to translate, it means a word or group of words in the string
or text file is not included in the associated English-Japanese dictionary
that exists in SQLite. Since this program translates strings and text files
word by word using this dictionary, the user will need to rephrase his or her
query and try again if this error is encountered after following the above 
guidelines.


SQLite: Japanese-English Dictionary

If the user wishes to view the Japanese-English dictionary table in SQLite, 
simply type and confirm "phpliteadmin words.db" in a separate terminal window.
Click on the corresponding link to view the database. You can see each entry
in the table by clicking the "Browse" action. If you wish to insert new data
into this table, click the "Insert" action.