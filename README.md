# Dublin-Bikes-Helper.
UCD SoftwareEng Group Project

Welcome to Dublin-Bikes-Helper, a comprehensive web application designed to enhance your cycling experience in the heart of Dublin City. Launched as part of a group project at UCD Software Engineering, our platform aims to streamline the use of the dublinbikes service, a popular public bike rental scheme initiated in 2009.

As a well-established mode of transportation, Dublinbikes has over 114 stations scattered around the city center, enabling citizens and tourists to easily navigate the city. Dublin-Bikes-Helper leverages this infrastructure to offer a more personalized, convenient, and efficient service for its users.

We aspire to revolutionize your cycling journey through Dublin-Bikes-Helper, providing critical information to help plan your routes, locate nearby stations, and much more. Our platform is built with a simple objective - to make the dublinbikes service as user-friendly and accessible as possible. Join us and transform the way you explore Dublin today!

![Loading web main images](https://github.com/ddrangers/Dublin-Bikes-Helper/blob/main/Deployment_DBH/SCR-20230616-qibv.png)

### Application Features

The app is deliberately designed to be simple to use. On opening the website, the user will be directed to click the appropriate bike marker on the map that they want information on. The website will then instantaneously produce that information. That is it!
This feature is based on the very successful Amazon ‘One-Click’ buying model which was developed by them in the 2000s. While users are not buying anything on our app, the convenience of receiving the required information with a single click is very powerful. Once the user clicks on a bike station they will receive

- The current weather
- Address of the bike station
- Whether it’s open or closed
- Current bike and parking availability
- Predicted availability for both bikes and parking over the course of the day.
  
If the user wants to look at information for another location, they just click on that station and the equivalent information pops up.
We looked at adding other features like predicted availability on other days, but that would require the user to enter additional information, and we felt this extra work would not be worth the trade-off in the extra information received by them.

We collect over 25 million data points each year to build our predictive model. As our database grows and our model is refined, we will be able to provide better predictions for the user and so improve their cycling experience.

## Architectural Structure
The application itself is hosted on a secure AWS EC2 Cloud-based server. The information that we collect to build our Machine Learning (ML) model is stored in an equally secure Amazon RDS database using a MySQL format.

Our front-end application (what the user sees) uses the backend ‘Flask’ application to interface with the servers and user requests. The front-end and back-end use separate Nginx servers. This approach enhances the system's reliability by isolating the concerns of the front-end and back-end components, enabling each server to focus on its specific functionality. This makes our system more scalable and secure.

![Loading architectural](https://github.com/ddrangers/Dublin-Bikes-Helper/blob/main/Deployment_DBH/SCR-20230616-qink.png)

This is a [Link to Team Project Report](https://drive.google.com/file/d/1KB-yEbXPoYGJePXZjVJho3lNMFpHjprZ/view?usp=sharing).


