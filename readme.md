# Flask Template

Welcome to Flask Template! Use this template to start your project. Let's get started!

## Getting Started

- [Flask Template](#flask-template)
  - [Getting Started](#getting-started)
  - [Project Structure](#project-structure)
    - [`src/database` Folder](#srcdatabase-folder)
      - [`database.py`](#databasepy)
    - [`src/general` Folder](#srcgeneral-folder)
    - [`src/routes` Folder](#srcroutes-folder)
    - [`.env` File](#env-file)
  - [Install Dependencies](#install-dependencies)
    - [MACOS and Linux](#macos-and-linux)
    - [Windows](#windows)
  - [Author](#author)

## Project Structure

```plain
├── 📂 src
|   ├── 📁 database
|   |   ├── 📄 __init__.py
|   |   ├── 📄 database.py
|   |   └── 📁 models
|   |       ├── 📄 base.py
|   |       └── 📄 example.py
|   |   
|   ├── 📁 general
|   |   ├── 📄 __init__.py
|   |   └── 📄 post_put_decorator.py
|   |
|   └── 📁 routes
|       ├── 📄 __init__.py
|       └── 📄 example_routes.py
|
├── 📄 main.py
├── 📄 .env.example
└── 📄 requirements.txt
```

### `src/database` Folder

This folder contains all the scripts related to the database. In `base.py` is the declarative_base from sqlalchemy from here it should be imported to the models.

All other files here should be inside the models folder to represent the models of the tables. This classes should implement the method `serialize`.

```python
def serialize(self):
    """
    Serialize the data

    Returns:
        dict: The serialized data
    """
```

#### `database.py`

This script  contains the class to interact with the database. It handles the connection and the queries to the database. 

The script needs all the models to be imported and stored in the `TABLE_CLASS_MAP` with the table name as the key and the class as the value.

```python
from .example import Example

TABLE_CLASS_MAP = {
    'examples': Example,
}
```

To use the database in any script you need to import it from the database module.

```python
from app.database import database

# Use database here
```

### `src/general` Folder

This folder contains all the scripts used for a general purpose. 

In `post_put_decorator.py` is the post_put_decorator from here it should be imported to the routes.

It also has the base URI to be used in the routes and instantiates the database which should be imported to the routes.

### `src/routes` Folder

This folder contains all the routes. In the script `example_routes.py` is the basic example on how to create routes using the blueprint.

Once you have the routes created you need to import the blueprint in the `__init__.py` and add it to the `__all__` list. After that you need to import the blueprint in the `app.py` and add it to the `app` list.

```python
from src.routes import example_bp

app.register_blueprint(example_bp)
```

### `.env` File

The app uses an `.env` to store database credentials, and the JWT secret key. You will need to copy the `.env.example` file to `.env` and fill in the credentials.

---

## Install Dependencies

I recommend using an virtual environment. But if you don't want to create one, you skip to the dependencies installation. You can create one using the following command:

```bash
python -m venv {your_venv_name}
```

Then depending on your OS you can install the dependencies using the following command:

### MACOS and Linux 

```bash
source {your_venv_name}/bin/activate
```

### Windows
```cmd
{your_venv_name}\Scripts\activate
```

Once the virtual environment is activated you can install the dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Author 
🧇 [@C4ncino](https://github.com/C4ncino) 🧇
