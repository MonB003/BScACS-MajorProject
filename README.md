# COMP 8800 and 8900 Major Project
> The *Secure MoniTor Toolkit* is a forensics toolkit, which offers a user-friendly solution to enhance the detection and response of digital forensic incidents. Users can upload files to check for file integrity.

[Hosted App Link](https://major-project-monb.netlify.app/)

## Table of Contents
- [Technologies](#technologies)
- [Operating Systems](#operating-systems)
- [How to run the project](#how-to-run-project)
- [Features](#features)

## Technologies
* Frontend: React, JavaScript
* Backend: Python, Flask
* Database: [MongoDB](https://www.mongodb.com/)
* Hosting: [Netlify.com (frontend)](https://www.netlify.com/), [Render.com (backend)](https://render.com/)

## <a id="operating-systems">Operating Systems</a>

This project has been tested on:
* Windows 11
* macOS Sonoma 14.4.1
* Fedora 40

## <a id="how-to-run-project">How to run the project</a>
### Prerequisites:
- Have a Git and GitHub account
- Have Visual Studio Code or another coding editor (for viewing and editing the code if needed)

### Configuration instructions:

You will need to install:
- [Node package manager](https://nodejs.org/en/download/) (npm)
- [Python](https://www.python.org/downloads/)
- [Pip package management](https://pypi.org/project/pip/) (pip)

Cloning the repository:
- Open Command Prompt (Windows) or Terminal (Mac and Linux)
- `cd` into the folder you want the repository stored in
- Type: `git clone https://github.com/MonB003/BScACS-MajorProject.git`

**Note:** There is a `.env` file that is needed in order for the database functionality to work.

In the respective folders, you will need to install these packages:
#### React Frontend (major-project-frontend folder):
```
npm install
```
#### Python Backend (major-project-backend folder):
The backend requires a virtual environment to be setup. 

**Windows and Linux:**
```
python -m venv venv
```
**Mac:**
```
python3 -m venv venv
```

Activate the environment.
**Windows:**
```
.\venv\Scripts\activate
```
**Mac and Linux:**
```
source venv/bin/activate
```

The packages below need to be installed.

**Windows and Linux:**
```
pip install flask
pip install flask-cors
pip install pymongo
pip install python-dotenv
pip install reportlab
```
**Mac:**
```
pip3 install flask
pip3 install flask-cors
pip3 install pymongo
pip3 install python-dotenv
pip3 install reportlab
```

### Running the project locally:
#### Backend (Python)
1. Open Command Prompt (Windows) or Terminal (Mac and Linux)
2. `cd` into your project folder (for example: `cd BScACS-MajorProject`)
3. Type `cd major-project-backend`
4. Type the following commands

**Windows:**
```
.\venv\Scripts\activate
python backend.py
```
**Mac:**
```
source venv/bin/activate
python3 backend.py
```
**Linux:**
```
source venv/bin/activate
python backend.py
```
5. This will start the server on http://localhost:5000

#### Frontend (React)
1. Open Command Prompt (Windows) or Terminal (Mac and Linux)
2. `cd` into your project folder (for example: `cd BScACS-MajorProject`)
3. Type `cd major-project-frontend`
4. Type `npm start`
5. Go to http://localhost:3000 on any browser
6. This will direct you to the main page

## <a id="features">Features</a>
- File metadata extraction
- Secure logging
- Real-time alert system