# Project 4 - Gamers Assemble

`Explore a wide variety of games, join an existing group or create your own. Chat with other members and provide feedback by rating the group. Personalize your profile and browse other users' profiles.`

## Running locally

```
pipenv install            # or: pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata jwt_auth/seeds.json genres/seeds.json games/seeds.json groups/seeds.json members/seeds.json ratings/seeds.json groupchat/seeds.json
python manage.py runserver
python manage.py test     # API tests
```

Without any environment variables the app uses a local SQLite file and development settings. Point the frontend at it with `VITE_API_URL=http://127.0.0.1:8000/api`.

## Deploying (Render)

The Heroku free tier no longer exists, so the repo ships a Render Blueprint (`render.yaml`):

1. Push this repo to GitHub.
2. In Render choose **New + > Blueprint** and select the repo. It creates the web service and a Postgres database, generates `SECRET_KEY` and wires up `DATABASE_URL`.
3. When asked, set `CORS_ALLOWED_ORIGINS` to your frontend's URL (e.g. `https://gamers-assemble.netlify.app`, no trailing slash).
4. The first deploy loads the demo data because `LOAD_SEEDS=true`. Remove that variable afterwards if you like.
5. In the frontend host (Netlify) set `VITE_API_URL=https://<your-service>.onrender.com/api` and redeploy.

Notes: free web services sleep after inactivity (the first request can take ~30-60 s), and free Render Postgres databases expire after 30 days unless upgraded.

Environment variables: `SECRET_KEY`, `DEBUG`, `DATABASE_URL`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `LOAD_SEEDS`.

## Table of Contents:

1.  Project Overview
2.  Features
3.  Project Brief
4.  Technologies Used
5.  Timeline
6.  Wins and Challenges
7.  Bugs
8.  Future Content and Improvements
9.  Key Learnings
10. Credits

## Project Overview

Project 4 was the most challenging and rewarding project I undertook during my GA immersive course. I wanted to achieve as many stretch goals as possible and spent considerable time refining my design and style. Initially, I had various ideas for the project, but after consulting with my instructors, I decided to build a multiplayer game group finder. As a lifelong gamer, I was passionate about this idea and put a lot of effort into the project. The group finder was completed within a 17-day period, and it was the last project for our immersive GA course. The backend database was deployed using Heroku, while the frontend was deployed on Netlify. Creating this project with Python Django was a new and exciting yet challenging experience for me. It was my first time working on a larger scale project with this language, but I found working on it quite intriguing and enjoyable.

