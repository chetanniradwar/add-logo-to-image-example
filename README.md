
## Project Setup for Mac
1. create a project folder `WaterMarkAdder`

2. clone the git repo locally using `git clone https://github.com/chetanniradwar/add-logo-to-image-example.git
` in 'blogs' folder

3. in current folder run `pipenv shell` to create virtual environment

4. `pipenv install` to install all the project dependencies

5. then, `cd watermarkadder` folder inside which `manage.py` file is there.

6. run `python manage.py migrate` to migrate all migrations and create table in the database

7. run `python manage.py runserver` to run the development server on 8000 port


## Postman documentation link
- [postman doc link](https://documenter.getpostman.com/view/20803750/2s93mByKQT)


## Technologies Used
- `djangorestframework` - to make REST apis in django
- `pipenv` - for making virtual environment
- `djangorestframework-simplejwt` - for authenticating apis
- `boto3` for AWS integration
- `pillow` for adding watermark/logo to an image


## Database
- `sqlite`
