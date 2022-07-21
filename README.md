<p align="center">
    <h1 align="center">Synthetic eventlog generator</h1>
    <h2 align="center">SEA - Spring 2022 </h2>
    <br>
</p>

This project is the main project for the course Software Engineering and Architecture at the program Master of Science in Computer Science at the University of Copenhagen. It is developed in the programming language Python. The framework used for the user interface is Kivy.

It includes three major parts: The user interface, the Editor and the Simulator.

## REQUIREMENTS

```
python3.9

altgraph==0.17.2
attrs==21.4.0
certifi==2021.10.8
charset-normalizer==2.0.12
cycler==0.11.0
docutils==0.18.1
fonttools==4.33.3
idna==3.3
iniconfig==1.1.1
kaki==0.1.5
Kivy==2.1.0
kivymd==0.104.2
Kivy-Garden==0.1.5
kiwisolver==1.4.2
macholib==1.16
matplotlib==3.5.2
micropm4py==0.2.1
monotonic==1.6
networkx==2.8
numpy==1.22.3
packaging==21.3
Pillow==9.1.0
pluggy==1.0.0
py==1.11.0
pydot==1.4.2
Pygments==2.12.0
pyinstaller==5.1
pyinstaller-hooks-contrib==2022.6
pyparsing==3.0.8
pytest==7.1.2
python-dateutil==2.8.2
requests==2.27.1
six==1.16.0
tomli==2.0.1
urllib3==1.26.9
watchdog==2.1.7

```

## INSTALLATION

You can get the project by unzipping the .zip file uploaded.

If you are a developer of the project, you can also access it by cloning the project from Github with the following command:

```
git clone https://github.com/AbrakaBarna/sea-directed-graph.git
```

After that you can install the required dependencies with [pip](https://www.w3schools.com/python/python_pip.asp) if you have [Python] (https://www.python.org/downloads/) installed.
If you do not have [Python] (https://www.python.org/downloads/), you may install it by following the instructions
at [python.org](https://www.python.org/downloads/).

The recommended way of running the project is through a virtual environment. You can create one with [virtualenv](https://virtualenv.pypa.io/en/latest/) if you have it installed. If this is not the case you can install it with the following command:

```
pip install virtualenv
```

After this you can create the virtual environment with the following command:

```
virtualenv <env_name>
```

After this, you can activate the environment. On Windows you can use:

```
./<env-name>/Scripts/activate.bat
```

On MacOs and Linux:

```
source <env_name>/bin/activate
```

If it was successful your terminal will indicate this with the (`<env_name>`) sign.

You can find all the dependecies in the requirements section above or in the setup.py file. You can always check if an install was successful with the `pip freeze` command.

You can then install the project dependencies using the following command:

```
pip install <dependency-name>
```

## USAGE

After installing every dependency you should be able to access the application with the command:

```
python3 main.py
```

## DEVELOPMENT

- Open the Issues tab in the GitHub repository and grab an unassigned issue
- Assign it to yourself
- Change the status of the issue in the project from Todo to In progress
- Work on the issue
- If you want to add commit your changes please do the following:
  - checkout a new branch (please name your branch after the number of the issue and the name of ticket, for example 1-prepare-the-skeleton)
  ```
  git checkout -b <issuenumber-description>
  ```
  - add all your changes
  ```
  git add .
  ```
  - commit the changes (please name your branch after the number of the issue and a short description, for example "1 - prepared the project skeleton")
  ```
  git commit -m "ticket number - short description"
  ```
  - push your changes
  ```
  git push
  ```
- Open a new pull request on GitHub. As the reviewer please set up every developer in the current sprint.
- Please wait until you get at least one approved review.
- Merge the branches
- Delete the old branch
- Change the status of the issue in the project to Done
- Close the issue

## TESTING

Tests for testing file manager are under the `tests` directory

In order to run the tests you can run the following command in your favourite terminal:

```
python3 -m pytest tests/*
```
