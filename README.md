# Flask KITTI Demo


### Screenshot

![Screenshot](_/screenshot_back_oxts.png)


### Requirements

- python (>=3.5)
- Flask
- Pandas
- PyTables


### Project Structure

- kittiproject
-- dataset (KITTI dataset files)
-- flaskapp (Flask application)
--- application (Core application and template files)
--- data (KITTI data storage files)
--- logs (Flask application log files)
--- static (CSS and JavaScript files)
--- config.py (Flask app configuration)
--- main.py (Main entry point)
--- run (Run app script)
-- migration (imports KITTI data to a H5 file)


### Installation

Navigate to project directory.
Optionally install virtual environment with:
```
virtualenv env -p python3
```
Start virtual environment with:
```
. env/bin/activate
```
Install required Python libraries with:
```
pip install -r requirements.txt
```


### Configuration

Make sure that appropriate port (default one is 4000) is free before running the application. You can change the port in PROJECT_DIR/config.py file by changing the PORT constant.


### Usage

From the project directory execute:
```
./run
```
or
```
python3 main.py
```
Open http://localhost:4000/ or http://127.0.0.1:4000/ in your web browser. 

### Credentials

username: demo
password: demo


### API

API key:

TODO
