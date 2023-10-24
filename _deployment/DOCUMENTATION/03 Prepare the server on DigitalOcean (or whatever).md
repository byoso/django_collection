
## Be sure you have a ssh-key

- If you DO NOT already have an ssh-key on your local machine in `~/.ssh`, do

```sh
$ ssh-keygen
```
note: DO NOT DO IT IF YOU ALREADY HAVE ONE

- Register your key (`cat ~/.ssh/id_rsa.pub`) within your DigitalOcean project if not already done (settings->security).

## Create a new droplet (or server if not DigitalOcean)

Choose "docker on Ubuntu" as an OS on the 'Marketplace', and the size of server you want.

## Create a non-root user on the server

- then:

```sh
$ ssh root@<IP adress>
$ adduser <user>
$ usermod -aG sudo <user>
$ user -aG docker <user>
mkdir -p /home/<user>/.ssh
touch /home/<user>/.ssh/authorized_keys
nano /home/<user>/.ssh/authorized_keys
```

- open a second terminal and:
```sh
cat ~/.ssh/id_rsa.pub
```

- Copy/paste the output of this command in the nano editor of the distant terminal, save it,  and close this local terminal.

- In the distant terminal, still logged in:
```sh
exit
ssh <user>@<IP adress>
sudo apt update
sudo apt install docker-compose
sudo apt upgrade -y # may be long and ask a few default choices
```

You can now log in the server with ssh as a normal user :)

## Set the firewall of the server

```sh
sudo ufw app list
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

## Add a key for github

```sh
sudo ssh-keygen -t ed25519 -C "Github Deploy Key"
# then leave the default locations, and blank password (useless)
sudo cp /root/.ssh/id_ed25519.pub ~/.ssh/id_ed25519.pub
cat ~/.ssh/id_ed25519.pub
```

Copy the output, go in the github repository, "setting/deploy keys",  "+add a deploy key" paste the key, and name it.

## git clone

In git repository, copy the clone link

then on the server:

```sh
sudo git clone git@github.com:your/project...
cd <project folder>

sudo cp .env-sample .env
sudo nano .env
# edit the .env file
```

Read carefully each line of the .env file and set them up before going further.