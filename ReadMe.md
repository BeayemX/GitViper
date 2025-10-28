<p align="center">
    <img src="https://user-images.githubusercontent.com/3453076/35360877-8035c5b2-015f-11e8-8ab2-1d74e65e3cd5.png" alt="GitViper logo">
</p>

# Overview
GitViper is a tool to improve the experience when using Git with the command line by showing you the current state of the repository. This tool is designed to only display git related information. You can still work with Git and modify files the way you want.


# Installation
GitViper builds on top of Git, therefore it is required to have Git installed on your system. Just use your package manager to install Git. The command should look something along these lines:

```sh
sudo apt-get install git python3 python3-pip
sudo dnf install git python3 python3-pip
pip3 install -r requirements.txt

```

# Docker / Podman

```bash
podman build -t gitviper .                       # Build image
podman run -it --rm -v $(pwd):/repo:ro gitviper  # Run gitviper in the current directory
```

## Known issues
* `bash_aliases.sh` hasn't been updated yet to work with the container
* Autocompletion does not (yet?) work
* Config file in the home directory will be ignored as it is not accessible

# How to use GitViper
Check out the documentation on [how to](documentation/howto.md) use GitViper.


# Feedback and bugs
If you encounter bugs or want to request new features just open an issue.

General questions can also be asked in the [Project discussion issue](https://github.com/BeayemX/GitViper/issues/26).
