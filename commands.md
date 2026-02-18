# This is a command to create a new environment with the name as game 
- python -m venv game
# To activate the environment we the the below command
- .\game\Scripts\activate
# If any error named "Script cannot be executed" is seen give the following command
- Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
# We need to install specific libraries according to our project 
- pip install <package name>