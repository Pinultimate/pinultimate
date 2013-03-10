PINULTIMATE
---------------------------------------------------------------------------
Team GitHub Account:
Username: puadmin
Email: teampinultimate@gmail.com
Password: pupassword123
---------------------------------------------------------------------------
SSH to EC2:
1. git pull to obtain ./ec2/pinultimatekey.pem
2. sudo chmod 600 ./ec2/pinultimatekey.pem
3. ssh -i ./ec2/pinultimatekey.pem ec2-user@ec2-54-241-230-239.us-west-1.compute.amazonaws.com
----OR----
ssh puadmin@ec2-54-241-230-239.us-west-1.compute.amazonaws.com
with password: pukey
---------------------------------------------------------------------------
PUSH to EC2:
> git push deploy master
CHECKOUT Code on EC2:
> cd ~/source.git
> GIT_WORK_TREE=/home/puadmin/source git checkout -f
---------------------------------------------------------------------------
SERVER-SIDE Development:
1. INSTALL MYSQL:
> brew install mysql
> unset TMPDIR
> mysql_install_db --verbose --user=`whoami` --basedir="$(brew --prefix mysql)" --datadir=/usr/local/var/mysql --tmpdir=/tmp
2. START MYSQL:
> mysql.server start
3. STOP MYSQL:
> mysql.server stop
4. INSTALL MYSQL DRIVER:
> pip install MySQL-python
5. CREATE local pudev ACCOUNT:
> mysql.server start
> mysql -u root
>> CREATE DATABASE HEATMAPDB;
>> CREATE USER 'pudevs'@'localhost' IDENTIFIED BY 'pukey';
>> GRANT ALL ON HEATMAPDB.* TO 'pudevs'@'localhost';