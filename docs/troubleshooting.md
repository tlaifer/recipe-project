
### MongoDB
- check status of mongo db
```bash
sudo systemctl status mongod
```
- restart mongo
```bash
sudo systemctl stop mongod
sudo systemctl start mongod
```
- if you can't figure out why mongo won't start try rebooting. the system:
```bash
sudo reboot
```

### Out of disk space? 
It's posible the VM runs out of space in certain directories. For example when trying to install node.js I saw:
```bash
Insufficient space in download directory /var/cache/yum/x86_64/7/centos-7-updates
    * free   768 k
    * needed 6.5 M
```

Investigating this I noticed the /var/spool directory was eating up memory
```bash
[tlaifer2@sp21-cs411-13 /]$ sudo du -h /var/* | sort -rh | head -10
3.2G    /var/spool/abrt/ccpp-2021-03-14-16:00:52-32698
3.2G    /var/spool/abrt
3.2G    /var/spool
518M    /var/lib
302M    /var/lib/mongo
300M    /var/lib/mongo/journal
286M    /var/cache
284M    /var/cache/yum/x86_64/7
284M    /var/cache/yum/x86_64
284M    /var/cache/yum
```

We can delete this with:
```bash
[tlaifer2@sp21-cs411-13 /]$ sudo abrt-cli rm /var/spool/abrt/ccpp-2021-03-14-16:00:52-32698
rm '/var/spool/abrt/ccpp-2021-03-14-16:00:52-32698'
```
