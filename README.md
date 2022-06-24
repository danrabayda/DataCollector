# DataCollector
A specific use case of an OCR (Optical Character Recognition) 

This code uses pytesseract ocr to watch youtube videos and assign labels with timestamps.

1. use data_collector.py to collect the timestamps as clean as possible
2. (optional) use cleaner.sh to remove repeated lines from logs if needed
3. import the log data into a .csv file and clean up slight discrepancies if needed.
4. use data_cleaner.ipynb to pull out specific information from the general csvs and save video times, labels, and any other data as well (i.e. additional classification info)

Much of the base code comes from Stack Overflow, 
Credit to user Kingsley https://stackoverflow.com/questions/52899174/real-time-ocr-in-python
