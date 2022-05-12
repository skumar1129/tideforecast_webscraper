from typing import List, Tuple
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()
driver = webdriver.Chrome()
WEBSITE = "https://www.tide-forecast.com/"


def scrape_location(location: str) -> None:
    city = location.split(",")[0]
    input = driver.find_element(by=By.ID, value="homepage-mast__location")
    input.clear()
    input.send_keys(city, Keys.RETURN)
    sunset_info = driver.find_element(By.CLASS_NAME, value="tide-header-summary")
    sunset_time = find_sunset_time(sunset_info.text)
    sunrise_time = find_sunrise_time(sunset_info.text)
    low_tide_info = driver.find_elements(
        By.XPATH, value="//td[contains(text(),'Low Tide')]/following-sibling::td"
    )
    low_tide_time1 = low_tide_info[0].find_element(By.TAG_NAME, value="b").text
    low_tide_height1 = low_tide_info[1].find_element(By.TAG_NAME, value="b").text
    low_tide_time2 = low_tide_info[2].find_element(By.TAG_NAME, value="b").text
    low_tide_height2 = low_tide_info[3].find_element(By.TAG_NAME, value="b").text
    results = compare_times(
        sunset_time=sunset_time,
        sunrise_time=sunrise_time,
        low_tide_time1=low_tide_time1,
        low_tide_height1=low_tide_height1,
        low_tide_time2=low_tide_time2,
        low_tide_height2=low_tide_height2,
    )
    print(f"The Low Tide for the day while the sun is up in {location}:")
    for result in results:
        print(
            f"At a time of {result[0]} the low tide  will have a height of {result[1]} \n"
        )


def compare_times(
    sunset_time: str,
    sunrise_time: str,
    low_tide_time1: str,
    low_tide_height1: str,
    low_tide_time2: str,
    low_tide_height2: str,
) -> List[Tuple[str, str]]:
    results = []
    sunset_time_int = convert_suntime_to_int(sunset_time)
    sunrise_time_int = convert_sunrise_to_int(sunrise_time)
    low_tide_time1_int = convert_lowtidetime_to_int(low_tide_time1)
    low_tide_time2_int = convert_lowtidetime_to_int(low_tide_time2)
    if low_tide_time1_int > sunrise_time_int and low_tide_time1_int < sunset_time_int:
        results.append((low_tide_time1, low_tide_height1))
    if low_tide_time2_int > sunrise_time_int and low_tide_time2_int < sunset_time_int:
        results.append((low_tide_time2, low_tide_height2))
    return results


def convert_suntime_to_int(time: str) -> int:
    hours, minutes = time.split("p")[0].split(":")
    pm_hours = int(hours) + 12
    return pm_hours * 60 + int(minutes)


def convert_sunrise_to_int(time: str) -> int:
    hours, minutes = time.split("a")[0].split(":")
    return int(hours) * 60 + int(minutes)


def convert_lowtidetime_to_int(time: str) -> int:
    hours, minutes = time.split(" ")[0].split(":")
    ampm = time.split(" ")[1]
    if ampm == "PM":
        pm_hours = int(hours) + 12
        return pm_hours * 60 + int(minutes)
    return int(hours) * 60 + int(minutes)


def find_sunset_time(info_text: str) -> str:
    info_text_array = info_text.split(" ")
    sunset_index = info_text_array.index("sunset")
    if sunset_index != -1:
        sunset_index = sunset_index + 3
        return info_text_array[sunset_index]
    else:
        return "Bad Data"


def find_sunrise_time(info_text: str) -> str:
    info_text_array = info_text.split(" ")
    sunrise_index = info_text_array.index("Sunrise")
    if sunrise_index != -1:
        sunrise_index = sunrise_index + 3
        return info_text_array[sunrise_index]
    else:
        return "Bad Data"


if __name__ == "__main__":
    locations = [
        "Half Moon Bay, California",
        "Providence, Rhode Island",
        "Huntington Beach, California",
        "Wrightsville Beach, North Carolina",
    ]
    for location in locations:
        driver.get(WEBSITE)
        scrape_location(location=location)
    driver.close()
