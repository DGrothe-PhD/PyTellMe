from speakerSetup import SpeakerStatus

speaker = SpeakerStatus()

unicode_smallcapsdic={
  'ᴀ' : 'a', 'ʙ' : 'b', 'ᴄ': 'c', 'ᴅ' : 'd', 'ᴇ' : 'e', 
  chr(42800) : 'f', 'ғ' : 'f', 'ɢ' : 'g', 
  'ʜ': 'h', 'ɪ' : 'i', 'ᴊ' : 'j', 'ᴋ' : 'k', 'ʟ' : 'l', 'ᴍ': 'm', 'ɴ': 'n', 
  'ᴏ' : 'o', 'ᴘ' : 'p', 'ǫ' : 'q',
  'ʀ': 'r', chr(0xA731): 's', 'ᴛ': 't', 'ᴜ' : 'u', 'ᴠ' : 'v', 'ᴡ' : 'w',
  'x': 'x', 'ʏ' : 'y', 'ᴢ' : 'z'
}

# TEST STRINGS
headline = "Dɪᴇ Zᴜᴋᴜɴꜰᴛ ᴅᴇꜱ Lᴇʀɴᴇɴꜱ ᴍɪᴛ Küɴꜱᴛʟɪᴄʜᴇʀ Iɴᴛᴇʟʟɪɢᴇɴᴢ"
srtest = "Fᴏʀ sᴄʀᴇᴇɴʀᴇᴀᴅᴇʀ sᴏғᴛᴡᴀʀᴇ, ɪᴛ ɪs ǫᴜɪᴛᴇ ᴅɪғғɪᴄᴜʟᴛ ᴛᴏ ʀᴇᴀᴅ sᴍᴀʟʟ ᴄᴀᴘs " + \
 "ᴛʜᴀᴛ ᴘᴇᴏᴘʟᴇ ʟɪᴋᴇ ᴛᴏ ᴜsᴇ ғᴏʀ ʜᴇᴀᴅʟɪɴᴇs ᴏɴ LɪɴᴋᴇᴅIɴ ᴘᴏsᴛs."
fox = "ᴛʜᴇ ʙɪɢ ʙʀᴏᴡɴ ғᴏx ᴊᴜᴍᴘs ᴏᴠᴇʀ ᴛʜᴇ ʟᴀᴢʏ ᴅᴏɢ."
franz = "ғʀᴀɴᴢ ᴊᴀɢᴛ ɪᴍ ᴋᴏᴍᴘʟᴇᴛᴛ ᴠᴇʀᴡᴀʜʀʟᴏsᴛᴇɴ ᴛᴀxɪ ǫᴜᴇʀ ᴅᴜʀᴄʜ ʙᴀʏᴇʀɴ."

# BEFORE CONVERSION
for saying in [headline, srtest, fox, franz]:
    speaker.talk(saying)

# output: D Z L Kü I

# CONVERSION
for to_replace, replacement in unicode_smallcapsdic.items():
    headline = headline.replace(to_replace, replacement)
    fox = fox.replace(to_replace, replacement)
    srtest = srtest.replace(to_replace, replacement)
    franz = franz.replace(to_replace, replacement)

# AFTER CONVERSION
for saying in [headline, srtest, fox, franz]:
    speaker.talk(saying)
