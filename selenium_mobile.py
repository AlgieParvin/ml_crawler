from selenium import webdriver

if __name__ == '__main__':
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36")
    firefox = webdriver.Firefox(profile)
    firefox.set_window_position(0, 0)
    firefox.set_window_size(320, 480)
    firefox.get('http://localhost:8000')

