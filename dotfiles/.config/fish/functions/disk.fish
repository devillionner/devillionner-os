function disk
    set -l info (df -h / | awk 'NR==2 {print $3; print $2; print $5; print $4}')
    echo (set_color magenta)"󰋊 Диск (Root): "(set_color cyan)$info[1](set_color normal)" / "$info[2]" "(set_color yellow)"("$info[3]")"(set_color normal)" — "(set_color green)"Вільно: "$info[4](set_color normal)
end
