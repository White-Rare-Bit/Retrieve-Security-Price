import argparse
import http.client
from datetime import datetime
import pytz

def main():
    parser = argparse.ArgumentParser(description='Check current ticker price ')
    parser.add_argument('-t', metavar='ticker', action="store", help='ticker to run with, e.g. GME, aapl')
    parser.add_argument('-i', action="store_true", help='ignore the time', default=False)
    args = parser.parse_args()

    ticker = args.t
    ignore_bool = args.i

    if ignore_time(ignore_bool):
        pass
    else:
        get_ny_time()

    if yes_or_no("Are you sure that you wish to run with " + ticker + "?"):
        get_price(ticker)
    else:
        exit()

def get_ny_time():
    ny_time = datetime.now(pytz.timezone('US/Eastern'))
    print_format = "%d-%m-%Y %H:%M:%S\n"
    hour_format = "%H"
    min_format = "%M"
    c_hour = int((ny_time.strftime(hour_format)))
    c_min = int((ny_time.strftime(min_format)))
    print("Date and time in New York: " + ny_time.strftime(print_format) + "The NYSE hours are between 9:30 and 16:00")

    is_nyse_open(c_hour, c_min)

def is_nyse_open(c_hour, c_min):
    s_hour = 9
    s_min = 30
    f_hour = 16
    f_min = 0

    if s_hour <= c_hour <= f_hour:
        #print(c_hour, " is inbetween or equal to", f_hour, " and ", s_hour)
        if s_min <= c_min <= f_min:
            #print(s_min, " is inbetween or equal to", s_min, " and ", f_min)
            print("market is open.")
    else:
        print("NYSE is currently closed.")

def ignore_time(ignore_bool):
    if ignore_bool:
        print("Ignoring the current time, checking current price.")
        return True
    else:
        return False

def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question + ' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

def get_price(ticker):
    conn = http.client.HTTPSConnection("twelve-data1.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "*REDACTED*",
        'x-rapidapi-host': "twelve-data1.p.rapidapi.com"
    }
    conn.request("GET", "/price?symbol=" + ticker + "&outputsize=30&format=json", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

main()
