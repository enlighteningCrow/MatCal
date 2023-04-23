from types import SimpleNamespace


class Theme:
    def __init__(self,
                 name,
                 FG,
                 BG,
                 BG2,
                 RED,
                 GREEN,
                 YELLOW,
                 BLUE,
                 PURPLE,
                 AQUA,
                 ORANGE
                 ):
        self.FG = FG
        self.BG = BG
        self.BG2 = BG2
        self.RED = RED
        self.GREEN = GREEN
        self.YELLOW = YELLOW
        self.BLUE = BLUE
        self.PURPLE = PURPLE
        self.AQUA = AQUA
        self.ORANGE = ORANGE
        self.name = name
        self.makeTheme()

    def makeTheme(self):
        theme = self
        result = f"""
        /* Set default styles for various widgets */
        QWidget {{
            color: {theme.FG};
            background-color: {theme.BG};
        }}

        QLabel {{
            background-color: transparent;
        }}

        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {theme.BG2};
            border: 1px solid {theme.BG2};
        }}

        QPushButton {{
            background-color: {theme.BG2};
            border: 1px solid {theme.BG2};
            padding: 5px 10px;
        }}

        QPushButton:hover, QPushButton:focus {{
            background-color: {theme.BG};
            border-color: {theme.BLUE};
        }}

        QMenuBar {{
            background-color: {theme.BG2};
        }}

        QMenuBar::item {{
            padding: 5px 10px;
            background-color: {theme.BG2};
            color: {theme.FG};
        }}

        QMenuBar::item:selected, QMenuBar::item:pressed {{
            background-color: {theme.BG};
            color: {theme.BLUE};
        }}

        QMenu {{
            background-color: {theme.BG2};
            border: 1px solid {theme.BG2};
        }}

        QMenu::item {{
            padding: 5px 10px;
            background-color: {theme.BG2};
            color: {theme.FG};
        }}

        QMenu::item:selected, QMenu::item:pressed {{
            background-color: {theme.BG};
            color: {theme.BLUE};
        }}

        QScrollBar {{
            background-color: {theme.BG2};
            border: 1px solid {theme.BG2};
        }}

        QScrollBar::handle {{
            background-color: {theme.BG};
        }}

        QScrollBar::handle:hover, QScrollBar::handle:focus {{
            background-color: {theme.BLUE};
        }}

        QScrollBar::add-page, QScrollBar::sub-page {{
            background-color: transparent;
        }}

        QScrollBar::add-line, QScrollBar::sub-line {{
            background-color: {theme.BG2};
            border: 1px solid {theme.BG2};
        }}

        QScrollBar::add-line:hover, QScrollBar::sub-line:hover {{
            background-color: {theme.BG};
            border-color: {theme.BLUE};
        }}

        QScrollBar::add-line:pressed, QScrollBar::sub-line:pressed {{
            background-color: {theme.BLUE};
            border-color: {theme.BLUE};
        }}

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 16px;
            height: 16px;
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            width: 16px;
            height: 16px;
        }}
        """
        with open("resources/themes/" + theme.name + ".qss", "w") as f:
            f.write(result)


# Theme(
#     "gruvboxDark",
#     FG="#ebdbb2",
#     BG="#282828",
#     BG2="#3c3836",
#     RED="#cc241d",
#     GREEN="#98971a",
#     YELLOW="#d79921",
#     BLUE="#458588",
#     PURPLE="#b16286",
#     AQUA="#689d6a",
#     ORANGE="#d65d0e"
# )


# TODO: Move back the theme_manual with a different name

themes = [
    Theme("gruvbox", "#ebdbb2", "#282828", "#3c3836", "#cc241d",
          "#98971a", "#d79921", "#458588", "#b16286", "#689d6a", "#d65d0e"),
    Theme("vscode-dark-plus", "#d4d4d4", "#1e1e1e", "#252526", "#f48771",
          "#c5e478", "#fac863", "#6fc1ff", "#dcbdfb", "#c2c080", "#d19a66"),
    Theme("ayu-dark", "#f0f0f0", "#0e1011", "#181a1f", "#ff6188",
          "#a9dc76", "#ffd866", "#78dce8", "#ab9df2", "#ffeead", "#fc9867"),
    Theme("nord", "#d8dee9", "#2e3440", "#3b4252", "#bf616a", "#a3be8c",
          "#ebcb8b", "#81a1c1", "#b48ead", "#88c0d0", "#d08770"),
    Theme("dracula", "#f8f8f2", "#282a36", "#44475a", "#ff5555",
          "#50fa7b", "#f1fa8c", "#bd93f9", "#ff79c6", "#8be9fd", "#ffb86c"),
    Theme("monokai", "#f8f8f2", "#272822", "#3e3d32", "#f92672",
          "#a6e22e", "#e6db74", "#66d9ef", "#ae81ff", "#a1efe4", "#fd971f"),
    Theme("one-dark", "#abb2bf", "#282c34", "#2c313a", "#e06c75",
          "#98c379", "#e5c07b", "#61afef", "#c678dd", "#56b6c2", "#d19a66"),
    Theme("tokyonight", "#c0caf5", "#1a1b26", "#21233d", "#f7768e",
          "#9ece6a", "#e0af68", "#7aa2f7", "#bb9af7", "#7dcfff", "#ff9e64")
]
