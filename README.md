# spot-api
Here you can find the repository of the technical test for backend developer. :D
## Environment preparation
Note: This example is done from a CMD in Windows, in the case of using a Linux terminal or even a PowerShell it could vary.  
The first thing we will do is download the repository.  
~/> git clone https://github.com/Juandadgj/spot-api.git  
Being in the root folder of the project we are going to prepare the dependencies.  
~/spot-api/> python -m venv venv  
~/spot-api/> venv/Scripts/activate.bat  
~/spot-api/> pip install -r requirements.txt  
**And that's it, with this we should have the environment ready to run!**
## Django Preparation
We need to create the database with your models before running our server. For that we will do the following:  
~/spot-api/> python manage.py makemigrations  
~/spot-api/> python manage.py migrate  
**Now we are ready to start.**  
~/spot-api/> python manage.py runserver  
## Overview
**To understand the basic operation of this api we can rely on the Postman documentation here: https://documenter.getpostman.com/view/20398385/UyxjFm2S**  
In architectural terms we don't have much to talk about. Everything is within the Django and Django Rest Framework standards. The code is fairly self-descriptive assuming the reader has basic knowledge of Django. I'll just make a couple of notes where I see fit.  
### GET: init() '/'
In the root path of the server, the consumption of the external API is made, where the song data is located. This information is defragmented and imported into our database, which is made up of the following models:  
- Song ( id, name, releaseDate, url, artistId, genderId )
- Artist ( id, name, url )
- Gender ( id, name, url )
### POST: login() 'login/'
This endpoint is where we can perform the authentication and obtain the token that will allow us to perform the queries that require it. Now, since a method to create a user is not implemented, we can create a Django administration user to execute the tests. You can do it this way:  
  
~/spot-api/> python manage.py createsuperuser  
  
It will ask you to enter a couple of pieces of information and you will be ready to get your token.
### POST: createSong() 'create-song/'
To create a song we must have a couple of considerations. Obviously, we can't make a song from an artist or genre that doesn't exist, so we have to be careful with that. Being the case that we want to create artists and genres, we can do it. **See the Postman documentation. There is the example of creating a song by The Weeknd that does not exist for example**  
## Points to improve
Like any software, you can always polish more. I would have liked to implement a management system for users. Endpoints were also missing to obtain only the artists or genres with a more complete model, but the dataset did not go far. It was missing to implement a better handling of exceptions with queries to the database. And many more things but time is not enough either. In short, I hope that it can comply with the majority, with more time something better is done. :D
