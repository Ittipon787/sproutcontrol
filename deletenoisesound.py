from mido import MidiFile, MidiTrack, Message

# โหลดไฟล์ MIDI
input_file = "input/AnyConv.com__BOWKYLION - วาดไว (recall) _ Piano Cover & Tutorial  MUSIC SHEET.midi"
output_file = "output_file.mid"
midi = MidiFile(input_file)

# สร้างไฟล์ MIDI ใหม่
new_midi = MidiFile()

for track in midi.tracks:
    new_track = MidiTrack()
    for msg in track:
        if msg.type == 'note_on' or msg.type == 'note_off':
            # ตัวกรอง: ลบโน้ตที่มี velocity ต่ำกว่า 20
            if msg.velocity > 20:
                new_track.append(msg)
        else:
            new_track.append(msg)
    new_midi.tracks.append(new_track)

# บันทึกไฟล์ MIDI ที่ปรับปรุงแล้ว
new_midi.save(output_file)
print(f"Saved filtered MIDI to {output_file}")
