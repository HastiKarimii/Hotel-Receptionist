# Hotel-Receptionist
This is a simple website to register and then add reservations etc. by the hotel receptionists.
For my hotel website project, I used Django as the backend framework and HTML, CSS and JavaScript as the frontend technologies. 
I implemented authentication and authorization features to restrict the access to the website to only receptionists or admins who have registered and verified their email. 
They can log in with their username and email and perform various tasks such as creating, updating or deleting reservations with traveler information. 
They can also change their passwords and access the functionalities of a normal user site. In addition, I designed an admin page with some filters to help the admins manage the website more efficiently.


Prerequisites

1. Install Python
Install python-3.7.2 and python-pip. Follow the steps from the below reference document based on your Operating System. Reference: https://docs.python-guide.org/starting/installation/

2. Setup virtual environment

#Install virtual environment
sudo pip install virtualenv


#Make a directory
mkdir envs


#Create virtual environment
virtualenv ./envs/

#Activate virtual environment
source envs/bin/activate

3. Install requirements
cd Hotel-Receptionist/
pip install -r requirements.txt

4. Run the server

#Make migrations
python manage.py makemigrations
python manage.py migrate


#Run the server
python manage.py runserver
