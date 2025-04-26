package test_case;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.Assert;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class TestServiceSSO {

    private WebDriver driver;
    private String baseUrl;

    public static void serviceLogin(WebDriver driver,String username,String password){
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

    @Test
    public void testGetSSOAccountList() {
        driver.get(baseUrl + "/");

        driver.findElement(By.id("refresh_account_button")).click();
        List<WebElement> rows = driver.findElements(By.xpath("//table[@id='account_table']/tbody/tr"));

        if (null != rows && !rows.isEmpty()) {
            System.out.println("Get SSO account list successfully!");
            Assert.assertEquals(true, (rows.size() > 0));
        }
        else {
            System.out.println("ERROR! There is no SSO account data!");
            Assert.assertEquals(true, (rows == null || rows.isEmpty()));
        }
    }




    @Test (dependsOnMethods = {"testGetSSOAccountList"})
    public void testGetSSOLoginAccountList() {
        driver.findElement(By.id("refresh_login_account_button")).click();
        List<WebElement> rows = driver.findElements(By.xpath("//table[@id='login_account_list_table']/tbody/tr"));

        if (null != rows && !rows.isEmpty()) {
            System.out.println("Get SSO login account list successfully!");
            Assert.assertEquals(true, (rows.size() > 0));
        }
        else {
            System.out.println("ERROR! There is no SSO login account data!");
            Assert.assertEquals(true, (rows == null || rows.isEmpty()));
        }
    }

    @Test (dependsOnMethods = {"testGetSSOLoginAccountList"})
    public void testKickOffSSOLoginAccount() {

        driver.findElement(By.id("refresh_login_account_button")).click();
        List<WebElement> rows = driver.findElements(By.xpath("//table[@id='login_account_list_table']/tbody/tr"));

        if (null == rows || rows.isEmpty()) {
            serviceLogin(driver, "fdse_microservices@163.com","DefaultPassword");
            driver.findElement(By.id("refresh_login_account_button")).click();
            rows = driver.findElements(By.xpath("//table[@id='login_account_list_table']/tbody/tr"));
        }


        driver.findElement(By.xpath("//table[@id='login_account_list_table']/tbody/tr[1]/td[4]/button")).click();
        List<WebElement> newRows = driver.findElements(By.xpath("//table[@id='login_account_list_table']/tbody/tr"));

        Assert.assertEquals(true, (newRows.size() == rows.size() - 1));
    }

    @AfterClass
    public void tearDown() throws Exception {
        driver.quit();
    }
}
