import time

from tools.savedata import save
from tools.sendemail import Mail
from tools.weibo_spider import getcidian_weibo
from tools.zhh_spider import getcidian


def run(interval):
    while True:
        try:
            result={}
            result.update(getcidian())
            result.update(getcidian_weibo())
            save(result)
            mail = Mail()
            mail.send()
            time_remaining = interval - time.time() % interval
            time.sleep(time_remaining)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    interval = 60*60
    run(interval)
