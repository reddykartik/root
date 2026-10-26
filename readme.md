root
---

Taking the [DataTalks Machine Learning ZoomCamp](https://github.com/DataTalksClub/machine-learning-zoomcamp)

1. Setting up the local development
```bash
# install nix package manager
sudo dnf install nix
# enable flakes 
# edit /etc/nix/nix.conf 
experimental-features = nix-command flakes

# start the development shell
nix develop
```
