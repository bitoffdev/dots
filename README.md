# Bit Off Dots

I use [dotdrop][dotdrop] to manage my dotfiles.

## Getting Started

*Note: Unless stated otherwise, all command listed below should be run in the
root directory of this repository*

- Install packages listed in  [required packages](#required-packages) below
- Clone this repo into `$HOME/.dots`
- Install base16 schemes by running `python3 lib/base16/main.py download`
- Run `dotdrop install` in the root directory of this repo.

## Ideology

- Configurations should be idempotent.
- Configurations should be declarative, not procedural.
- Configurations should be done at the lowest level where they can be done in
  full.
    - Corollary: Shell colors should be set using ANSI colors
      wherever possible, not in the terminal-emulator configuration.
      This will mean that colors even work in ttys.

## Required packages

APT

```bash
apt-get install bspwm compton dunst feh python3 python3-pip shellex sxhkd rxvt-unicode xbacklight xinit xclip xcursor-themes
```

Python

```bash
pip3 install --user dotdrop pystache pyyaml
```

## Recommendations

### APT

```bash
apt-get install acpi alsa-utils arandr arp-scan curl dnsutils deluge dia evince flatpak git htop libnotify-bin lm-sensors neovim net-tools network-manager-gnome nmap nodejs npm openvpn parcellite pavucontrol pktstat rclone snapd sxiv texlive-full tmux traceroute tree whois vlc wireshark zathura
```

### Flatpak

```bash
flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

flatpak install --user flathub com.discordapp.Discord com.getpostman.Postman com.spotify.Client com.valvesoftware.Steam org.inkscape.Inkscape org.telegram.desktop
```

### OpenRCT

Install [OpenRCT 2][openrct2] to the `/opt/OpenRCT2` directory.

### Python

```bash
pip3 install --user flake8 pynvim
```

### Slack

- Sidebar themes: https://slackthemes.net

### Thunderbird

Install thunderbird into `/opt` directly from Mozilla. The `thunderbird`
package from APT and other package managers tends to be out of date.

**Add-ons**

- [DKIM verifier][dkimverifier]
- [Expression Search][expressionsearch]
- [Monterail Dark][monteraildark] by [Emanuele Concas][conema]

[conema]: https://github.com/conema
[dkimverifier]: https://addons.thunderbird.net/en-US/thunderbird/addon/dkim-verifier
[dotdrop]: https://github.com/deadc0de6/dotdrop
[expressionsearch]: https://addons.thunderbird.net/en-US/thunderbird/addon/gmailui/
[monterail]: https://addons.thunderbird.net/en-US/thunderbird/collections/conema/monterail-themes/
[monteraildark]: https://addons.thunderbird.net/en-US/thunderbird/addon/monterail-dark
[openrct2]: https://openrct2.org/
