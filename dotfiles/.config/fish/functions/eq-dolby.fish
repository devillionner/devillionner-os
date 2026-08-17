function eq-dolby
    printf "%s\n" "Dolby Atmos" > ~/.cache/ff-audio-preset
    command easyeffects -l "Dolby Atmos" >/dev/null 2>&1 &
    echo "🎬 Режим: Кіно / 3D Простір (Dolby Atmos)"
end
