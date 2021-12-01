from lib import aimer
from lib import helpers
from lib import keycodes
from lib.bones import bones
import ctypes

#### CHANGE OPTIONS HERE ####

# Field of View
# Alter this between 0.1 and 3.0 for best results. 0.1 is very narrow, while larger numbers allow
# for more soldiers to be targeted
fov = 2.0

# Distance Limit
# Example, set to 100 to limit locking onto soldiers further than 100 meters away.
distance_limit = None

# Trigger Button
# Grab your preferred button from lib/keycodes.py
trigger = keycodes.LALT


# Aim Location Options
# Aim Location Switching (default is the first one listed)
# Check available bones in lib/bones.py
aim_locations = [bones['Head'], bones['Spine'], bones['Neck'], bones['Hips']]

# Key to switch aim location (set to None to disable)
aim_switch = keycodes.ADD
#aim_switch = None

# Normally, you won't need to change this
# This will attempt to gather your primary screen size. If you have issues or use
# a windowed version of BFV, you'll need to set this yourself, which probably comes with its own issues
screensize = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
# or
#screensize = (1280, 960)

#### END OF CHANGE OPTIONS ####



version = "0.5"

if fov < 0.1 or fov > 3.0:  # you can delete this if you know what you're doing
    print("检查 fov 设置.")
    exit(1)
if distance_limit is not None and distance_limit <= 0:
    print("检查 距离 设置")
    exit(1)

if __name__ == "__main__":

    if not helpers.is_admin():
        print("[+] 错误: 必须管理员权限运行")
        input("点击'回车'继续")
        exit(1)

    if not helpers.is_python3():
        print("[+] 错误: Python 2 不支持，请用Python 3")
        raw_input("点击'回车'继续")
        exit(1)

    arch = helpers.get_python_arch()
    if arch != 64:
        print("[+] 错误: 请安装64位 Python 环境" % (arch))
        input("点击'回车'继续")
        exit(1)

    print ("运行窗口大小: %s x %s" % screensize)
    aimer = aimer.Aimer(screensize, trigger, distance_limit, fov, aim_locations, aim_switch)
    aimer.start()

