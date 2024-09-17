#
class UnicodeConversions:
    """Conversion dictionaries and methods for most important Unicode formatting styles."""
    unicodeSmallCapsDic={
     'ᴀ' : 'a', 'ʙ' : 'b', 'ᴄ': 'c', 'ᴅ' : 'd', 'ᴇ' : 'e', 
     chr(42800) : 'f', 'ғ' : 'f', 'ɢ' : 'g', 
     'ʜ': 'h', 'ɪ' : 'i', 'ᴊ' : 'j', 'ᴋ' : 'k', 'ʟ' : 'l', 'ᴍ': 'm', 'ɴ': 'n', 
     'ᴏ' : 'o', 'ᴘ' : 'p', 'ǫ' : 'q',
     'ʀ': 'r', chr(0xA731): 's', 'ᴛ': 't', 'ᴜ' : 'u', 'ᴠ' : 'v', 'ᴡ' : 'w',
     'x': 'x', 'ʏ' : 'y', 'ᴢ' : 'z'
    }
    
    @staticmethod
    def convertSmallCaps(headline : str) -> str:
        """converts SMALL-CAPS unicode strings to normal ones."""
        hl = headline
        for to_replace, replacement in UnicodeConversions.unicodeSmallCapsDic.items():
            hl = hl.replace(to_replace, replacement)
        return hl