# web_scrapper_ocr

Most of the web scrappers use the BeautifulSoup to read the response of the URL request response to extract the data they required.

Those web scrappers fail to extract the required text if it is not in text format.<br>
Below is the example where But it failed to extract the e-mail ID’s when I make the following URL request **https://www.google.com/search?q=emails+stryker.com%28"** which gives us 28 results of **emails stryker.com”**.

**My need is very simple, I need to get what I see with my eyes**. So, I tried using OCR/ML models to recognize characters from a given picture. Tesseract library, an optical character recognition (OCR) tool for python provided by Google.


We got the way to solve the problems, let’s start designing the program,
  
    1. Launch the web Browser
    2. Read the company name to search from an xlsx(Microsoft Excell) format file.
    3. Create the request URL
    4. Hit the URL using the browser object
    5. Take the screenshot of the body of the web page
    6. Read the screenshot to a text file using the pytesseract library.
    7. Use the regular expression to extract e-mail ID’s from the text file.
    8. Write the list of e-mail ID into a Spreadsheet.


