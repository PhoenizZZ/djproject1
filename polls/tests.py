from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver


class MySeleniumTests(StaticLiveServerTestCase):
    # no crearem una BD de test en aquesta ocasió
    # fixtures = ['testdb.json',]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
        # creem superusuari
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_grup(self):
        url = self.live_server_url

        # login a l'admin panel
        self.selenium.get(f"{url}/admin/login/")
        self.assertEqual(self.selenium.title, "Log in | Django site admin")
        self.selenium.find_element(By.NAME, "username").send_keys("isard")
        self.selenium.find_element(By.NAME, "password").send_keys("pirineus")
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()
        self.assertEqual(self.selenium.title, "Site administration | Django site admin")

        # 1. crear el grup
        self.selenium.get(f"{url}/admin/auth/group/add/")
        self.selenium.find_element(By.NAME, "name").send_keys("grup_test")
        self.selenium.find_element(By.NAME, "_save").click()

        # 2. el grup apareix a la llista de grups
        self.selenium.get(f"{url}/admin/auth/group/")
        self.selenium.find_element(
            By.XPATH, "//table[@id='result_list']//a[text()='grup_test']")

        # 3. el grup apareix entre els que es poden assignar a un usuari nou
        self.selenium.get(f"{url}/admin/auth/user/add/")
        self.selenium.find_element(By.NAME, "username").send_keys("nou_usuari")
        self.selenium.find_element(By.NAME, "password1").send_keys("Cl4u-segura-123")
        self.selenium.find_element(By.NAME, "password2").send_keys("Cl4u-segura-123")
        self.selenium.find_element(By.NAME, "_continue").click()
        self.selenium.find_element(
            By.XPATH, "//select[@id='id_groups_from']/option[text()='grup_test']")
