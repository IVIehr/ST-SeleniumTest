import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest


def extract_number(text):
    # getting numbers from string
    res = [int(i) for i in text.split() if i.isdigit()]
    return int(res[0])


class SampleTestCase(unittest.TestCase):

    def setUp(self):
        # open Firefox browser
        self.driver = webdriver.Chrome()
        # maximize the window size
        self.driver.maximize_window()
        # delete the cookies
        self.driver.delete_all_cookies()
        # navigate to the url
        self.driver.get('http://localhost:3000/')
        self.counter = 0

    def testAdd(self):
        record = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/main/main/main/p')
        number_of_divs = extract_number(record.text)
        number_of_rows = int(number_of_divs / 4)

        for j in range(number_of_rows):
            round = j + 1
            last_div_in_row = number_of_rows * round
            first_div_in_row = last_div_in_row - number_of_rows + 1
            for i in range(first_div_in_row, last_div_in_row):
                button = self.driver.find_element(By.XPATH, f'//*[@id="root"]/div/main/main/div/div[{i}]/button')
                button.click()
                self.counter += 1
                elem = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[1]/div/div')
                time.sleep(1)
                self.assertEqual(int(elem.text), self.counter, f"Add button of div{i} is not working correctly")

    def testQuantity(self):
        button = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/main/main/div/div[1]/button')
        button.click()
        self.counter += 1
        button.click()
        self.counter += 1
        button.click()
        self.counter += 1
        quantity = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div/div[1]/p[2]')

        amount_of_quantity = extract_number(quantity.text)
        time.sleep(1)
        self.assertEqual(amount_of_quantity, self.counter, "Counting the quantity is not correct")

        minus = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div/div[2]/div/button[1]')
        minus.click()
        self.counter -= 1
        quantity = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div/div[1]/p[2]')

        amount_of_quantity = extract_number(quantity.text)
        time.sleep(1)
        self.assertEqual(amount_of_quantity, self.counter, "Counting the quantity is not correct")

        plus = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div/div[2]/div/button[2]')
        plus.click()
        plus.click()
        self.counter += 2
        quantity = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div/div[1]/p[2]')

        amount_of_quantity = extract_number(quantity.text)
        time.sleep(1)
        self.assertEqual(amount_of_quantity, self.counter, "Counting the quantity is not correct")

    def testRemove(self):
        add_button = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/main/main/div/div[3]/button')
        for i in range(20):
            add_button.click()

        remove_button = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div/button')
        remove_button.click()
        elem = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[1]/div/div')
        time.sleep(1)
        self.assertEqual(int(elem.text), 0, "Remove button does not work correctly")

    def testToggle(self):
        for i in range(7):
            record = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/main/main/main/p')
            number_of_items = extract_number(record.text)
            option = self.driver.find_element(By.XPATH, f'//*[@id="root"]/div/main/div/div[1]/div[{i + 1}]')
            option.click()
            new_record = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/main/main/main/p')
            new_number_of_items = extract_number(new_record.text)
            time.sleep(1)
            self.assertNotEqual(number_of_items, new_number_of_items, "toggling the buttons of filtering is not "
                                                                   "working properly")

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
