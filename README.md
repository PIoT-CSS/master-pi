## Car Share System (CSS): Master Pi

#### Recommend: making virutal environment

```bash
python3 -m venv venv
. venv/bin/activate
```

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
  - `cli.py` contains Flask app initialisation code and configs, **also serves as MasterCSS's entry point**.

- Unit testing will be done in `tests/`.

