# Tamagochi: Pet Simulation Website
## Motivation:
Originally, Tamagochi is a virtual pet simulation game played through a small egg-shaped device. While some of us wish to revisit our childhood memories by playing the game, it is surprisingly inaccessible today. By making a web version of this game, we believe we can make Tamagotchi both free to use and accessible from multiple devices without the need for installation. Some creativities are added as well.
## Functions and Features:
#### 1. User Registration / Login / Logout / Change Password
- Registration is based on email confirmation
- Pet's age is calculated by user's accumulated login time
- User can reset the password if he/she forget the password through email
- User can change the password by confirming his/her old password

#### 2. Pet Generation
- User would be given an egg after successfully activate his/her account. 
- The pet would be named by user.
- The pet appearance and gender would be randomly assigned by system from 16 male characters and 16 female characters

#### 3. Pet Status / Death
- Pet would have "Health", "Energy", and "Happiness" value to measure its status. The status would be updated every 5 seconds by Ajax.
- "Health" is affected by weather. For instance, bad weather condition like snowing and raining would decrease pet's health. (The weather system is based on the real weather in Pittsburgh by using API) User can increase the pet's "Health" by buying drugs in Hospital.
- "Energy" is continously decreasing in a certain rate. And playing game would decrease the pet's energy, too. User can increase the pet's "Energy" by buying food in store.
- "Happiness" is continously decreasing in a certain rate. User can increase the pet's "Happiness" either by playing games or buying toys in the store.
- Pet would die if any of the these three become zero. Died pet would be saved in Hospital - Previous. And user would be given a new egg.

#### 4. Friend / Marriage System
- User can add friend by fuzzy querying "username"
- User can see "nearby" friend (based on user's login location information) and send the invitation to add friends.
- User can feed friends' pets
- Pet may propose to another pet if both of them are higher than level2.
- Pet can only propose to the different gender and can only propose to his/her friend
- After marrying with another pet, two pets share one warehouse. But would not share wallet.
- If one pet die, his/her partner would become single again.

#### 5. Game
- There are two single games and one multiple game
- Single game one: Floppy Tamagochi
- Single game two: Catch your Tamagochi
- Multiple game: Racing Game

#### 6. Love Wall
- User may post love massage in Love Wall
- Other user may click "thumbsup" to like a post
- User's pet may propose to another pet in Love Wall and also would receive love massage in Love Wall


# TEAM MEMBERS
- Zhe Zhao
- Cheng Chen
- Mengdi Yang
- Chenxi Li

# PROJECT URL
http://54.80.8.195/

# DEPLOYMENT PLATFORM
AWS EC2
gunicorn / daphne / nginx

# Development Environment
- Python version: python 3.7
- Django version: Django 2.1
- Email Server: Gmail SMTP server
- Database: MySQL

# Development Techniques
HTML / CSS / JavaScript / JQuery / Ajax / WebSocket /

# API
- Weather API： https://openweathermap.org/api openweathermap
- Geological API： （pip install django-ipware）

# REFERENCES
### CSS Library
- Bootstrap 3.3.7
- W3CSS Library (https://www.w3schools.com/w3css/4/w3.css)
- hoverCSS Library (http://ianlunn.github.io/Hover/)
- Font: Abel (http://fonts.googleapis.com/css?family=Abel)
- Font: Amatic+SC (http://fonts.googleapis.com/css?family=Amatic+S)
- Font: Indie+Flower (http://fonts.googleapis.com/css?family=Indie+Flower)

### Online Source
- Floppybird (https://github.com/nebez/floppybird)

### Images
- Qiantu Website: http://www.58pic.com/ (copyright: Commercially available)
