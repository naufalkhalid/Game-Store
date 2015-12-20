Project Plan
-----------------------

### 1. Team

545691 Gaurav Bhorkar
534398 Manish Thapa
546687 Naufal Khalid



### 2. Goal

In this project we will be building an online game store for JavaScript games. The game store will be a marketplace where players can buy games and developers can sell their games on the platform.



### 3. Plans

The platform will have multiple pages. For the basic functionality we have discussed the following important views in our web-application:

1. Home Page (To display all the games available)
2. Game Page (A page where the game can be played/bought)
3. User/Developer Dashboard (User can see bought games, Developer can see added games)
4. Sign-up (To register new player/developer)
5. Log-in (For sign in)
	
Furthermore, we plan to have the following models:

1. User 
It will store the user details and will have a flag which will tell apart whether the user is a player or a developer. We will check the flag and provide appropriate functionality to the user.
Fields:
	* Id
	* Name
	* Last Name
	* Email
	* Password
	* Developer Flag

2. Game
The Game model will store all the games added by developers to the marketplace. It will also store the price set by the developer.
Fields:
	* Id
	* Developer Id (from User model)
	* Title
	* Source (Link to the HTML file)
	* Price (set by developer)
	* Category (Game category to facilitate searching)
	
3. PlayerGame
This model is to keep track of which user has purchased what games. When a player purchases a game, it will be added to this table against the username of the player. This will also keep track of the game state and the score of the player.
Fields:
	* Game Id (from Game model)
	* Player Id (From User model)
	* PurchasedOn Timestamp (When the game was purchased)
	* PurchasePrice (Price at which game was purchased, used in statistics)
	* State
	
4. ScoreBoard
This model will keep track of the score submission from games. Whea a player is playing a game and a score is submitted, it will add a new entry in this table. 
Fields:
	* Timestamp (Time at which the score is submitted)
	* Game Id (from Game model, game which submitted the score)
	* Player Id (from User model, player playing the game)
	* Score 
	
Following sections describe the plans for implementing each feature:

#### 3.1. Authentication
We plan to use the Django Authentication system to implement authentication service for the users and developers. The Login view will be for input and a session will be created when a user logs in. Based on the user type (player or developer), he will be directed to appropriate dashboard (player or developer). We will also include email verification process. 

#### 3.2. Developer Functions
The developer functions will be accessed from the developer dashboard view. To add new games, we will create a new view which will add the game link and its price to the Game model. We will also provide the functionality to update the price of the game. The sales statistics can be shown on the dashboard and can be gathered from the PlayerGame model. 

#### 3.3. Player Functions
A player can see the games bought by him from the player dashboard view. To play the game, we will create a Game view. Upon navigating to the Game view, we will confirm if he has bought the game (from PlayerGame model) and then load the iframe.
If the player has not bought the game, then a "Buy" option will be presented. When the player buys the game, an entry will be created in the PlayerGame table. The recommended mock payment service will be used. 
A player can find the games form the Home view, where games will be able to be searched based on category and text input.

#### 3.4. Game/Service Integration
The integration between the game and service will be done using message transfer between the iFrame and the parent window. The messages will be used as described in the project requirements.

#### 3.5. Security
We will make the application try to prevent SQL Injections, XSS, CSRF attacks.


#### 3.5. Extra features
The extra features we plan to implement are:
	* Save/Load and resolution feature
	* RESTful API
	* Mobile Friendly
If time permits, we will try to implement other features. 



### 4. Process and Time schedule
So far, we have decided to collaborate over email. Moreover, we will be meeting in the campus every alternate day to discuss about the current status of the project and take appropriate actions. We will distribute work equally amongst the team members.

Following is the rough timeline for the project:

Due Date	Feature Completion
01-01-2016	Basic HTML Views, Models, and Authentication
15-01-2016	Developer and Player Functionality
30-01-2016	Payment Functionality + Save Load features
10-02-2016	Home View and Searching games
15-02-2016	Final touch up and bug fixes



### 5. Testing
We will use the example game provided to test the game service.

