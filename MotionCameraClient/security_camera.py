from picamera import PiCamera
import time
import telebot
import RPi.GPIO as GPIO

camera = PiCamera()
camera_online = False

GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(16, GPIO.IN)

f = open("token.txt", "r")
lines = f.readlines()
token = lines[0].strip()
group_id = lines[1].strip()

print("Token: " + str(token))
print("GroupID: " + str(group_id))

bot = telebot.TeleBot(str(token))


def toggle_bot():
    global camera_online

    while camera_online:
        if GPIO.input(16) == GPIO.HIGH:
            print("Motion detected...")
            camera.start_preview()
            time.sleep(0.5)
            camera.capture('/home/pi/images/image.jpg')
            bot.send_photo(chat_id=int(group_id), photo=open("/home/pi/images/image.jpg", "rb"))
            camera.stop_preview()
            blink_slow(6)
            blink_slow(3)


def blink_fast(times):
    times_blinked = 0
    while int(times_blinked) != int(times):
        GPIO.output(18, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(18, GPIO.LOW)
        time.sleep(0.1)
        times_blinked = times_blinked + 1


def blink_slow(times):
    times_blinked = 0
    while int(times_blinked) != int(times):
        GPIO.output(18, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(18, GPIO.LOW)
        time.sleep(0.5)
        times_blinked = times_blinked + 1


def set_camera_value(value):
    global camera_online

    camera_online = value

    if camera_online:
        print("Cameras online!...")
        toggle_bot()
    else:
        print("Cameras offline!...")


@bot.message_handler(commands=['start'])
def start_camera():
    set_camera_value(True)


@bot.message_handler(commands=['stop'])
def stop_camera():
    set_camera_value(False)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Wrong Input")


camera.start_preview()
blink_fast(10)
camera.stop_preview()

bot.polling()
