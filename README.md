# Sed Online - Find and Replace Text

[![GitHub issues](https://img.shields.io/github/issues/Pop101/SedOnline)](https://github.com/Pop101/SedOnline/issues)

# Table of Contents

- [Sed Online - Find and Replace Text](#sed-online---find-and-replace-text)
- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
  - [Usage](#usage)

# Overview

Guess the person from 5 sentences about them from their wikipedia page.
Every guess reveals more information about the person, starting from obscure sentences from their page, to more and more revealing ones.

Try it out at [https://sedonline.leibmann.org](https://sedonline.leibmann.org)!

# Technologies

This project is created with:

- [Flask](https://flask.palletsprojects.com/en/2.0.x/): 2.0.2
- [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/): 2.1.2
- [Simple CSS](https://simplecss.org/): 2.2.1
  
# Getting Started

Clone the Repo and ensure poetry is installed
```
git clone https://github.com/Pop101/SedOnline/issues
pip install poetry
```

Install the dependencies
```
poetry install
```

Edit the config file (```./config.yml```)

Run the webserver
```
poetry run app.py
```

## Usage

Just connect to the webserver on port 2043
```http://localhost:2043```

To use the API, send a GET request to
`Get /<pattern>/<replacement>/<input>`

`pattern` is a regular expression.
`replacement` is a string.
`input` is a string or URL.

The response should mirror the input reponse (assuming the input is a URL).

Note that for now, only the Global Matchall regex flag is supported.

You can always customize anything in
```config.yml```, just note that doing so
might require you to restart the webserver
