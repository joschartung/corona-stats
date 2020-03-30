import requests
import time
link = "https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases"

def main():
    confirmed = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv"
    rc = requests.get(confirmed)
    with open("data/time_series_covid19_confirmed_global.csv",'wb') as f:
        f.write(rc.content)
    f.close()
    print("waiting for next request")
    time.sleep(1)
    deaths = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv"
    rd = requests.get(deaths)
    with open("data/time_series_covid19_deaths_global.csv", 'wb') as f:
        f.write(rd.content)
    f.close()
    print("waiting for final request")
    time.sleep(1)
    recovered = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv"
    rr = requests.get(recovered)
    with open("data/time_series_covid19_recovered_global.csv", 'wb') as f:
        f.write(rr.content)
    f.close()

if __name__ == "__main__":
    main()
