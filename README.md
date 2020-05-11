# NFFS_PygameMySQL
A trivial Python Game using the Pygame library with a MySQL database for Leaderboards/Rankings.

Steps:

1] Download and install xampp: https://www.apachefriends.org/download.html

2] Create database 'gameboard' with table 'user_info' having columns (name,score). You can do this by running Apache and Mysql in Xampp, then  going to 'localhost/phpmyadmin' in your browser and executing the following queries.
  create database
  create table user_info(name VARCHAR(20), scoreVARCHAR(20))
  
3] Run: pip install -r requirements.txt in your shell

4] Run NNFS.py

References:
https://pythonprogramming.net/pygame-python-3-part-1-intro/
