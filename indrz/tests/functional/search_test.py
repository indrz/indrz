# Copyright (C) 2014-2016 Michael Diener <m.diener@gomogi.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class IndrzSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_indrz(self):
        driver = self.driver
        driver.get("http://localhost:8000")
        self.assertIn("Campus", driver.title)
        elem = driver.find_element_by_id("search-input")
        elem.send_keys("Irene Fellner")
        elem.send_keys(Keys.RETURN)
        elem.submit()
        assert "No results found." not in driver.page_source


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()

