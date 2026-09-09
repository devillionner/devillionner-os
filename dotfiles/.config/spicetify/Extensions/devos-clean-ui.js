(() => {
    const STYLE_ID = "devos-spotify-clean-ui";
    const LUCID_KEY = "lucid:settings";
    const LUCID_MARKER = "devos:lucid-preset-v4";
    const RELOAD_GUARD = "devos:lucid-preset-reload-v1";

    const css = String.raw`
/*
 * Devillionner Spotify experience.
 * Cleanup selectors are curated from Spicetify Marketplace snippets
 * (spicetify/marketplace @ ec6f772891bad4bf08b645447c2ade6b06c4f991).
 * Lucid owns the main visual language; this layer only removes clutter and
 * adds Oneko as a progress companion without overriding Lucid's progress geometry.
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

/* Keep Spotify/Lucid's native fill untouched. Oneko is positioned by
 * Spotify's own --progress-bar-transform; sliderArea still clips only the fill.
 */
.player-controls .playback-progressbar .progress-bar,
.playback-bar .progress-bar {
    position: relative !important;
    overflow: visible !important;
}
.player-controls .playback-progressbar .progress-bar::after,
.playback-bar .progress-bar::after {
    content: '';
    position: absolute;
    width: 32px;
    height: 32px;
    left: var(--progress-bar-transform, 0%);
    top: 50%;
    transform: translate(-50%, -82%);
    image-rendering: pixelated;
    background-image: url('https://raw.githubusercontent.com/adryd325/oneko.js/14bab15a755d0e35cd4ae19c931d96d306f99f42/oneko.gif');
    pointer-events: none;
    z-index: 101;
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
                    show: false,
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
        applyLucidPreset();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", boot, { once: true });
    } else {
        boot();
    }
})();
