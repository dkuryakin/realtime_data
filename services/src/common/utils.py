def symbols(symbols_count: int, symbols_prefix: str):
    digits = len(str(symbols_count - 1))
    fmt = f"%0{digits}d"
    return [
        (symbols_prefix + fmt % i)
        for i in range(symbols_count)
    ]
