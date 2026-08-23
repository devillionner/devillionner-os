# YouTube Music — manual setup

The custom Better Lyrics theme is stored in:

`assets/better-lyrics/blyrics-theme.rics`

## First setup

Update the Blueprint and launch a separate Helium profile for YouTube Music:

```bash
cd ~/devillionner-os && git pull --ff-only
helium-browser --user-data-dir="$HOME/.config/ytm-isolated" --app=https://music.youtube.com
```

Then, once in the opened YouTube Music profile:

1. If Helium shows first-run setup, choose **Use defaults**.
2. Install **Better Lyrics** from the Chrome Web Store.
3. Open Better Lyrics settings and import the theme file:
   `~/devillionner-os/assets/better-lyrics/blyrics-theme.rics`
4. Restart the YouTube Music window.

## Next launches

Use the same isolated profile:

```bash
helium-browser --user-data-dir="$HOME/.config/ytm-isolated" --app=https://music.youtube.com
```

The profile is kept in `~/.config/ytm-isolated`, so Better Lyrics and its settings persist between launches.
