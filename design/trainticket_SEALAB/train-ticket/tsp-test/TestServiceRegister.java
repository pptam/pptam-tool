package test_case;

import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.Assert;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

import java.util.concurrent.TimeUnit;

public class TestServiceRegister {
    private WebDriver driver;
    private String baseUrl;
    public static void login(WebDriver driver,String username,String password){
        driver.findElement(By.id("login_email")).clear();
        driver.findElement(By.id("login_email")).sendKeys(username);
        driver.findElement(By.id("login_password")).clear();
        driver.findElement(By.id("login_password")).sendKeys(password);
        driver.findElement(By.id("login_button")).click();
    }
    @BeforeClass
    public void setUp() throws Exception {
        System.setProperty("webdriver.chrome.driver", "/Users/hechuan/Downloads/chromedriver");
        driver = new ChromeDriver();
        baseUrl = "http://localhost:80/";
        driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
    }
    @DataProvider(name="user")
    public Object[][] Users(){
        return new Object[][]{
                {"hechuan@outlook.com", "DefaultPassword"}, // already exits
                {"he@outlook.com", "DefaultPassword"}, // register user
        };
    }
    @Test (dataProvider="user")
    public void testRegister(String username,String password) throws Exception{
        driver.get(baseUrl + "/");

        driver.findElement(By.id("register_email")).clear();
        driver.findElement(By.id("register_email")).sendKeys(username);
        driver.findElement(By.id("register_password")).clear();
        driver.findElement(By.id("register_password")).sendKeys(password);

        driver.findElement(By.id("register_button")).click();
        Thread.sleep(1000);

        String statusSignUp = driver.findElement(By.id("register_result_msg")).getText();
        if (statusSignUp.startsWith("Success")) {
            System.out.println("Sign Up btn status:" + statusSignUp);
            Assert.assertEquals(statusSignUp.startsWith("Success"),true);
        }
        else {
            System.out.println("Failed, Status of Sign Up btn is: " + statusSignUp);
            Assert.assertEquals(statusSignUp.startsWith("Success"),false);
        }
    }

    //@Test // In single micro service, the register service need to verify the format of register email.
    public void testRegisterErrorInfo() throws Exception {
        driver.get(baseUrl + "/");

        driver.findElement(By.id("register_email")).clear();
        driver.findElement(By.id("register_email")).sendKeys("chuan");
        driver.findElement(By.id("register_password")).clear();
        driver.findElement(By.id("register_password")).sendKeys("DefaultPassword");

        driver.findElement(By.id("register_button")).click();
        Thread.sleep(1000);

        Alert alert = driver.switchTo().alert();
        if (null != alert) {
            String alertMessage = alert.getText();
            if (null != alertMessage && alertMessage.startsWith("Email Format Wrong.")) {
                System.out.println("Failed, Status of Sign Up btn is: " + alertMessage);
                Assert.assertEquals(alertMessage.startsWith("Success"), false);
            }
        }

        String statusSignUp = driver.findElement(By.id("register_result_msg")).getText();
        if (statusSignUp.startsWith("Success")) {
            System.out.println("Sign Up btn status:" + statusSignUp);
            Assert.assertEquals(statusSignUp.startsWith("Success"), true);
        } else {
            System.out.println("Failed, Status of Sign Up btn is: " + statusSignUp);
            Assert.assertEquals(statusSignUp.startsWith("Success"), false);
        }
    }

    @Test (dependsOnMethods = {"testRegister"}, dataProvider = "user")
    public void testRegisterLogin(String username,String password) throws Exception{
        //call function login
        login(driver, username, password);
        Thread.sleep(1000);

        //get login status
        String statusLogin = driver.findElement(By.id("login_result_msg")).getText();
        if(statusLogin.startsWith("Success")) {
            System.out.println("Login status:"+statusLogin);
            driver.findElement(By.id("microservice_page")).click();
        }
        else if("".equals(statusLogin))
            System.out.println("False,Failed to login! StatusLogin is NULL");
        else
            System.out.println("Failed to login!" + "Wrong login Id or password!");

        Assert.assertEquals(statusLogin.startsWith("Success"),true);
    }
    @AfterClass
    public void tearDown() throws Exception {
        driver.quit();
    }
}
