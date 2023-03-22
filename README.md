# Pancake
Basic wrapper for Flatpak's command-line tool with the added functionality of managing run scripts.

## Usage
Multiple of the following flags can be placed in one command (ex: pancake -su discord), however some will conflict (i.e. installing and uninstalling).

`-h` `--help` - Prints the list of commands that can be run with pancake.<br>
`-l` `--symlinks` - TODO: Temporarily prints out a list of installed apps, behavior will change during a later update.<br>
`-q <package>` `--query <package>` - Searches for the given package online.<br>
`-r [packages]` `--remove [packages]` `--uninstall [packages]` - Uninstalls the list of packages specified after the flag.<br>
`-s [packages]` `--install [packages]` - Installs the list of packages specified after the flag.<br>
`-u` `--update` - Updates all installed packages.<br>
`-V` `--version` - Prints the currently installed version of pancake.<br>

## License
This work is dual-licensed under GPL Version 2 and GPL Version 3. You may choose between these licenses on a case-by-case basis.

