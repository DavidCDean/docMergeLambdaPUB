# docMergeLambdaPUB

Read more at:
https://www.davidcdean.com/salesforce-record-data-pdfs/

Adding some (admittedly sketchy) example code.

- buildspec.yml : Example for basic Amazon CI build
- src / SFConnect.py : Quick and dirty SFDC API client
- src / TokenMerge.py : Shims simple Docx Merge with docxtpl
- src / pullAndMerge.py : Entry and control flow for Lambda func
- src / requirements.txt : Any pip install reqs during build