from audio import player, recorder
import time

mPlayer=player(None)
mPlayer.set_vol(100)

aRecorder=recorder()
aRecorder.start('/sdcard/record.wav', recorder.WAV, 10)

i = 0
while aRecorder.is_running():
    print('Recording:', i)
    i += 1
    time.sleep(1)

aRecorder.stop()

print('Playback the recording file')
mPlayer.play('file://sdcard/record.wav')