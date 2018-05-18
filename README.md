# ShortifyURL
Creates a minimized version of the given URL.

Uses a MD5 hash of the original URL

Coverts the Hash value to base64 encoding 

Stores the hashed base64 value along with the original URL in DB

The hashed base64 value is the shortened URL.

URL deployed at: https://vivekrana.pythonanywhere.com

Please note : The web app is not handling any UI validations as of now. But Backend validation is implemented to take care of checking for valid URL.
