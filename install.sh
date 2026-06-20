#!/bin/bash

# Install python-nautilus
echo "Installing python-nautilus..."
if type "pacman" > /dev/null 2>&1
then
    # check if already install, else install
    pacman -Qi python-nautilus &> /dev/null
    if [ `echo $?` -eq 1 ]
    then
        sudo pacman -S --noconfirm python-nautilus
    else
        echo "python-nautilus is already installed"
    fi
elif type "apt-get" > /dev/null 2>&1
then
    # Find Ubuntu python-nautilus package
    package_name="python-nautilus"
    found_package=$(apt-cache search --names-only $package_name)
    if [ -z "$found_package" ]
    then
        package_name="python3-nautilus"
    fi

    # Check if the package needs to be installed and install it
    installed=$(apt list --installed $package_name -qq 2> /dev/null)
    if [ -z "$installed" ]
    then
        sudo apt-get install -y $package_name
    else
        echo "$package_name is already installed."
    fi
elif type "dnf" > /dev/null 2>&1
then
    installed=`dnf list --installed nautilus-python 2> /dev/null`
    if [ -z "$installed" ]
    then
        sudo dnf install -y nautilus-python
    else
        echo "nautilus-python is already installed."
    fi
else
    echo "Failed to find python-nautilus, please install it manually."
fi

# Prompt user for editors to enable
echo "--------------------------------------------------"
echo "Configure editors to enable in Nautilus context menu:"
enabled_editors=()

read -p "Enable VS Code? (Y/n): " ans_vscode < /dev/tty
if [[ -z "$ans_vscode" || "$ans_vscode" =~ ^[Yy]$ || "$ans_vscode" =~ ^[Yy][Ee][Ss]$ ]]; then
    enabled_editors+=("VSCode")
fi

read -p "Enable Antigravity IDE? (Y/n): " ans_anti < /dev/tty
if [[ -z "$ans_anti" || "$ans_anti" =~ ^[Yy]$ || "$ans_anti" =~ ^[Yy][Ee][Ss]$ ]]; then
    enabled_editors+=("Antigravity")
fi

read -p "Enable Cursor? (Y/n): " ans_cursor < /dev/tty
if [[ -z "$ans_cursor" || "$ans_cursor" =~ ^[Yy]$ || "$ans_cursor" =~ ^[Yy][Ee][Ss]$ ]]; then
    enabled_editors+=("Cursor")
fi

# Write config JSON
mkdir -p ~/.config/code-nautilus
json_content="{\"enabled_editors\": ["
first=true
for ed in "${enabled_editors[@]}"; do
    if [ "$first" = true ]; then
        first=false
    else
        json_content="$json_content, "
    fi
    json_content="$json_content\"$ed\""
done
json_content="$json_content]}"

echo "$json_content" > ~/.config/code-nautilus/config.json
echo "Saved configuration to ~/.config/code-nautilus/config.json"
echo "--------------------------------------------------"

# Remove previous version and setup folder
echo "Removing previous version (if found)..."
mkdir -p ~/.local/share/nautilus-python/extensions
rm -f ~/.local/share/nautilus-python/extensions/VSCodeExtension.py
rm -f ~/.local/share/nautilus-python/extensions/code-nautilus.py

# Install the extension file
if [ -f "./code-nautilus.py" ]; then
    echo "Installing local version of the extension..."
    cp ./code-nautilus.py ~/.local/share/nautilus-python/extensions/code-nautilus.py
else
    echo "Downloading newest version from fork..."
    wget -q -O ~/.local/share/nautilus-python/extensions/code-nautilus.py https://raw.githubusercontent.com/matheussesso/code-nautilus/master/code-nautilus.py
fi

# Restart nautilus
echo "Restarting nautilus..."
nautilus -q

echo "Installation Complete"

