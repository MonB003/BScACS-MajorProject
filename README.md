# COMP 8800 and 8900 Major Project
> The *Secure MoniTor Toolkit* is a forensics toolkit, which offers a user-friendly solution to enhance the detection and response of digital forensic incidents. Users can upload files to check the file integrity.

[Hosted App Link](https://major-project-monb.netlify.app/)

## Table of Contents
- [Technologies](#technologies)
- [Dependencies](#dependencies)
- [How to run the project](#how-to-run-project)
- [Features](#features)

## Technologies
* Frontend: React, JavaScript
* Backend: Python, Flask
* Database: MongoDB
* Hosting: [Netlify.com (frontend)](https://www.netlify.com/), [Render.com (backend)](https://render.com/)

## Dependencies
This project has been tested on:
* Windows 11
* Fedora 40

## <a id="how-to-run-project">How to run the project</a>
### Prerequisites:
- Have a Git and GitHub account
- Have Visual Studio Code or another coding editor

### Configuration instructions:

You will need to install:
- [Node package manager](https://nodejs.org/en/download/) (npm)
- [Python](https://www.python.org/downloads/)
- [Pip package management](https://pypi.org/project/pip/) (pip)

Cloning the repository:
- Open Command Prompt 
- `cd` into the folder you want the repository stored in
- Type: `git clone https://github.com/MonB003/BScACS-MajorProject.git`

<b>Note:</b> There is a `.env` file that is needed in order for the database functionality to work.

In the respective folders, you will need to install these packages:
#### React-Frontend (major-project-frontend folder):
```
npm install 
```
#### Python-Backend (major-project-backend folder):
```
pip install flask
pip install flask-cors
pip install pymongo
pip install python-dotenv
pip install reportlab
```
The backend requires a virtual environment to be setup:
```
python -m venv venv
```

### Running the project locally:
#### Server (Python)
1. Open Command Prompt
2. `cd` into your project folder
3. Type `cd major-project-backend`
4. Type the following commands

<b>Windows:</b>
```
.\venv\Scripts\activate
python backend.py
```
<b>Linux:</b>
```
source venv/bin/activate
python backend.py
```
5. This will start the server on http://localhost:5000

#### Client (React)
1. Open Command Prompt
2. `cd` into your project folder
3. Type `cd major-project-frontend`
4. Type `npm start`
5. Go to http://localhost:3000 on any browser
6. This will direct you to the main page

## <a id="features">Features</a>
- File metadata extraction
- Secure logging
- Real-time alert system