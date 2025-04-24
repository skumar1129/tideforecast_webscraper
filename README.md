# Sahil Tideforecast Scraper

## Project Background
A webscraping application that get the tideforecast of different locations defined in a list

## Tech Stack
Python, Selenium

## Instructions to run:

### Create Virtual ENV
```python3 -m venv env```

### Activate Virtual ENV
```source env/bin/activate```

### Install Dependencies
```pip install -r requirements.txt```

### Run Scraper
```python scraper.py```

### Note
When the script is ran too often the site will have a pop up ad that will cause the web driver to hang. In this case, quit all chrome processes where a web driver is running in and restart the script.