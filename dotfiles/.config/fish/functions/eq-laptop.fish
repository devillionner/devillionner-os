function eq-laptop
    printf "%s\n" "Zenbook / Laptop" > ~/.cache/ff-audio-preset
    command easyeffects -l "Laptop" >/dev/null 2>&1 &
    echo "🔊 Режим: Динаміки Zenbook (Laptop Master)"
end
