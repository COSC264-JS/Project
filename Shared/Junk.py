from Shared import packet

stringInput = """1881400512Harry Potter and the Goblet of Fire by J.K. Rowling

HARRY POTTER AND THE GOBLET OF FIRE

CHAPTER ONE ­ THE RIDDLE HOUSE

The villagers of Little Hangleron still called it "the Riddle House," even though it had been many years since the Riddle family had lived there. It stood on a hill overlooking the village, some of its windows boarded, tiles missing from its roof, and ivy spreading unchecked over its face. Once a fine­looking manor,"""

newPacket = packet.createPacketFromString(stringInput)
