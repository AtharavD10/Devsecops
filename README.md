Project Overview
The Gym Management Web Application allows users to register for memberships, view and edit diet plans, and access personalized fitness recommendations. It is built using Python and Django with a responsive frontend using HTML and CSS. The application is deployed on AWS EC2 and includes CI/CD integration using Jenkins and GitHub, with static code analysis performed via SonarQube.

Prerequisites
Ensure the following tools and environments are set up:

Python (version 3.12 or higher).
Pip (Python package manager).
Virtual Environment (venv).
AWS EC2 instance (configured with SSH access and a public IP).
Jenkins (installed and configured for CI/CD).
SonarQube (optional, for static code analysis).
Git (for version control).


Installation Steps

Step 1: Clone the Repository
SSH into your EC2 instance:
ssh -i <your-key.pem> ec2-user@<your-ec2-public-ip>
Clone the project repository:
git clone <your-repo-url>
cd <repository-name>

Step 2: Create and Activate a Virtual Environment
Create a virtual environment:
python3 -m venv myenv
Activate the virtual environment:
source myenv/bin/activate

Step 3: Install Dependencies
Install the required Python packages:
pip install -r requirements.txt

Deployment Steps
Step 1: Database Migration
Run the following command to set up the database:
python manage.py makemigrations
python manage.py migrate

Step 2: Create Superuser
To access the admin interface, create a superuser:
python manage.py createsuperuser

Step 3: Run the Application
Start the Django development server:
python manage.py runserver 0.0.0.0:8000
Access the application in your browser at:
http://<your-ec2-public-ip>:8000


CI/CD Integration
Jenkins Configuration
Log in to Jenkins and create a new pipeline.
Link the pipeline to your GitHub repository.
Add a Jenkinsfile with the following steps:
Pull the latest code from GitHub.
Install dependencies.
Run database migrations.
Restart the Django application.
Static Code Analysis
Analyze your code using SonarQube.
Fix any identified issues such as code smells, vulnerabilities, and bugs.
Commit the changes to GitHub and re-analyze until the quality gate passes.
Additional Notes
Security: Ensure sensitive data is stored securely using .env files and exclude them from the repository using .gitignore.
Monitoring: Use AWS CloudWatch or similar tools to monitor server performance and logs.
Future Enhancements:
Add HTTPS by configuring an SSL certificate.
Improve test coverage by writing automated tests.