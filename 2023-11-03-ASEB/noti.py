import select

import pyfanotify as fan


if __name__ == '__main__':
    fanot = fan.Fanotify(init_fid=True)
    fanot.mark('/var/spool/cron/crontabs', is_type='fs', ev_types=fan.FAN_ALL_FID_EVENTS)
    fanot.mark('/tmp/', is_type='fs', ev_types=fan.FAN_ALL_FID_EVENTS)
    fanot.start()

    cli = fan.FanotifyClient(fanot, path_pattern='*')
    poll = select.poll()
    poll.register(cli.sock.fileno(), select.POLLIN)
    try:
        while poll.poll():
            x = {}
            for i in cli.get_events():
                i.ev_types = fan.evt_to_str(i.ev_types)
                x.setdefault(i.path, []).append(i)
            if "cron" in str(x) or "boatnet" in str(x):
                print(x)
    except:
        print('STOP')

    cli.close()
    fanot.stop()
