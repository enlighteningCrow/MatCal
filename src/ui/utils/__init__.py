def setMaxWidth(widg, table):
    margins = widg.layout().contentsMargins()
    widg.setMaximumWidth(
        table.horizontalHeader().length() + table.verticalHeader().width() +
        table.frameWidth() * 2 + margins.left() + margins.right() + 6 + (
            table.verticalScrollBar().width() if table.verticalScrollBar().
            isVisible() else 0
        )
    )