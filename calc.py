import datetime

'''
- 土日        *1.35
- 22時以降    *1.25
- 8時間目以降 *1.25
- 24時を経過しても0時にならず、そのまま足される
    ex.) AM5:00 == 29:00
'''

def calc(start_time, end_time, day, hourly):
    hourly = int(hourly)
    print(start_time)
    print(end_time)
    print(day)
    print(hourly)
    s_h, s_m = start_time.split(':')
    e_h, e_m = end_time.split(':')
    start = datetime.timedelta(hours=int(s_h), minutes=int(s_m))
    end   = datetime.timedelta(hours=int(e_h), minutes=int(e_h))
    total_hours = float(((end-start).total_seconds()) /3600)
    salary = total_hours *hourly

    # 8時間以降
    if total_hours >= 8:
        o_h = (total_hours - 8)
        overtime_pay = (o_h *1.25 - o_h) *hourly
    else:
        overtime_pay = 0

    # 深夜
    if int(e_h) >= 22:
        m_h = (end - datetime.timedelta(hours=22))
        m_h = float(m_h.total_seconds() / 3600)
        midnight_allowance = (m_h*1.25 - m_h) *hourly
    else:
        midnight_allowance = 0

    salary += overtime_pay + midnight_allowance

    # 土日
    if day =='土曜' or '土' or '日曜' or '日':
        salary * 1.35
    
    return int(salary)
