Chatbot for interacting with the e6data documentation. Ask your questions, get answers!

Before you start, please install the pre-requisites 
```
pip install requirements.txt
```

Then, get your openAI API key and add it to the code.
You can specify whether there is already a persitent index present (it will be in the stores folder) or whether to update the same.
If the persistence is already present, there is no need to make any changes.

If the persistence is not present, you have to add the documentation to '/docs/e6-documentation-main' and add the flag
```
index=load_data(False)
```

In order to run the program, simply type 
```
streamlit run persist-docu.py
```
in the terminal.
