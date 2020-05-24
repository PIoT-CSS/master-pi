## Car Share System (CSS): Master Pi

#### Recommended: making virtual environment

```bash
python3 -m venv venv
. venv/bin/activate
```

#### Installation

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

#### To run unit testing with pytest:

Execute the following in the root folder. Ensure `css_unit_test` database is created.

```bash
pip3 install -e . && pytest
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
- To manage cars, please go to 'hostname/management/cars'.
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


