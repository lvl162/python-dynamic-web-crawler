import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import io

with open("recipe_urls.txt", "r") as f:
    urls = f.readlines()
res = []
driver = webdriver.Chrome(ChromeDriverManager().install())

# Tu dieu chinh index array urls[] va part
# Tinh part = 2, url[2000:4000]
# Han part = 3, url[4000:6000]
# Dat part = 4, url[6000:]
# Da duoc 100 recipes in r_1.json _ ~ ~2000 cong thuc mon an 
part = 2
start = 1000
error_index = []
for url in urls[1000 : start + 10]:
    start = start + 1
    driver.get(url)
    time.sleep(3)
    try:
        khau_phan = driver.find_elements_by_xpath(
            '//*[@id="app"]/div[3]/div/div/div[1]/div[3]/div[5]/span'
        )[0].text
        nguyen_lieu = driver.find_element_by_id(id_="ingredients-list")
        title = driver.find_elements_by_class_name("recipe-name")
        title_str = ""
        img_src = driver.find_elements_by_xpath(
            '//*[@id="app"]/div[3]/div/div/div[1]/div[2]/img'
        )[0].get_attribute("src")
        n_likes = int(
            driver.find_elements_by_xpath(
                '//*[@id="app"]/div[3]/div/div/div[1]/div[3]/div[1]/span'
            )[0].text.split(" ")[0]
        )
        cook_steps_class = driver.find_elements_by_class_name("cook-step-content")[
            0
        ].text
        description = driver.find_elements_by_class_name("recipe-desc-less")[0].text
        cook_steps = cook_steps_class.split("\n")[1::2]
        for value in title:
            title_str += value.text
        arr = nguyen_lieu.text.split("\n")
        dictionary = {}
        dictionary["description"] = description
        dictionary["ingredients"] = dict(zip(arr[0::2], arr[1::2]))
        dictionary["image"] = img_src
        dictionary["cooking_steps"] = cook_steps
        dictionary["radion"] = khau_phan.split(":")[1]
        dictionary["likes"] = n_likes
        dictionary["name"] = title_str.capitalize()
        res.append(dictionary)
        with io.open("temp.json", "w+", encoding="utf-8") as outfile:
            outfile.write(json.dumps(res, ensure_ascii=False))
        print(start)
    except:
        error_index.append(start - 1)
        print("error tai %s" % start)


driver.close()

with io.open("recipes_%s.json" % part, "w", encoding="utf-8") as outfile:
    outfile.write(json.dumps(res, ensure_ascii=False))

with open("error_index.txt", "a") as fw_error:
    fw_error.write(str(error_index))

print(error_index)