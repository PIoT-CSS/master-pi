## Car Share System (CSS): Master Pi

#### Installation

Execute the following in the root folder.

```bash
pip3 install -e .
```

#### To run

```bash
MasterCSS
```

or

```bash
python3 -m MasterCSS.cli
```

#### Uninstallation

```bash
pip3 uninstall MasterCSS
```



#### Note

- To add/remove dependency packages, please modify `install_requires` in `setup.py` then reinstall the app.



#### Code Structure

- `setup.py` is used for configuring `MasterCSS` package, including dependency packages, entry point, etc.
- In `src/MasterCSS/`:
  -  `controllers/` contains Flask REST API controllers.
  -  `models/` contains classes and db functions for all entities.
  - `static/` contains static files such as `.js`, `.css` , `favicon.ico`, etc. Files are categorised into folders.
  - `templates/` contains `.html` template files.
  - `auth.py` contains code for authentication (registration, login and logout).
  - `cli.py` contains Flask app initialisation code and also serves as **MasterCSS's entry point**.
  - `db.py` contains code to maintain db connection.

- Unit testing will be done in `tests/`.

