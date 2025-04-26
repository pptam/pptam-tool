package test_case;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.Assert;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

import java.util.concurrent.TimeUnit;

public class TestServiceVerificationCode {
    private WebDriver driver;
    private String baseUrl;
    // private String orderId = "";

    public static void serviceLogin(WebDriver driver, String username, String password, String verificationCode){
        driver.findElement(By.id("flow_one_page")).click();
        driver.findElement(By.id("flow_preserve_login_email")).clear();
        driver.findElement(By.id("flow_preserve_login_email")).sendKeys(username);
        driver.findElement(By.id("flow_preserve_login_password")).clear();
        driver.findElement(By.id("flow_preserve_login_password")).sendKeys(password);
        driver.findElement(By.id("flow_preserve_login_verification_code")).clear();
        driver.findElement(By.id("flow_preserve_login_verification_code")).sendKeys(verificationCode);
        driver.findElement(By.id("flow_preserve_login_button")).click();
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
                {"fdse_microservices@163.com","DefaultPassword", "verification", true}, // verification code error! but now unable the function
                {"fdse_microservices@163.com", "DefaultPassword", "verificationCode", true} // verification code correct!
        };
    }

    @Test(dataProvider="user")
    public void testSignIn(String username, String password, String verificationCode, boolean expectText)throws Exception{
        driver.get(baseUrl + "/");

        //call function login
        serviceLogin(driver, username, password, verificationCode);
        Thread.sleep(1000);

        //get login status
        String statusSignIn = driver.findElement(By.id("flow_preserve_login_msg")).getText();
        if (!"".equals(statusSignIn))
            System.out.println("Sign Up btn status: "+statusSignIn);
        else
            System.out.println("False，Status of Sign In btn is NULL!"); //need to check!
        System.out.println(expectText);
        Assert.assertEquals(statusSignIn.startsWith("Success"),expectText);
    }

    @AfterClass
    public void tearDown() throws Exception {
        driver.quit();
    }
}
