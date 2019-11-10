# Splitted NZ #

## Additional Django apps dependencies
- Pillow
- django-imagekit

## Additional JavaScript apps dependencies
- jquery
- photoswipe

## Prerequisites

- Django-Python [development environment](https://www.djangoproject.com/start/) already set up.
- virtualenv installed.

## Forked from

[Django Photo Gallery](https://github.com/VelinGeorgiev/django-photo-gallery)
by Velin Georgiev ([@VelinGeorgiev](https://twitter.com/velingeorgiev))

## Minimal Path to Awesome

- Clone this repository.
- Open the command line, navigate to the django app folder and execute:
    - `virtualenv env` (requires virtualenv), Mac `virtualenv yourenv -p python3.6`
    - Linux: `source env/bin/activate`, Windows: `call env/Scripts/activate.bat`, Mac `source env/bin/activate`
    - navigate to the `django_photo_gallery` folder using `cd django_photo_gallery`
    - execute `pip install -r requirements.txt` or `pip3 install -r requirements.txt` depending on your python installation. 
    - If the Pillow fail to install on Windows, then install it manually `pip install ../whl/Pillow-5.0.0-cp36-none-win32.whl` (if you are not using python 3.6 32 bit then  [download the Pillow wheel](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow) for your python version).
    - Run `python manage.py migrate` or `python3 manage.py migrate`
    - Run `python manage.py runserver` or `python3 manage.py runserver` depending on your python installation
    - Open http://127.0.0.1:8000/ in web browser.
    - To access the admin forms go to http://127.0.0.1:8000/admin/ and enter user: admin, password: administrator
