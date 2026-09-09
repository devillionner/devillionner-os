(() => {
    const STYLE_ID = "devos-spotify-clean-ui";
    const LUCID_KEY = "lucid:settings";
    const LUCID_MARKER = "devos:lucid-preset-v1";
    const RELOAD_GUARD = "devos:lucid-preset-reload-v1";

    const css = String.raw`
/*
 * Devillionner Spotify experience.
 * Cleanup selectors are curated from Spicetify Marketplace snippets
 * (spicetify/marketplace @ ec6f772891bad4bf08b645447c2ade6b06c4f991).
 * Lucid owns the main visual language; this layer only removes clutter and
 * adds the Caelestia-style wave progress + Oneko progress companion.
 */

/* Remove Popular shelves from Home. */
[data-testid='home-page'] .contentSpacing > [data-testid='component-shelf']:has(
    [href='/section/0JQ5DAuChZYPe9iDhh2mJz'],
    [href='/section/0JQ5DAnM3wGh0gz1MXnu4h'],
    [href='/section/0JQ5DAnM3wGh0gz1MXnu3B'],
    [href='/section/0JQ5DAnM3wGh0gz1MXnu3D']
) {
    display: none !important;
}

/* Hide Recently Played shortcuts/section. */
.view-homeShortcutsGrid-shortcuts,
section[aria-label='Recently played'] {
    display: none !important;
}

/* Hide Podcasts and What's New chrome. */
button[aria-label='Podcasts'],
[aria-label="What's New"] {
    display: none !important;
}

/* Hide Mini Player button. */
button:has(path[d='M16 2.45c0-.8-.65-1.45-1.45-1.45H1.45C.65 1 0 1.65 0 2.45v11.1C0 14.35.65 15 1.45 15h5.557v-1.5H1.5v-11h13V7H16V2.45z']),
button:has(path[d='M16 2.45c0-.8-.65-1.45-1.45-1.45H1.45C.65 1 0 1.65 0 2.45v11.1C0 14.35.65 15 1.45 15h5.557v-1.5H1.5v-11h13V7H16z']) {
    display: none !important;
}

/* Hide Spotify's fullscreen button; ivLyrics owns the useful fullscreen view. */
[data-testid="fullscreen-mode-button"] {
    display: none !important;
}

/* Hide Scroll through previews action on album/playlist pages. */
.main-actionBar-exploreButton {
    display: none !important;
}

/* Keep video available without giving it a giant text button. */
.dcSY8Zom_VXgK71Lbym_ {
    position: absolute;
    opacity: 0.4;
    transition: opacity 0.25s ease;
    z-index: 999;
}
.dcSY8Zom_VXgK71Lbym_:hover {
    opacity: 1;
}
.dcSY8Zom_VXgK71Lbym_ .encore-text {
    display: none;
}

/* Now Playing sidebar: keep artwork/queue/lyrics, remove artist + credits cards. */
.nw2W4ZMdICuBo08Tzxg9 {
    justify-content: center;
    height: 100%;
    width: 100%;
}
.main-nowPlayingView-section:not(.main-nowPlayingView-queue):not(.lyrics-npv-card) {
    display: none !important;
}

/* Caelestia-style wave progress bar. */
.player-controls .playback-progressbar {
    position: relative !important;
    overflow: visible !important;
}
.player-controls .playback-progressbar .x-progressBar-progressBarBg,
.player-controls .playback-progressbar .x-progressBar-fillColor,
.playback-bar .x-progressBar-progressBarBg,
.playback-bar .x-progressBar-fillColor {
    height: 10px !important;
    border-radius: 0 !important;
    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 10'%3E%3Cpath d='M0 5 C4.5 1 4.5 1 9 5 S13.5 9 18 5 S22.5 1 27 5 S31.5 9 36 5' fill='none' stroke='black' stroke-width='3' stroke-linecap='round'/%3E%3C/svg%3E");
    -webkit-mask-repeat: repeat-x;
    -webkit-mask-position: left center;
    -webkit-mask-size: 36px 10px;
    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 10'%3E%3Cpath d='M0 5 C4.5 1 4.5 1 9 5 S13.5 9 18 5 S22.5 1 27 5 S31.5 9 36 5' fill='none' stroke='black' stroke-width='3' stroke-linecap='round'/%3E%3C/svg%3E");
    mask-repeat: repeat-x;
    mask-position: left center;
    mask-size: 36px 10px;
}
.player-controls .playback-progressbar .x-progressBar-progressBarBg,
.playback-bar .x-progressBar-progressBarBg {
    background: rgba(var(--spice-rgb-text), 0.18) !important;
}
.player-controls .playback-progressbar .x-progressBar-fillColor,
.playback-bar .x-progressBar-fillColor {
    background: var(--spice-button-active, var(--spice-accent)) !important;
}
.player-controls .playback-progressbar .progress-bar__slider,
.playback-bar .progress-bar__slider {
    width: 10px !important;
    height: 10px !important;
    box-shadow: 0 0 0 2px rgba(var(--spice-rgb-main), 0.7), 0 0 12px rgba(var(--spice-rgb-button-active), 0.35) !important;
}

/* Oneko follows the actual playback position instead of sitting at a fixed edge. */
.player-controls .playback-progressbar::after {
    content: '';
    width: 32px;
    height: 32px;
    bottom: calc(100% - 7px);
    left: clamp(16px, var(--devos-spotify-progress, 0%), calc(100% - 16px));
    transform: translateX(-50%);
    position: absolute;
    image-rendering: pixelated;
    background-image: url('https://raw.githubusercontent.com/adryd325/oneko.js/14bab15a755d0e35cd4ae19c931d96d306f99f42/oneko.gif');
    pointer-events: none;
    z-index: 5;
    animation: devos-oneko 1s infinite;
}
@keyframes devos-oneko {
    0%, 50% { background-position: -64px 0; }
    50.0001%, 100% { background-position: -64px -32px; }
}
`;

    function installStyle() {
        if (document.getElementById(STYLE_ID)) return;
        const style = document.createElement("style");
        style.id = STYLE_ID;
        style.textContent = css;
        document.documentElement.appendChild(style);
    }

    function updateProgress() {
        try {
            const fraction = Number(Spicetify?.Player?.getProgressPercent?.());
            const pct = Number.isFinite(fraction) ? Math.max(0, Math.min(1, fraction)) * 100 : 0;
            document.documentElement.style.setProperty("--devos-spotify-progress", `${pct}%`);
        } catch {}
    }

    function startProgressTracking() {
        updateProgress();
        try {
            Spicetify.Player.addEventListener("onprogress", updateProgress);
            Spicetify.Player.addEventListener("songchange", updateProgress);
            Spicetify.Player.addEventListener("onplaypause", updateProgress);
        } catch {}
    }

    function applyLucidPreset() {
        try {
            const currentTheme = Spicetify?.Config?.current_theme;
            if (currentTheme && currentTheme !== "Lucid") return;
            if (localStorage.getItem(LUCID_MARKER) === "1") return;

            let persisted = {};
            try {
                persisted = JSON.parse(localStorage.getItem(LUCID_KEY) || "{}");
            } catch {
                persisted = {};
            }

            const state = persisted && typeof persisted.state === "object" && persisted.state
                ? persisted.state
                : {};

            state.page = {
                ...(state.page || {}),
                mode: "default",
                coverMode: "default",
                panelGap: 0,
            };
            state.player = {
                ...(state.player || {}),
                mode: "default",
                autoHide: false,
                isFloating: false,
                nextSongCard: {
                    ...(state.player?.nextSongCard || {}),
                    show: true,
                    isFloating: false,
                },
            };
            state.library = { ...(state.library || {}), autoHide: false };
            state.rightSidebar = {
                ...(state.rightSidebar || {}),
                mode: "default",
                autoHide: false,
            };
            state.globalNav = {
                ...(state.globalNav || {}),
                floating: false,
                autoHide: false,
            };
            state.color = {
                ...(state.color || {}),
                mode: "dynamic",
                isDark: true,
                isTinted: true,
            };

            localStorage.setItem(
                LUCID_KEY,
                JSON.stringify({ ...persisted, state, version: persisted.version ?? 1 }),
            );
            localStorage.setItem(LUCID_MARKER, "1");

            if (sessionStorage.getItem(RELOAD_GUARD) !== "1") {
                sessionStorage.setItem(RELOAD_GUARD, "1");
                setTimeout(() => location.reload(), 250);
            }
        } catch (error) {
            console.warn("[devos] Lucid preset could not be applied", error);
        }
    }

    function boot() {
        installStyle();
        startProgressTracking();
        applyLucidPreset();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", boot, { once: true });
    } else {
        boot();
    }
})();
