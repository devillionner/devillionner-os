function eq-sony
    printf "%s\n" "Sony / Harman" > ~/.cache/ff-audio-preset
    command easyeffects -l "Sony AutoEq Harman" >/dev/null 2>&1 &
    echo "🎧 Режим: Навушники Sony (Harman Target)"
end
