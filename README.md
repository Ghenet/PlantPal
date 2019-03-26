# PlantPal
PlantPal is an app designed to simplify plant owners' lives and help them keep their plants alive. Users can sign up and add which plants they have from a designated list. Once they add their plants, it will automatically begin calculating when the plants' next water day is. When you have exceed the amount of time between waterings, the tracker will let you know and you can reset the counter after you water your plant.

https://plant-pal.herokuapp.com/

![profile](https://cdn.glitch.com/3f59e2c6-0558-4467-9057-8202e97223b4%2FScreen%20Shot%202019-03-24%20at%203.32.57%20PM.png?1553495462186)


-Plant Page Where the used picks a plant

![plant's page](https://cdn.glitch.com/3f59e2c6-0558-4467-9057-8202e97223b4%2FScreen%20Shot%202019-03-24%20at%2011.35.52%20PM.png?1553495782703)

## Technologies Used:
- Python Flask 
- Sqlite DB
- Peewee
- JavaScript and Ajax
- Custom HTML, CSS, Bootstrap

## Our Process
The first steps we took with this project was to plan out our database and how our tables would be connected together. We decided to use three tables, Users, Plants, and Users' Plants, which is a join table. The join table is where we stored information of when the plant was added and the date it was last watered so we could track when it needed to be watered. We also sketched out our wireframes and defined our user stories. Users can signup/login and they will be redirected to their profile. From their profile page, they can view their profile information and their existing plants. Once they click to add new plants, they will be redirected to a plant selection page. Users can select multiple plants and optionally add notes to the plants as well. Once they have added all the plants they want, they are redirected back to their profile where they can see all the plants.

![](https://trello-attachments.s3.amazonaws.com/5c8fe1271ba21e4277577ca1/5c8fea55bd0cdb7ca079996a/b51bee25c16ae8e1b12b0e4c5aeb604d/IMG_5465.jpg)

## Challenges and Wins
  Wins :
   - Core understanding of the languages, ORM and libraries we used 
   - Creating multiple user’s plants at the same time
  Challenges:
   - Deployment. Unfortunately Heroku had an issue closing the database so our seed data did not properly populate the database
   - Updating the user’s plants (notes and watering)

## Future Development Ideas
Due to the time constraints and the pace we had to learn new technologies, there were some features we wanted to implement but weren't able to.
 - Email reminders
 - Search bar for plants
 - See other users' plants, make posts, share advice, etc.

## PlantPal App File Hierarchy:

![plantpal Hierarchy](https://cdn.glitch.com/3f59e2c6-0558-4467-9057-8202e97223b4%2FScreen%20Shot%202019-03-24%20at%2011.29.08%20PM.png?1553495377297)
