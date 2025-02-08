from render import (
        renderDeletePage,
        renderMergePage,
        renderRotatePage,
        renderSplitPage
)

backgroundColor = "#161616"
foregroundColor = "#FFFFFF"
borderColor = "#3B3B3B"
hoverColor = "#3A3A3A"
buttonColor = "#0F3180"
entryColor = "#ACACAC"

fontFamily = "Bahnschrift Light"

eventMap = {
    0 : renderMergePage,
    1 : renderSplitPage,
    2 : renderDeletePage,
    3 : renderRotatePage
}