You can find the deployed project [here](https://gamers-assemble.netlify.app/)

As most actions are locked before authentication registration would be required, but you can also use the premade user's credential which would be: user@gmail.com for email and **userPassword** for password. You can also login with user1@gmail.com and user2@gmail.com using the same password as before, if you want to perform additional tests. The game "Rust" which is the first one on the games list has groups already created.

![Alt text](https://i.imgur.com/RE50Eee.png "Optional title")

## Features

- Home page displaying a quote for games and a button to go to the browse games page
- Register and login page for user authentication
- The project features a navigation bar and footer that allow users to easily move between the Home, Browse, Register, and Login pages. The navigation bar also includes a donut menu for easy access to its options.
- If the user is logged in, register and login links are replaced by the user's username and a logout function. Username links a user to their profile page.
- Two browse pages with games, each game linking to a detailed page with groups for that game
- Group page where users can chat with other members, rate the group and if the owner, edit name and description of group and remove members
- User profile page displaying their details, joined groups, and created groups with the ability to edit user's details
- Error handling included for various actions performed
- Backend API built with Python Django
- Frontend built with React
- PostgreSQL database (deployed on Render via `render.yaml`)

## The Brief

- Build a full-stack application by making your own backend and frontend
- Use Django API to serve your data from a Heroku database
- Consume your API with a separate frontend built with React
- Be a complete product which most likely means multiple relationships and CRUD functionality for at least a couple of models
- Be deployed online so it's publicly accessible

## Technologies Used

### Backend:

- Django: a Python web framework used for building the project.
- Pylint: a static code analysis tool used for Python code quality.
- PyJWT: a Python library used for JSON Web Token (JWT) authentication.
- psycopg2-binary: a PostgreSQL adapter for Python used for connecting Django with PostgreSQL database.
- django-cors-headers: a Django library used for handling Cross-Origin Resource Sharing (CORS) headers.
- gunicorn, whitenoise and dj-database-url (production server, static files and `DATABASE_URL` support for hosting on Render)
- django-rest-framework: a powerful and flexible toolkit for building Web APIs with Django.

### Frontend:

- React: a JavaScript library for building user interfaces
- React DOM: provides an API for manipulating the DOM
- React Router Dom: a popular routing library for React applications
- Axios: a promise-based HTTP client for making API requests
- Bootstrap: a popular CSS framework for building responsive websites
- React Bootstrap: a library that integrates Bootstrap components with React
- JWT Decode: a library for decoding JSON Web Tokens
- React Circular Menu: a circular menu component for React applications
- Sass: a preprocessor scripting language that is interpreted into Cascading Style Sheets (CSS)
- Styled Components: a library for styling React components using CSS-in-JS syntax
- @types/react: type definitions for React
- @types/react-dom: type definitions for React DOM
- @vitejs/plugin-react: a plugin for Vite, a build tool for modern web development, that enables support for React applications
- Vite: a build tool for modern web development that aims to provide a faster and leaner development experience.

## Timeline

### Day 1

On my first day of the project, I began by carefully planning out the steps I would need to take to achieve my goals. Using Excalidraw, I visualized the different components that would be necessary for my project, as well as identified which elements would be my stretch goals. This planning helped me to stay organized and focused on the most important aspects of my project, while also giving me a clear roadmap to follow. By taking the time to plan out my project in advance, I was able to optimize my workflow and ensure that I was making the most of my time and resources.

![Alt text](https://i.imgur.com/OXT95ZJ.png "Optional title")

I then started working on the backend using Django. I first had to set it up. I installed the necessary dependencies like Pipenv and Django, created a virtual environment and entered the shell using "pipenv shell". I started the app using "django-admin startproject project ." and then run the migrations by doing "python manage.py migrate". I created a super user so that I could get my development server up and running with "python manage.py createsuperuser" and ran my server using "python manage.py runserver" to check for any errors.

### Day 2,3,4,5,6

The following day, I began creating the different apps that would be included in the project starting with games. I ran the command django-admin startapp games then made the models and views that would be associated with games. Game model would also have a **ManyToManyField** relationship with groups. I also added the app inside the "INSTALLED_APPS" section in project settings and registered the game model to the admin site.

Game model:

![Alt text](https://i.imgur.com/lLPPrrp.png "Optional title")

INSTALLED APPS:

![Alt text](https://i.imgur.com/l0KJ4uU.png "Optional title")

admin.py:

![Alt text](https://i.imgur.com/gUbIn3O.png "Optional title")

As I wanted to create two separate pages for games, and I was unfamiliar with this task I asked ChatGPT for some guidance. I imported PageNumberPagination and modified my "get all games" function in my views file which looked like this:

![Alt text](https://i.imgur.com/7FQzW33.png "Optional title")

Continued with adding a serializers folder containing the common and populated serializer and a urls file. I added the games app in the

Serializers:

![Alt text](https://i.imgur.com/qAutpjh.png "Optional title")

Urls:

![Alt text](https://i.imgur.com/CrZsabw.png "Optional title")

Finally, I passed the games app URL to the project's URL file.:

![Alt text](https://i.imgur.com/dI02BqP.png "Optional title")

I continued with the development process by creating additional apps, starting from the games app, moving to the genres app, and finally creating the jwt_auth app to handle user authentication. Throughout this process, I frequently used commands such as "python manage.py makemigrations" and "python manage.py migrate" to ensure that my database schema was up-to-date. Additionally, I tested the functionality of each app using Postman to ensure that it was working as expected. Next, I added a **ForeignKey** relationship to the game model for the groups app, followed by the creation of the members app, group chat, and finally the ratings app. The trickiest ones were the last three needing multiple relationships with the group and the user.

Code to delete a member:

![Alt text](https://i.imgur.com/cBkkorL.png "Optional title")

Posting a message in group chat:

![Alt text](https://i.imgur.com/aPO8ccI.png "Optional title")

The ratings app isn't complete yet and it doesn't work like I want it to in the frontend but I'm close:

**(Code updated)**
![Alt text](https://i.imgur.com/9YqqQH1.png "Optional title")

The ratings feature has two view classes, one for liking and one for disliking. The ratings model contains two BooleanFields named "has_liked" and "has_disliked". These fields should be checking whether the user has liked or disliked a certain item and disables the corresponding button on the frontend. The fields also increment or decrement the respective like or dislike count when the user clicks the corresponding button.
Another challenging one was posting a new group. Here I wanted to be able to add a new group by grabbing the title of the game that I wanted to add the group to. I then added the id of the Game object to the request data as the game field. I then set the owner field of the request data as the id of the currently authenticated user. I also set the members field to an empty list, as I did not want to add any members while creating a new group.

![Alt text](https://i.imgur.com/GlpctYp.png "Optional title")

### Day 7,8,9,10,11,12

As I began developing the frontend using React and Vite, I utilized the development server in Django to write some seed data and test whether the game details would display in the frontend. I started with creating the homepage, which was static and included a button to navigate the user to the browse games page. From there, I quickly moved on to creating the register and login page. To capture the input from the user, I utilized "[e.target.name]" and "e.target.value" in the input fields. I then pushed this data to the backend using an axios.post request to either the /login or /register url. For the login page, I also set the token in localStorage upon successful login using the onSubmit function.

Login:

![Alt text](https://i.imgur.com/mF4hKeH.png "Optional title")

Continued with the navbar and footer using the loggedIn state variable to conditionally render the username and logout instead of register and login if the user is logged in:

![Alt text](https://i.imgur.com/DnS87Nh.png "Optional title")

![Alt text](https://i.imgur.com/z8hPNlU.png "Optional title")

Browse games page was a quite straightforward get request but getting the games to show in two different pages was a bit trickier, and I once again turned to chatGPT for assistance :

![Alt text](https://i.imgur.com/uwpIgrk.png "Optional title")

![Alt text](https://i.imgur.com/GOQYs4S.png "Optional title")

After completing the browse games page, I added the individual game page, which would display additional details and a list of groups created for that game. To achieve this, I used the **useParams()** hook to grab the id of the selected game from the URL. I then passed this id to an axios.get request to retrieve the game details and the list of groups associated with it and rendered everything on the page.
To redirect the user to the group page upon clicking a group, a Link element "<Link key={ind} to={`/groups/${item.id}`}>" was used with the 'to' attribute set to a specific URL of the group page which was obtained by extracting the id of the group from a "groups.map" function.

To create the group page, several functions were implemented to enable the desired functionalities. Firstly, the group name and description were made editable using input fields and edit, save and cancel buttons. Additionally, members could join or leave a group, leave messages if they were members, and group owners could remove members. Bootstrap alerts were also used to display errors that occurred during these actions. A like and dislike button was also added but their functionality still needs some work to achieve the desired result.

Join group, scroll to the bottom when new message is added, and add message functions:

![Alt text](https://i.imgur.com/40Dhgwt.png "Optional title")

Remove member from list and editable fields states:

![Alt text](https://i.imgur.com/XiHoXlQ.png "Optional title")

**(Code updated)**
Dislike and like functions called when clicking the like or dislike button:
![Alt text](https://i.imgur.com/tQ73qDl.png "Optional title")
Dynamic Rendering of Buttons with Conditional Styling Based on User Actions:
![Alt text](https://i.imgur.com/GvNQDqs.png "Optional title")

Editable field in return statement that appears if the user is the owner of the group:

![Alt text](https://i.imgur.com/RzLJ2hK.png "Optional title")

Message form that appears if the conditions "isOwner" or "foundMember" are satisfied:

![Alt text](https://i.imgur.com/9bQEm46.png "Optional title")

Finally I began implementing the user's profile page, where the user's details could be edited by clicking on an edit button, and then saved with a save button or discarded with a cancel button. The functionality was similar to that of the group page, where the owner of the group could edit and update group details. The page also contained a form that allowed the user to create a new group. This was achieved by including a dropdown menu from which the user could select the game's name to which they wanted to add the group. This was propably the trickiest part of this page:

Spread operator used to select group by its title using title as a parameter:

![Alt text](https://i.imgur.com/N8dqgva.png "Optional title")

Return statement, passing the game.title as an argument when the function **onSelectGame** is called in the dropdown menu :

![Alt text](https://i.imgur.com/ZjcIu1J.png "Optional title")

Since most of the functionality for the user's page had already been implemented earlier in other pages, the process of implementing the remaining functionality was fairly straightforward.

### Day 13,14,15,16

During the next four days, I dedicated my efforts to styling the project and ensuring that it was responsive. The task proved to be quite challenging, but I ultimately found the end result to be very satisfying. I utilized the inspect tool in my browser to navigate through elements, test different approaches, and observe results in real-time. This approach alongside using Bootstrap and media queries to make the styling more responsive significantly accelerated my progress and helped me achieve the desired outcome.

### Day 17

On the last day, I allocated some time to address some of the remaining bugs and enhance the styling. Afterward, we deployed the backend to Heroku with guidance from our instructor and the frontend to Netlify. The project was developed using version control with Git. Whenever changes were made, the changes were saved using "git add ." command, then committed using "git commit -m" command along with a message describing the changes, and finally pushed to two different GitHub repositories for the backend and frontend using "git push" command.

## Final project:

#### Homepage:

![Alt text](https://i.imgur.com/S7FzKWl.png "Optional title")

#### Browse games page:

![Alt text](https://i.imgur.com/SHhkRB2.png "Optional title")

#### Game page:

![Alt text](https://i.imgur.com/pChWUss.png "Optional title")

#### Group page:

![Alt text](https://i.imgur.com/of13eYD.png "Optional title")

#### User's page:

![Alt text](https://i.imgur.com/vbYVD38.png "Optional title")

#### Register page:

![Alt text](https://i.imgur.com/XfQdZNb.png "Optional title")

#### Login page:

![Alt text](https://i.imgur.com/eXlNJYM.png "Optional title")

## Wins and Challenges

### Wins

I consider one of my achievements in this project to be the styling, which is an area I was not very confident in. I allocated a significant amount of time towards it and managed to make the project responsive and aesthetically pleasing. Another major win was implementing the chatbox and the create group card, as well as making the user's and group's details editable. I was also happy about being able to handle various errors, especially in the register page, and display them through Bootstrap alerts.

### Challenges

During the project, I encountered various challenges, including resolving persistent bugs that surfaced after fixing some parts of the code. I often needed to carefully review the code to determine whether the problem was on the backend or frontend, although it was usually related to the frontend. To gain a better understanding of the issues, I relied heavily on **console.log** statements to observe the data and identify what wasn't working. Implementing the editable fields and getting the like and dislike button, which is not yet complete, to function correctly were also quite difficult. Another challenge I faced was knowing when to stop. I always wanted to add more functionality and improve the styling, but this often led to the appearance of last-minute bugs that needed to be fixed before deployment.

## Bugs

There are occasional internal server errors when refreshing or navigating pages, specifically on the user page. The issue appears to stem from attempting to retrieve both the currently logged-in user's data and another user's ID data when clicking on a username link in the navbar, footer, or on another user's profile page. This conflict may cause the page to break and malfunction, but a refresh usually resolves the issue. One potential solution is to selectively render a user's information based on whether they are the logged-in user or another user. Additionally, it may be helpful to review the code and ensure that any incorrect logic is corrected.

## Future Content and Improvements

Some of my future content plans:

- Refactoring code to make it more concise, DRY, and easier to read.
- Implementing the like and dislike functionality correctly
- Further improving upon the styling and responsiveness
- Enabling users to send friend requests and messages to each other
- Adding more information about each game, such as links to purchase sites and real-time data from Steam charts regarding the number of players currently in game

### Update

The ratings feature has been implemented, currently exploring options to save the user's actions on the frontend even after a page refresh. One possible solution would be to use local storage.

## Key Learnings

Improving my time management skills and working on the project regularly, breaking it into smaller parts, and following a plan was one of my significant achievements during this project. I have struggled with efficient time management in the past, so being able to accomplish this was a big win for me. Additionally, I gained a better understanding of the efficiency and ease of using Django for the backend, which helped me write data and set up the backend quickly. I also improved my knowledge of React and became more comfortable with hooks such as **useState**. Moreover, I discovered the power of ChatGPT and utilized it to accelerate my development process significantly.
