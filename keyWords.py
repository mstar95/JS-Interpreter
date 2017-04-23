from tokenType import TokenType
keyWords = {
         "function": TokenType.Function,
         "if": TokenType.If,
         "else": TokenType.Else ,
         "return": TokenType.Return,
         "var": TokenType.Var,
         "String": TokenType.String
};

simpleSigns = {
        '(': TokenType.ParenthOpen,
        ')': TokenType.ParenthClose,
        '{': TokenType.BracketOpen,
        '}': TokenType.BracketClose,
        '[': TokenType.SquareBracketOpen,
        ']': TokenType.SquareBracketClose,
        ',': TokenType.Comma,
        ';': TokenType.Semicolon,
        '+': TokenType.Plus,
        '.': TokenType.Dot
};
