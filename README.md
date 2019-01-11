# Catalog Project

This project hosts a server and database that you connect to and can perform certain operations on.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### The database

The database has 2 tables, CATEGORIES and ITEMS.

Each row in CATEGORIES is a unique category with the primary key *id*

Each row in ITEMS is an item with the primary key *id* and the foreign key *cat_id*.

### Prerequisites

What things you need to install, the software and how to install them

You will need [Python](https://www.python.org/downloads/) installed.

I reccomend using [Vagrant](https://www.vagrantup.com/downloads.html) to use report.py  
If you are not using Linux you will need to install a virtual machine. I reccomend [VirtualBox](https://www.virtualbox.org)  

Once vagrant is downloaded and VirtualBox installed, put the report.py script into the vagrant directory. Then run these commands:

```
vagrant up
vagrant ssh
cd /vagrant
```
### Database

If the database is not working:

```
python database_setup.py
python lotsofcat.py
```
That will create the database and then populate it.

## Running


To run the server run this

```
python application.py
```
It should start the server

Then in your browser go to [localhost:8000](http://localhost:8000)

It should open a webpage you can interact with


## Authors

* **Aric Kuter** - *Everything*


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
