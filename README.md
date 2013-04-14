PINULTIMATE
---------------------------------------------------------------------------

* Username: puadmin
* Email: teampinultimate@gmail.com
* Github Password: pupassword123

## SSH to EC2:
```bash
ssh deploy@pinultimate.net
```
password: pinultimate

## DEPLOY to EC2:
First time setup:
```bash
git remote remove deploy
git remote add deploy ssh://deploy@pinultimate.net/home/deploy/pinultimate.git
```
Then, whenever you want to deploy:
```bash
git push deploy master
```
**Never deploy from any other branch other than master. The server will reject all non-fast-forward changes**

Finally, ssh into the server to restart Apache so the new changes to the code are now available to the webserver
```bash
sudo service apache2 restart
```

## SERVER-SIDE Development:

### Install Homebrew & PIP:
```bash
/usr/bin/ruby -e "$(/usr/bin/curl -fksSL https://raw.github.com/mxcl/homebrew/master/Library/Contributions/install_homebrew.rb)"
brew update
```
```bash
sudo easy_install pip
```

### Django SETUP:
```bash
pip install django
```

### MongoDB SETUP:
```bash
brew install mongodb
pip install pymongo
pip install mongoengine
```

### MYSQL SETUP:
1. INSTALL MYSQL:
```bash
brew install mysql
```
```bash
unset TMPDIR
```
```bash
mysql_install_db --verbose --user=`whoami` --basedir="$(brew --prefix mysql)" --datadir=/usr/local/var/mysql --tmpdir=/tmp
```
2. START MYSQL:
```bash
mysql.server start
```
3. STOP MYSQL:
```bash
mysql.server stop
```
4. INSTALL MYSQL DRIVER:
```
pip install MySQL-python
```
5. CREATE local pudev ACCOUNT:
```bash
mysql.server start
```
```bash
mysql -u root
```
6. INITIALIZE DATABASE
```sql
CREATE DATABASE HEATMAPDB;
CREATE USER 'pudevs'@'localhost' IDENTIFIED BY 'pukey';
GRANT ALL ON HEATMAPDB.* TO 'pudevs'@'localhost';
```
