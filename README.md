## Car Share System (CSS): Master Pi

**Car Share System** is a full-stack car-share rental service system that runs on ***Raspberry Pi(s)*** while utilising ***IoT elements*** such as use of ***socket programming with MQTT pub/sub, facial recognition, QR generation and detection, Bluetooth technology and also Google Assistant SDK*** to complete the application suite.

![Car Share System Architecture Diagram](https://media.discordapp.net/attachments/429105317293326346/720991280699539616/Blank_Diagram.png?width=1098&height=921)

<center><strong>Car Share System Architecture Diagram</strong></center>

Skip to [Installation](#installation)

## Master Pi Features (Flask Web Application)

- **Car Share Booking System** for customers:
  - View and filter available cars in the system based on car attributes and pickup/return location
  - Make bookings with selected car for a specific timeframe
    - **Google Calendar Event** with booking specific details will be automatically created
    - Car's pickup/return location will be displayed on **Google Maps** with **Google Maps API**
  - Cancel upcoming bookings
    - **Google Calendar Event** with booking specific details will be automatically removed
  - View all of a customer's bookings
- **Car Share Admin System** for admins, managers and engineers:
  - Admin specific features:
    - View all of customers' bookings
    - Search and view user and cars
    - Add, remove and update cars and users
    - Report cars with issue
      - Engineers will be notified with **Pushbullet API**.
  - Manager specific features:
    - Visualisation graphs (from **Google Data Studio** and data from **Google Cloud SQL**) to make business decisions:
      - Daily Revenue Graph
      - Total Bookings of All Cars Graph
      - Daily Active Users
  - Engineer specific features:
    - QR code generation with profile details on account creation
    - View all pending and self-resolved issues with rental cars
      - Car's location will be displayed on **Google Maps** with **Google Maps API**
- **MySQL Cloud database** on **Google Cloud SQL** to store data.
- Google Asisstant SDK:
  - Pickup/return location (pickup/return), current location
  - Number of cars in the system
  - Error checking, if id doesnt exist
  - Car availablity
- **MQTT pub/sub system**, allowing Agent Pi to publish/receive data to/from Master Pi and perform necessary updates when needed:
  - Publish customer's photo when customer authenticates on Agent Pi with facial recognition option
  - Receive facial recognition result from Agent Pi
  - Verify customer's credentials when customer authenticates on Agent Pi with username/password
  - Mark booking status as active when customer is authenticated on Agent Pi
  - Mark booking status as inactive when customer returns car with Agent Pi
  - Publish all engineers' Bluetooth MAC addresses to Agent Pi for unlocking car with engineer's nominated Bluetooth device
  - Receive issue ID and engineer's profile details from Agent Pi to mark issue as resolved

## Installation

#### Recommended: making virtual environment

```bash
python3 -m venv venv
. venv/bin/activate
```

Execute the following in the root folder.  ***sudo*** is required to host on **port 80**. Ensure `css_test_1` database is created.

```bash
sudo pip3 install -e .
```

#### To run

```bash
sudo MasterCSS
```

or

```bash
sudo python3 -m MasterCSS.cli
```

#### To run Car Share Assistant:

Ensuring you have initialised OAuth 2.0 credentials from Google, execute the following in the root folder. 

```bash
chmod u+x runAssistant.sh && ./runAssistant.sh
```

You will need a microphone and speaker to use the assistant.

#### To run unit testing with pytest:

Execute the following in the root folder. Ensure `css_unit_test` database is created.

```bash
sudo python3 -m pytest
```

#### To generate docs in HTML:

Execute the following in the root folder.  ***sudo*** **is not required**.

```bash
pip3 install -e . && cd docs && make html
```

HTML docs will be in `docs/_build/html`.

#### To connect to Google Cloud SQL for proxy:

```bash
gcloud sql connect main-sql --user=root --project a2-css-iot
```

#### Uninstallation

```bash
sudo pip3 uninstall MasterCSS
```



#### Note

- To add/remove dependency packages, please modify `install_requires` in `setup.py` then reinstall the app.
- Prepare 2 mysql databases (as defined in `.env`):
  - `css_test_1` for MasterCSS app
  - `css_unit_test` for MasterCSS unit testing
- Configure Agent Pi's IP address in `.env`
- Modify your host file and make `carshare.com` redirects to Master Pi's IP.



#### Code Structure

- `setup.py` is used for configuring `MasterCSS` package, including dependency packages, entry point, etc.
- In `src/MasterCSS/`:
  -  `controllers/` contains Flask REST API controllers.
  -  `models/` contains classes and db functions for all entities.
  - `static/` contains static files such as `.js`, `.css` , `favicon.ico`, etc. Files are categorised into folders.
  - `templates/` contains `.html` template files.
  - `cli.py` contains Flask app initialisation code and configs, **also serves as MasterCSS's entry point**.
  - `tests/` contains unit tests.


