import os
from mido import MidiFile


def list_files(extension=""):
    """
    docstring here
    """
    # folder path
    dir_path = r'.'
    # list to store files
    res = []
    # add dot if needed
    if extension != "" or not extension.startswith("."):
        extension = '.' + extension
    extension = extension.lower()
    # Iterate directory
    for filename in os.listdir(dir_path):
        # check only text files
        if filename.lower().endswith(extension):
            res.append(filename)
    return res

def get_integer_value():
    """
    docstring here
    """
    user_value = input()
    try:
        return int(user_value)
    except ValueError:
        print(f"{user_value} is not a valid integer. Please try again.")
    return get_integer_value()

def export_tracks( track_nums : list, tracks : list ):
    """
    docstring here
    """
    for i_track in track_nums:
        track = tracks[i_track]
        notes = []
        csvname = str(i_track) + "_" + track.name + ".csv"
        outfile = open(file=csvname, mode="w")
        cumtime = 0
        for x in track:
            try:
                note = x.note #duck-typing check
                print (x)
                typechannel = "00"
                if x.type == "note_on":
                    typechannel = "9"
                elif x.type == "note_off":
                    typechannel = "8"
                #typechannel += "{:1x}".format( x.channel )
                # if x.channel == 1:
                #     continue
                typechannel += "0"
                line = str( x.time) \
                     + ',' + str(x.type) \
                     + ',' + str(x.channel) \
                     + ',' + str(x.note) \
                     + ',' + str(x.velocity)
                #need a check for exceeding the 1-byte time
                time = 0
                time_adjuster = 8 # bigger value -> song plays faster
                if x.time != 0:
                    time = int(min( max(1,int(x.time/time_adjuster+0.4999)), 127 ))
                cumtime += x.time
                line += \
                    ',' + '"=""{:02x}"""'.format(time) \
                    + ',' + typechannel \
                    + ',' + '"=""{:02x}"""'.format(x.note) \
                    + ',' + '"=""{:02x}"""'.format(x.velocity)
                line += '\n'
                outfile.write(line)
                notes.append(note)
            except AttributeError:
                cumtime += x.time
                print(len(notes), "cumutime:", cumtime, x)
                
        print(str(i_track) + " | '" + track.name + "' (" + str(len(notes)) + " notes)")
        outfile.close()

print("==== MIDI Files in this Directory ==== ")
midis = list_files("mid")
for i in range(0,len(midis)):
    print(i," : ", midis[i])
print("====================================== ")
print("Enter the number of the file to open:")
filenumber = get_integer_value()

midi = []
mido = None
try:
    f = open(midis[filenumber], "rb")
    midi = f.read()
    mido = MidiFile(midis[filenumber], clip=True)
except Exception as e:
    print("There was a problem opening or reading the file:")
    print(e)
    quit()
print()

print("==== Track List ====")
for iTrack in range(0, len(mido.tracks)):
    track = mido.tracks[iTrack]
    numNotes = 0
    for x in track:
        # find the notes using duck-typing on .note
        try:
            note = x.note #
            numNotes += 1
        except:
            pass
    print(str(iTrack) + " | '" + track.name + "' (" + str(numNotes) + " notes)")

print ("Choose a track to export to .csv:")
trackNum = get_integer_value()
export_tracks([trackNum], mido.tracks)
