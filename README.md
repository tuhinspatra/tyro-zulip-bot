
<p align="center"><a href="https://github.com/armag-pro/tyro-zulip-bot" target="_blank" rel="noopener noreferrer"><img width="300" src="https://github.com/armag-pro/tyro-zulip-bot/blob/master/assets/logo.png" alt="tryo Bot logo"></a></p>


<p align="center">
<a href="https://github.com/armag-pro/tyro-zulip-bot">
    <img src="https://img.shields.io/badge/version-1.1-blue.svg" alt="version 1.1">
</a>
<a href="https://github.com/armag-pro/tyro-zulip-bot/pulls">
    <img src="https://img.shields.io/badge/PRs-Welome-brightgreen.svg" alt="PRs Welcome">
</a>
<a href="https://github.com/armag-pro/tyro-zulip-bot/blob/master/LICENSE">
    <img src="https://img.shields.io/apm/l/vim-mode.svg" alt="License MIT">
</a>
</p>

<p align="center">
<a href="https://github.com/ellerbrock/open-source-badge/">
    <img src="https://badges.frapsoft.com/os/v1/open-source.svg?v=103" alt="Open Source Love">
</a>
</p>



> Fun and fruitful AI bot for zulip chat.


**tyro** is a educational bot built on the zulip platform, powered by Google's dialogflow NLU, packed with simple AI games and dozens of other weird abilities.

__Note: Dialogflow Intent matching is not implemented for all commands but can be done.__

## Get Started
You need to setup a google service account for the Dialogflow API to work. Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the downloaded json file.

If you are behind a proxy and get service limit exceeded error set the https_proxy same as http_proxy.

* Go to your Zulip account and  add a bot. Use Generic bot as the bot type.
* Download the bot's zuliprc configuration file to your computer.
* Download the zulip_bots Python package to your computer using pip install zulip_bots.
* Start the bot process on your computer.
Run  `zulip-run-bot ~/path/to/botname.py --config-file ~/path/to/zuliprc`.

* Check the output of the command. It should include the following line:

```
INFO:root:starting message handling...
Congrats! Your bot is running.
```

 To talk with the bot, at-mention its name, like `@**bot-name**`.

## Screenshots
### AI Smalltalk
Engage in general human talk.

![Smalltalk](https://github.com/armag-pro/tyro-zulip-bot/blob/master/assets/smalltalk.png "Smalltalk")

### Explain
Ask the bot to explain.
![Explain](https://github.com/armag-pro/tyro-zulip-bot/blob/master/assets/explain.png "Explain")

### Evaluate
Evaluate chain of mathermatical equations.
![evaluate](https://github.com/armag-pro/tyro-zulip-bot/blob/master/assets/evaluate.png "evaluate")

### code
Get your code output.
![Code](https://github.com/armag-pro/tyro-zulip-bot/blob/master/assets/code.png "Code")

### Personal Instagram quiz
Code based on your instagram pictures and AI.
![Instaquiz](https://github.com/armag-pro/tyro-zulip-bot/blob/master/assets/instaquiz.png "Instaquiz")


### Quiz
![Quiz](https://github.com/armag-pro/tyro-zulip-bot/blob/master/assets/quiz.png "quiz")

### Facts
Confirm a fact.
![Facts](https://github.com/armag-pro/tyro-zulip-bot/blob/master/assets/tellme.png "Facts")

### Contests
![Contests](https://github.com/armag-pro/tyro-zulip-bot/blob/master/assets/contests.png "Contests")

### Stackoverflow
![Stackoverflow](https://github.com/armag-pro/tyro-zulip-bot/blob/master/assets/stackoverflow.png "Stackoverflow")

## Contributors
* **Tuhin Subhra Patra** - [armag-pro](https://github.com/armag-pro)
* **Bavishi Milan** - [jarvisdev](https://github.com/jarvisdev)
* **Jugta Ram** - [jugtaram](https://github.com/jugtaram)

## License
[MIT](http://opensource.org/licenses/MIT)

Certain resources(icons, images, etc) require attribution.


Copyright (c) 2018-present, **Team SacredHacks**.
