# from mido import MidiFile, MidiTrack, Message

# input_path = 'input/Naruto Shippuuden - Blue Bird.mid.mid'  # ไฟล์ MIDI ต้นฉบับ
# output_path = 'output_c3_b51.mid'  # ไฟล์ MIDI ที่ปรับแล้ว

# # ช่วงโน้ตที่ต้องการ (C3 ถึง B5)
# MIN_NOTE = 48  # C3
# MAX_NOTE = 71  # B5

# # โน้ตชาร์ปที่ต้องปรับ
# SHARP_TO_NEAREST = {
#     49: 48,  # C# -> C
#     51: 52,  # D# -> E
#     54: 53,  # F# -> F
#     56: 57,  # G# -> A
#     58: 57,  # A# -> A
#     61: 60,  # C# -> C (อ็อกเทฟสูง)
#     63: 64,  # D# -> E (อ็อกเทฟสูง)
#     66: 65,  # F# -> F (อ็อกเทฟสูง)
#     68: 69,  # G# -> A (อ็อกเทฟสูง)
#     70: 69,  # A# -> A (อ็อกเทฟสูง)
# }

# # โหลด MIDI
# midi = MidiFile(input_path)
# adjusted_midi = MidiFile()

# for track in midi.tracks:
#     new_track = MidiTrack()
#     for msg in track:
#         if msg.type in ['note_on', 'note_off']:
#             note = msg.note

#             # ปรับโน้ตให้อยู่ในช่วง C3 ถึง B5
#             while note < MIN_NOTE:
#                 note += 12  # เพิ่ม 1 อ็อกเทฟ
#             while note > MAX_NOTE:
#                 note -= 12  # ลด 1 อ็อกเทฟ

#             # ปรับโน้ตชาร์ป
#             if note in SHARP_TO_NEAREST:
#                 note = SHARP_TO_NEAREST[note]

#             # อัพเดตโน้ต
#             msg.note = note

#         new_track.append(msg)
#     adjusted_midi.tracks.append(new_track)

# # บันทึกไฟล์ MIDI ที่ปรับแล้ว
# adjusted_midi.save(output_path)

from mido import MidiFile, MidiTrack, Message

input_path = 'input/Attack on Titan Original.mid'  # ไฟล์ MIDI ต้นฉบับ
output_path = 'Attack Original.mid'  # ไฟล์ MIDI ที่ปรับแล้ว

# ช่วงโน้ตที่ต้องการ (C3 ถึง B6)
MIN_NOTE = 48  # C3
MAX_NOTE = 83  # B6

# โน้ตชาร์ปที่ต้องปรับ
SHARP_TO_NEAREST = {
    49: 48,  # C# -> C
    51: 52,  # D# -> E
    54: 53,  # F# -> F
    56: 57,  # G# -> A
    58: 57,  # A# -> A
    61: 60,  # C# -> C
    63: 64,  # D# -> E
    66: 65,  # F# -> F
    68: 69,  # G# -> A
    70: 69,  # A# -> A
    73: 72,  # C# -> C
    75: 76,  # D# -> E
    78: 77,  # F# -> F
    80: 81,  # G# -> A
    82: 81,  # A# -> A
}

# โหลด MIDI
midi = MidiFile(input_path)
adjusted_midi = MidiFile()

for track in midi.tracks:
    new_track = MidiTrack()
    for msg in track:
        if msg.type in ['note_on', 'note_off']:
            note = msg.note

            # ปรับโน้ตให้อยู่ในช่วง C3 ถึง B6
            while note < MIN_NOTE:
                note += 12  # เพิ่ม 1 อ็อกเทฟ
            while note > MAX_NOTE:
                note -= 12  # ลด 1 อ็อกเทฟ

            # ปรับโน้ตชาร์ป
            if note in SHARP_TO_NEAREST:
                note = SHARP_TO_NEAREST[note]

            # อัพเดตโน้ต
            msg.note = note

        new_track.append(msg)
    adjusted_midi.tracks.append(new_track)

# บันทึกไฟล์ MIDI ที่ปรับแล้ว
adjusted_midi.save(output_path)
