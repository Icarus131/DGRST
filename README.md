# How to run

`pip install -r requirements.txt`

- Once you run `python3 manage.py runserver` you will be able to navigate to the localhost page. This will take you to a page with an oauth request link.
- Upon clicking the oauth link, you will be able to authenticate
- After authentication is succesful you will be redirected to the api response with the google calendar events.
- Each time to get info from the calendar api, you must re-authenticate
