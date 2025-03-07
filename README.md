# COMP 8800 and 8900 Major Project
> The *Secure MoniTor Toolkit* is a forensics toolkit, which offers a user-friendly solution to enhance the detection and response of digital forensic incidents. Users can upload files to check for file integrity.

## Table of Contents
- [Technologies](#technologies)
- [Operating Systems](#operating-systems)
- [How to run the project](#how-to-run-project)
- [Features](#features)

## Technologies
* Frontend: React, JavaScript
* Backend: Python, Flask
* Database: [MongoDB](https://www.mongodb.com/)
* Hosting for initial prototype: [Netlify.com (frontend)](https://www.netlify.com/), [Render.com (backend)](https://render.com/)

## <a id="operating-systems">Operating Systems</a>

This project has been tested on:
* Windows 11
* macOS Sonoma 14.4.1
* Fedora 40
* Ubuntu 2024.04 LTS
* Manjaro

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

**Note:** There is a `.env` file that is needed in order for the database and security functionality to work.

In the respective folders, you will need to install these packages:
#### React Frontend (major-project-frontend folder):
```
npm install
```
#### Python Backend (major_project_backend folder):
The backend requires a virtual environment to be setup. 

**Windows and Linux (Fedora, Manjaro):**
```
python -m venv venv
```
**Mac and Linux (Ubuntu):**
```
python3 -m venv venv
```

Activate the virtual environment.

**Windows:**
```
.\venv\Scripts\activate
```
**Mac and Linux:**
```
source venv/bin/activate
```

The packages below need to be installed.

**Windows and Linux (Fedora, Manjaro):**
```
pip install flask flask-cors pymongo python-dotenv reportlab pycryptodome python-docx PyPDF2 PyJWT

```
**Mac and Linux (Ubuntu):**
```
pip3 install flask flask-cors pymongo python-dotenv reportlab pycryptodome python-docx PyPDF2 PyJWT
```

### Running the project locally:
#### Backend (Python)
1. Open Command Prompt (Windows) or Terminal (Mac and Linux)
2. `cd` into your project folder (for example: `cd BScACS-MajorProject`)
3. Type `cd major_project_backend`
4. Type the following commands

**Windows:**
```
.\venv\Scripts\activate
python backend.py
```
**Mac and Linux (Ubuntu):**
```
source venv/bin/activate
python3 backend.py
```
**Linux (Fedora, Manjaro):**
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