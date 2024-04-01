import json
import os
import time
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def save_data(data, event_id, status):
    if status == "INTERRUPTED":
        json_data = {
            
            "date_&_time": data[0],
            "team_1_name": data[1],
            "team _1_score": data[2],
            "team_1_run_rate": data[3],
            "current_status": data[4],
            "current_over": data[5],
            "team _2_name": data[6],
            "team_2_score": data[7],
            "team_2_run_rate": data[8],
        }
    elif status == "ENDED":
        json_data = {
            
            "date_&_time": data[0],
            "team_1_name": data[1],
            "team _1_score": data[2],
            "team_1_run_rate": data[3],
            "current_status": data[4],
            "current_over": data[5],
            "team _2_name": data[6],
            "team_2_score": data[7],
            "team_2_run_rate": data[8],
        }

    elif status == "INN":
        json_data = {

            "date_&_time": data[0],
            "team_1_name": data[1],
            "team_1_score": data[2],
            "team_1_run_rate": data[3],
            "team_2_name": data[5],
            "team_2_score": data[6],
            "team_2_run_rate": data[7],
            "inn_no": data[8],
            "overs": data[10],
            "match_status": data[12],
        }
    elif status == "00/0 (0.0)":
        json_data = {

            "date_&_time": data[0],
            "team_1_name": data[1],
            "team_1_score": data[2],
            "team_1_run_rate": data[3],
            "current_status": data[4],

            "current_over": data[5],
            "team_2_name": data[6],
            "team_2_score": data[7],
            "team_1_run_rate": data[8],
        }
    # elif status=="no data":
    #     json_data={
    #         "data_&_time":data[0]
    #     }
    else:

        json_data = {

            "date_&_time": data[0],
            "team_1_name": data[1],
            "team_1_score": data[2],
            "team_1_run_rate": data[3],
            "current_status": data[4],
            "match_status": data[5],
            "current_over": data[6],
            "team_2_name": data[7],
            "team_2_score": data[8],
            "team_1_run_rate": data[9],
        }

    folder_name = "cricket"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    filename = os.path.join(folder_name, f"{event_id}.json")
    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)


def scrape_data():
    chrome_options = Options()
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://lotus365.vip/dashboard")
    driver.implicitly_wait(15)

    try:
        while True:
            football_section = driver.find_element(
                By.XPATH, "/html/body/app-root/app-layout/div/div/div/app-topnav/div[1]/nav/span[1]/a/span")
            football_section.click()
            driver.implicitly_wait(15)
            print("Navigated to cricket Section")

            div_element = driver.find_element(
                By.XPATH, '/html/body/app-root/app-layout/div/div/div/div/app-dashboard/app-d-dashboard/div[1]/div[4]/div/app-d-sport-list/div/table')

            rows = WebDriverWait(driver, 15).until(
                EC.visibility_of_all_elements_located((By.TAG_NAME, 'tr')))

            for row in rows:
                try:
                    link = WebDriverWait(row, 15).until(
                        EC.visibility_of_element_located((By.TAG_NAME, 'a')))
                    small_tag = WebDriverWait(row, 15).until(
                        EC.visibility_of_element_located((By.TAG_NAME, 'small')))

                    link_url = link.get_attribute('href')
                    small_class = small_tag.get_attribute('class')

                    if small_class == 'in-play-content':
                        print(link_url)

                        event_id = link_url.split('/')[-1]

                        driver.execute_script(
                            "window.open('" + link_url + "', '_blank');")
                        driver.switch_to.window(driver.window_handles[-1])

                        data_element = driver.find_element(
                            By.XPATH, '/html/body/app-root/app-layout/div/div/div/div/app-sport-detail/app-d-sport-detail/div[1]/div/div/div/div[1]/div/div[2]')
                        time.sleep(8)
                        data = data_element.text.split('\n')

                        status = ""
                        if "INTERRUPTED" in data:
                            status = "INTERRUPTED"
                        elif "ENDED" in data:
                            status = "ENDED"
                        elif "INN 4"in data:
                            status = "INN"
                        elif "00/0 (0.0)" in data:
                            status="00/0 (0.0)"
                        # elif "00/0 (0.0)" not in data:
                        #     status="no data"
                        save_data(data, event_id, status)

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

                except Exception as e:
                    print("An error occurred while processing a row:", e)
                    continue
            driver.refresh()
            time.sleep(4)

    except Exception as e:
        print("An error occurred:", e)

    finally:
        driver.quit()


if __name__ == "__main__":

    time.sleep(3)
    scrape_data()
