# github-activity

The GitHub User Activity CLI is a no nonsense, low resource tool to retrieve data on commits, open issues, and starred repos.

## Table of Contents

[Features](#features)
[Requirements](#requirements)
[Installation](#installation)


## Features

* Retrieve recent events with just the user's name
* Filter output with "limit" and "commit" flags
* Filter output with starred, events, and issues commands

## Requirements

* Python 3

## Installation

1. Clone the repository

```bash
https://github.com/Erik-Rhoden/github-activity.git
```

2. Navigate to directory

```bash
cd github-activity
```

3. Symlink command, if desired
```bash
chmod +x ~/github-activity/main.py
ln -s ~/github-activity/main.py ~/.local/bin/github-cli
```

4. Base command
```bash
github-cli events <username>
```

or (no symlinkj)
```bash
python3 main.py events <username>
```

5. Need help?
```bash
github-cli -h
```

or (no symlink)
```bash
python3 main.py -h
```

