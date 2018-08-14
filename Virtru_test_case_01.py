######################################################
#                    Imports                         #
######################################################
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

######################################################
#                  Variables                         #
######################################################
URL = "http://www.gmail.com"
email = "jr.severn55@gmail.com"
pw = "Test123!"
decryptedMessage = "This message has been encrypted by Virtru. Please verify this message using Selenium Webdiver."

######################################################
#                  XPATHS                            #
######################################################
signIn = "//a[contains(text(), 'Sign In')]"
emailInput = "//input[contains(@id, 'identifierId')]"
emailNextButton = "//span[contains(text(), 'Next')]/ancestor::div[contains(@id, 'identifierNext')]"
passwordInput = "//input[contains(@type, 'password')]"
passwordNextButton = "//span[contains(text(), 'Next')]/ancestor::div[contains(@id, 'passwordNext')]"
encryptedEmail = "//*[contains(text(), 'Virtru')]/ancestor::tr"
unlockMessage = "//a[text()[contains(., 'Unlock Message')]]"
selectYourEmail = "//span[contains(text(), '" + email + "')]/ancestor::a"
loginWith = "//a[text()[contains(., 'Login With')]]"
sendEmail = "//a[contains(text(), 'Send me an email')]"
subject = "//span[contains(text(), 'Verify with Virtru on')]"
inbox = "//a[contains(@href, 'https://mail.google.com/mail/u/0/#inbox')]"
refresh = "//div[contains(@data-tooltip, 'Refresh')]"
verifyMe = "//a[text()[contains(., 'VERIFY ME')]]"
virtruLabel = "//span[text()[contains(., 'Encrypted Message')]]/span[contains(text(), 'Virtru')]"
decryptedMessageXpath = "//span[contains(@class, 'tdf-body')]" #"//div[contains(@class, 'row row-body')]/descendant::*[contains(text(), '" + decryptedMessage + "')]"
contextDeleteEmail = "//div[text()='Delete']"
deleteEmail = "//div[contains(@aria-label, 'Delete')]"

######################################################
#                  Test Case                         #
######################################################
def start_test_case():
#Open a browser instance, and go to a URL
    open_browser()
    browse_to_url(URL)
#Sign in to Gmail account
    print("Signing into Gmail account")
    input_text(emailInput, email)
    wait_and_click(emailNextButton)
    input_text(passwordInput, pw)
    wait_and_click(passwordNextButton)
#Open Encrypted Email
    print("Opening Encrypted Email")
    wait_and_click(encryptedEmail)
    wait_and_click(unlockMessage)
#Switch tabs
    print("Switching Tabs...")
    switch_tabs(1)
#Verify identity flow
    print("Verifying identity")
    wait_and_click(selectYourEmail)
    wait_and_click(sendEmail)
    wait_for_element_to_be_visible(subject)
    verifySubject = get_text(subject)
    global verifyEmail
    verifyEmail = "//*[contains(text(), '" + verifySubject + "')]/ancestor::tr"
    verifyEmail = verifyEmail.replace('"', '')
#Switch and close tabs
    print("Closing new tab, and switching back to original tab")
    close_tab()
    switch_tabs(0)
#Open verification email
    print("Opening verification email")
    wait_and_click(inbox)
    wait_for_new_email()
    wait_for_presence_of_element(verifyEmail)
    wait_and_click(verifyEmail)
    wait_and_click(verifyMe)
#Switch tabs
    print("Switching to tab with decrypted email")
    switch_tabs(1)
#Verify decrypted text
    print("Verifying decrypted email text")
    wait_for_element_to_be_visible(virtruLabel)
    try:
        assert get_text(decryptedMessageXpath) == decryptedMessage
    except AssertionError:
        print("The decrypted text from the email did not match the expected result: '%s' != '%s'" % (get_text(decryptedMessageXpath), decryptedMessage))

def end_test_case():
    print("Cleaning up...")
    close_tab()
    switch_tabs(0)
    wait_and_click(inbox)
    emailToDelete = wait_for_element_to_be_visible(verifyEmail)
    actionChains = ActionChains(driver)
    actionChains.context_click(emailToDelete).perform()
    wait_and_click(contextDeleteEmail)
    wait_for_element_to_be_not_visible(verifyEmail)
    print("Closing Browser: Chrome")
    driver.quit()
######################################################
#                  Functions                         #
######################################################
def open_browser():
    print("Opening Browser: Chrome")
    global driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def browse_to_url(url):

    print("Browsing to: '%s'" % (url))

    driver.get(url)

def wait_for_element_to_be_visible(xpath):
    
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    return element

def wait_for_element_to_be_not_visible(xpath):
    element = WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located((By.XPATH, xpath)))
    return element

def wait_for_new_email():
    inboxCounter = get_text(inbox)
    currentinboxCounter = get_text(inbox)
    while inboxCounter == currentinboxCounter:
        try:
            wait_and_click(inbox)
            currentinboxCounter = get_text(inbox)
        except:
            pass

def wait_for_presence_of_element(xpath):
    
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))

def wait_and_click(xpath):
    element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()

def input_text(xpath, text):
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    element.send_keys(text)

def get_text(xpath):
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    text = driver.find_element_by_xpath(xpath).text
    return text

def switch_tabs(index):
    
    driver.switch_to_window(driver.window_handles[index])

def close_tab():
    
    driver.close()

start_test_case()
end_test_case()