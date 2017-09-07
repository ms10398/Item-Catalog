# Item Catalog

### Project Overview
> To Develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

### What Will I Learn?
  * Develop a RESTful web application using the Python framework Flask
  * Implementing third-party OAuth authentication.
  * Implementing CRUD (create, read, update and delete) operations.

### How to Run?

#### PreRequisites
  * [Python ~2.7](https://www.python.org/)
  * [Vagrant](https://www.vagrantup.com/)
  * [VirtualBox](https://www.virtualbox.org/)

#### Setup Project:
  1. Install Vagrant and VirtualBox
  2. Download or Clone [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository.
  3. Find the catalog folder and replace it with the content of the zip.

#### Launch Project
  1. Launch the Vagrant VM using command:

  ```
    $ vagrant up
  ```
  2. Run your application within the VM

  ```
    $ python /vagrant/catalog/database_setup.py
    $ python /vagrant/catalog/put_genre.py
    $ python /vagrant/catalog/main.py
  ```
  3. Access and test your application by visiting [http://localhost:5000](http://localhost:5000).
