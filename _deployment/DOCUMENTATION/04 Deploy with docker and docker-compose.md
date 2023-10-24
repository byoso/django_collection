## Ressources
[Video 01 - overhaul](https://www.youtube.com/watch?v=mScd-Pc_pX0)
[Video 02 - SSL certificate](https://www.youtube.com/watch?v=3_ZJWlf25bY&t=3204s)
[same with text](https://londonappdeveloper.com/django-docker-deployment-with-https-using-letsencrypt/)

## build the docker images


```sh
# get the initial ssl certifcate
docker-compose -f docker-compose.prod.yml run --rm certbot /opt/certify-init.sh
# Waiting for nginx to be available... can appear for a while, don't worry, just wait a little.

# then down
docker-compose -f docker-compose.prod.yml down
# and re-up for good
docker-compose -f docker-compose.prod.yml up -d

```

## CRON automatic certificate renewal

### manual renewal

For now, the certificate can be manually renewed with:

```sh
docker-compose -f docker-compose.prod.yml run --rm certbot sh -c "certbot renew"
```

### CRON renewal

We want the certificate to automatically renew, so, we'll make a cron for that.

In the /home directory of the server (where you can find your main code directory), create a new file: 'renew.sh'

**renew.sh**

*replace {docker-compose place} by the place given by `whereis docker-compose` (example: /usr/bin/docker-compose)**

```sh
#! /bin/sh

set -e

echo "$(date): Tried to launch renew.sh script from cron..." >> /home/<user>/logs

cd /home/<user>/<project folder>

# do: 'whereis docker-compose' to have the right path to docker-compose
/usr/bin/docker-compose -f docker-compose.prod.yml run --rm certbot certbot renew

# add a trace to logs
echo "$(date): SSL certificate renewe successfully" >> /home/byoso/logs


```

Make sure it is executable: `sudo chmod +x renew.sh`

Try if it works: `./renew.sh`


then create a crontab (as normal user, not sudo):
```sh
crontab -e
```

register this line:

```sh
0 0 * * 6 sh /home/<user>/renew.sh
```
*0 0 * * 6  means:  every saturday at midnight* ([crontab.guru here](https://crontab.guru))
