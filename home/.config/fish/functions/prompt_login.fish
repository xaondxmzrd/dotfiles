# patch for /usr/share/fish/functions/prompt_login.fish

function prompt_login --description "display user name for the prompt"
    if not set -q __fish_machine
        set -g __fish_machine
        set -l debian_chroot $debian_chroot

        if test -r /etc/debian_chroot
            set debian_chroot (cat /etc/debian_chroot)
        end

        if set -q debian_chroot[1]
            and test -n "$debian_chroot"
            set -g __fish_machine "(chroot:$debian_chroot)"
        end
    end

    # Prepend the chroot environment if present
    if set -q __fish_machine[1]
        echo -n -s (set_color yellow) "$__fish_machine" (set_color normal) ' '
    end

    echo -n -s (set_color $fish_color_user) "$USER" (set_color normal)

    if set -q SSH_TTY
        echo -n -s @ (set_color $fish_color_host) (prompt_hostname)
    end

    echo -n -s (set_color normal)
end
