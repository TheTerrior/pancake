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

## Documentation
Pancake works by searching the best matching packages via flatpak, and during installation it will generate executable scripts in either /usr/local/bin or ~/.config/pancake/bin (this behavior can be specified in the config). If the directory is added to the PATH environment variable, the user can simply run this script in a user-friendly manner, i.e. running 'discord' instead of 'flatpak run com.discordapp.Discord'. If the user removes a package, pancake will check if a run script existed for that package, and will remove it.

Because these scripts could conflict with system binaries, the default location of these scripts is set to ~/.config/pancake/bin. Pancake keeps track of active scripts in its ~/.config/pancake/symlinksrc file, which the user can add and remove entries from manually, however any custom formatting and comments will be reset when pancake runs. This file is only meant to be edited when the user has manually added or removed a script without pancake having been aware of such change. This may be necessary when 'pancake -s' finds the wrong package. This obstacle will be addressed in future updates.

## License
This work is dual-licensed under GPL Version 2 and GPL Version 3. You may choose between these licenses on a case-by-case basis.

