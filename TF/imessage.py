import os
#osascript -e 'tell application "Messages" to send "Hello World" to buddy "J D McIninch"'

message = "Hello world"
contact = "Jave"

param = "'tell application \"Messages\" to send \"{0}\" to buddy \"{1}\"'".format(message, contact)

command = "osascript -e {0}".format(param)

print(command)

os.system(command)
#\" to buddy \"Jave\"'")


