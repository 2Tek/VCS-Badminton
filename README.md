# For submission review:
1. Deployed on: Render.com
2. Assement Link:
- Singple Webpage Application: 
https://vcs-badminton-website.onrender.com
- Web Service: `https://vcs-badminton.onrender.com`
- Database External URL for verification if any: `postgresql://vcsbadminton_user:NMmOJFXkO58FjcZSH8RsSOj7yAD64GX5@dpg-cssofb23esus739op580-a.singapore-postgres.render.com/vcsbadminton`
# Project Rubrics
## Data Modeling
1. Architect relational database models in Python
2. Utilize SQLAlchemy to conduct database queries
- No raw sql used
- Correct applied SQLAlchemy to define model
- Creates methods to serialize model data and helper methods to simplify API behavior such as insert, update and delete.
## API Architecture and Testing
1. Follow RESTful principles of API development
  - RESTful principles are followed throughout the project, including appropriate naming of endpoints, use of HTTP methods GET, POST, PATCH, and DELETE
  - Routes perform CRUD operations
3. Structure endpoints to respond to four HTTP methods, including error handling
4. Enable Role Based Authentication and roles-based access control (RBAC) in a Flask application
- Player able to:
    - `delete:court-registrations`
    - `get:court-registrations`
    - `patch:court-registrations`
    - `post:court-registration`
 - Admin able to:
    - `delete:courts`
    - `get:courts`
    - `patch:courts`
    - `post:court`
5. Demonstrate validity of API behavior
API behavior can be tested through given postman collection
## Third-Party Authentication
- The Auth0 Domain Name
- The JWT code signing secret
- The Auth0 Client ID
- Roles and permission tables are configured in Auth0.
- Access of roles is limited. Includes at least two different roles with different permissions.
- The JWT includes the RBAC permission claims.
## Deployment
1. Application is hosted live at student provided URL
https://vcs-badminton-website.onrender.com
2. Includes instructions to set up authentication
- Go to User tab
- Click login button
- Default user can CRUD to enroll game
- Only admin role can create and delete court
## Code Quality & Documentation
1. Write clear, concise, and well-documented code
2. Project demonstrates reliability and testability
3. Project demonstrates maintainability

