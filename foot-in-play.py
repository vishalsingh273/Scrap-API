import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def save_data(data, event_id, status):
    if status == "INTERRUPTED":
        json_data = {
            'teams': data[0],
            'date_&_time': data[1],
            'team_1_name': data[2],
            'half': data[3],
            'time': data[5],
            'team_1_goals': data[6],
            'team_2_goals': data[8],
            'team_2_name': data[9]
        }
    elif status == "ENDED" or status == "ABANDONED" or status == "HT":
        json_data = {
            'teams': data[0],
            'date_&_time': data[1],
            'team_1_name': data[2],
            'match_status': data[3],
            'team_1_goals': data[4],
            'team_2_goals': data[6],
            'team_2_name': data[7]
        }

    elif status == "ET":
        json_data = {
            'teams': data[0],
            'date_&_time': data[1],
            'team_1_name': data[2],
            'extra_half': data[3],
            'time': data[5],
            'team_1_goals': data[6],
            'team_2_goals': data[8],
            'team_2_name': data[9]
        }

    elif status == "Finished":
        json_data = {
            'teams': data[0],
            'date_&_time': data[1],
            'match_status': data[2],
            'goals': data[3]
        }
    elif status == "Time":
        json_data = {
            "teams": data[0],
            "date_&_time": data[1],
            'time': data[2],
            'current_score': data[3]
        }
    else:
        json_data = {
            'teams': data[0],
            'date_&_time': data[1],
            'team_1_name': data[2],
            'half': data[3],
            'time': data[5],
            'team_1_goals': data[6],
            'team_2_goals': data[8],
            'team_2_name': data[9]
        }

    filename = os.path.join(f"{event_id}.json")
    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)


def scrape_data():
    chrome_options = Options()
    # chrome_options.add_argument(
    #     "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://lotus365.vip/dashboard")
    driver.implicitly_wait(15)

    try:
        while True:
            football_section = driver.find_element(
                By.XPATH, "/html/body/app-root/app-layout/div/div/div/app-topnav/div[1]/nav/span[2]/a/span")
            football_section.click()
            driver.implicitly_wait(15)
            print("Navigated to football Section")

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
                            By.XPATH, '/html/body/app-root/app-layout/div/div/div/div/app-sport-detail/app-d-sport-detail/div[1]/div/div/div/div[1]/div')
                        time.sleep(8)
                        data = data_element.text.split('\n')

                        if len(data) >= 3:
                            status = ""
                            if "INTERRUPTED" in data:
                                status = "INTERRUPTED"
                            elif "ENDED" in data:
                                status = "ENDED"
                            elif "HT" in data:
                                status = "HT"
                            elif "Finished" in data:
                                status = "Finished"
                            elif "ABANDONED" in data:
                                status = "ABANDONED"
                            elif "ET" in data:
                                status="ET"
                            save_data(data, event_id, status)

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

                except Exception as e:
                    print("An error occurred while processing a row:", e)
                    continue  

            driver.refresh()

    except Exception as e:
        print("An error occurred:", e)

    finally:
        driver.quit()


if __name__ == "__main__":
    time.sleep(3)
    scrape_data()
