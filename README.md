<h1 align="center" id="title">Spotify Music Downloader Telegram Bot</h1>

<p align="center"><img src="https://socialify.git.ci/dog1912/Spotify-Music-Downloader-Telegram-Bot/image?language=1&amp;owner=1&amp;name=1&amp;stargazers=1&amp;theme=Light" alt="project-image"></p>

<p id="description">This is a project that allows you to download music from Spotify via Telegram. This repository was created and tested on Python3.10 and Ubuntu 22.04.3 LTS </p>

<h2>🛠️ Installation Steps:</h2>

<p>1. Download the necessary files or clone this project anywhere</p>

```
git clone https://github.com/dog1912/Spotify-Music-Downloader-Telegram-Bot.git
```
<p>2. Сhange paramener to config.json</p>

- YOUR PASSWORD - This is your password for authorisation. This bot isn't public because the api has a restriction.
- API_TOKEN - You can generate with [BotFather](https://t.me/BotFather)
- SPOTIFY_CLIENT_ID - [Spofify for developers](https://developer.spotify.com/dashboard)
- SPOTIFY_CLIENT_SECRET - [Spofify for developers](https://developer.spotify.com/dashboard)
<p>3. Setup a python script as a service through systemctl/systemd </p>

<p>vi /etc/systemd/system/telegram_bot.service (name of the service which is test in this case) </p>

```
[Unit]
Description=Spotify Music Downloader Telegram Bot
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 bot.py
Restart=always
  
[Install]
WantedBy=multi-user.target
```
<p>5. You need to reload the daemon </p>

```
systemctl daemon-reload
```

<p>6. To start a service at boot, use the enable command </p>

```
systemctl enable telegram_bot.service
```

<h2>💖Like my work?</h2>

Feel free to send bug reports and feature requests. If you are using this solution in production please tell me to know it's being useful.
