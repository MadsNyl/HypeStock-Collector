def format_timing(timing: str) -> str:
    """
        Format timing to correct string.
    """   
    timing = timing[-10:]
    return f"{timing[-4:]}-{timing[-10:-8]}-{timing[-7:-5]}"