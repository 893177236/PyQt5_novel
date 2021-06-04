from PyQt5.Qt import QSyntaxHighlighter, QRegExp, QBrush, QColor, QFont, QTextCharFormat, Qt


class UserRuleHighLight(QSyntaxHighlighter):
    def __init__(self, parent,keywords:list):
        super(UserRuleHighLight, self).__init__(parent)
        specialConstant = QTextCharFormat()
        self.highlightingRules = []
        # specialConstant
        brush_foreground = QBrush(Qt.white, Qt.SolidPattern)
        brush_background = QBrush(QColor("#f26c4f"))
        specialConstant.setForeground(brush_foreground)
        specialConstant.setBackground(brush_background)
        specialConstant.setFont(QFont("Microsoft YaHei", 10))

        # keywords = ["f'{searchName_}'", "{bookid}"]
        for word in keywords:
            pattern = QRegExp(word)
            rule = UserRuleHighlightingRule(pattern, specialConstant)
            self.highlightingRules.append(rule)

    def highlightBlock(self, text: str):
        for rule in self.highlightingRules:
            expression = QRegExp(rule.pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, rule.format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)


class UserRuleHighlightingRule:
    def __init__(self, pattern, format):
        self.pattern = pattern
        self.format = format
