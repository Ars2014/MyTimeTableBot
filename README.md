# MyTimeTable
![Version: 0.2.2](https://img.shields.io/badge/version-0.2.2-brightgreen.svg?style=flat-square)  [![Roadmap](https://img.shields.io/badge/Roadmap-here-brightgreen.svg?style=flat-square)](https://trello.com/b/GuQeA6lF/mytimetable)
Telgram bot that saves your time and paper

## Dependencies
To install bot make sure you have this dependencies:
* Python (3.5 and above)
* RethinkDB 2.3(Fantasia)
* Nginx (ortional)
* Gunicorn (optional)


## Installing
1. Install RethinkDB. Create user and grant all permissions. [See RethinkDB wiki here](https://www.rethinkdb.com/).
2. Run `git clone https://github.com/Ars2014/MyTimeTableBot` to download latest version from GitHub.
3. Configure bot settings in `config.ini` file. [See examples here](https://github.com/Ars2014/MyTimeTableBot/tree/master/examples)*.
4. Create virtual environment with [`virtualenv`](https://virtualenv.pypa.io/en/stable/) and activate.
5. Install dependencies with `pip install -r requirements.txt`
6. (For webhook) Configure nginx. [See example here](https://github.com/Ars2014/MyTimeTableBot/blob/master/examples/nginx.conf)*.
7. (For webhook) Configure gunicorn. [See example here](https://github.com/Ars2014/MyTimeTableBot/blob/master/examples/gunicorn.conf.py)*.
8. Run bot with `python main.py`.
9. (Optional) Add bot to [supervisor](http://supervisord.org/) or [systemd](https://wiki.freedesktop.org/www/Software/systemd/)
\* - All examples from working project. Some lines changed for privacy.

### Special thanks to 
* My computer science teacher
* and others...
