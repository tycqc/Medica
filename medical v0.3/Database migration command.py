import subprocess
def runcmd(command):
    ret = subprocess.run(command,shell=True)
    if ret.returncode == 0:
        print("success:",ret)
    else:
        print("error:",ret)


# runcmd(["dir","/b"])#序列参数
# runcmd("exit 1")#字符串参数
cmds = [
    # "python manage.py makemigrations --empty medicine",
    # "python manage.py makemigrations --empty orders",
    # "python manage.py makemigrations --empty staff",
    # "python manage.py makemigrations --empty store",
    # "python manage.py makemigrations",
    # "python manage.py migrate",
    "python manage.py runserver",
]
for cmd in cmds:
    runcmd(cmd)
print("OK")