from setuptools import setup, find_packages

setup(
    name="MasterCSS",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    entry_points={"console_scripts": ["MasterCSS = MasterCSS.cli:main",],},
    install_requires=[
        "pytest",
        "flask",
        "requests",
        "oauthlib",
        "pyOpenSSL",
        "Flask-Login",
        "Flask-SQLAlchemy",
        "Flask-Marshmallow",
        "python-dotenv",
        "marshmallow-sqlalchemy",
        "mysql-connector",
        "pymysql",
        "geoalchemy2",
    ],
)
