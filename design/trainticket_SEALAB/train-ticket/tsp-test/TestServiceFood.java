package test_case;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.Select;
import org.testng.Assert;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.List;
import java.util.Random;
import java.util.concurrent.TimeUnit;

public class TestServiceFood {

    private WebDriver driver;
    private  String baseUrl;

    public static void login(WebDriver driver, String username, String password) {
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
    public void login() throws Exception {

        driver.get(baseUrl + "/");

        //define username and password
        String username = "fdse_microservices@163.com";
        String password = "DefaultPassword";

        //call function login
        login(driver,username,password);
        Thread.sleep(1000);

        //get login status
        String statusLogin = driver.findElement(By.id("login_result_msg")).getText();
        if("".equals(statusLogin))
            System.out.println("Failed to Login! Status is Null!");
        else if(statusLogin.startsWith("Success"))
            System.out.println("Success to Login! Status:"+statusLogin);
        else
            System.out.println("Failed to Login! Status:"+statusLogin);

        Assert.assertEquals(statusLogin.startsWith("Success"),true);
    }

    @Test (dependsOnMethods = {"login"})
    public void testGetFoodList() throws Exception {

        JavascriptExecutor js = (JavascriptExecutor) driver;

        //set the date in page
        SimpleDateFormat sdf=new SimpleDateFormat("yyyy-MM-dd");
        Calendar newDate = Calendar.getInstance();
        newDate.add(Calendar.DATE, 1);// book food of tomorrow
        String bookDate=sdf.format(newDate.getTime());
        js.executeScript("document.getElementById('food_date').value='" + bookDate + "'");

        driver.findElement(By.id("food_start_station")).clear();
        driver.findElement(By.id("food_start_station")).sendKeys("Nan Jing");

        driver.findElement(By.id("food_end_station")).clear();
        driver.findElement(By.id("food_end_station")).sendKeys("Shang Hai");

        driver.findElement(By.id("food_trip_id")).clear();
        driver.findElement(By.id("food_trip_id")).sendKeys("G1234");

        driver.findElement(By.id("query_food_button")).click();
        Thread.sleep(1000);

        List<WebElement> foodList = driver.findElements(By.xpath("//*[@id='train_food_list_table']/tbody/tr"));
        if (null == foodList || foodList.isEmpty()) {
            System.out.println("Failed! There is no food data!");
            Assert.assertEquals(true, null == foodList || foodList.isEmpty());
        }

        WebElement station = driver.findElement(By.id("food_station_select"));
        Select selectStation = new Select(station);
        selectStation.selectByValue("1"); //nanjing
        Thread.sleep(1000);

        List<WebElement> foodStoreList = driver.findElements(By.xpath("//*[@id='food_stores_of_station_list']/tbody/tr"));
        if (null == foodStoreList || foodStoreList.isEmpty()) {
            System.out.println("Failed! There is no food store data!");
            Assert.assertEquals(true, null == foodStoreList || foodStoreList.isEmpty());
        }

        driver.findElement(By.xpath("//*[@id=\"food_stores_of_station_list\"]/tbody/tr[1]/td[6]/button")).click();
        Thread.sleep(1000);

        List<WebElement> foodInStoreList = driver.findElements(By.xpath("//*[@id='food_of_store']/tbody/tr"));
        if (null == foodInStoreList || foodInStoreList.isEmpty()) {
            System.out.println("Failed! There is no food data in store!");
            Assert.assertEquals(true, null == foodInStoreList || foodInStoreList.isEmpty());
        } else {
            System.out.println("Succeed!");
            Assert.assertEquals(true, foodInStoreList.size() > 0);
        }
    }

    @Test (dependsOnMethods = {"login"})
    public void testQueryFoodOrderList() throws Exception {

        driver.findElement(By.id("query_food_order_button")).click();
        Thread.sleep(1000);

        List<WebElement> foodOrderList = driver.findElements(By.xpath("//*[@id='food_order_list_table']/tbody/tr"));
        if (null == foodOrderList || foodOrderList.isEmpty()) {
            System.out.println("Failed! There is no food order data, please book food first!");
            Assert.assertEquals(true, null == foodOrderList || foodOrderList.isEmpty());
        } else {
            System.out.println("Succeed!");
            Assert.assertEquals(true, foodOrderList.size() > 0);
        }
    }

    @AfterClass
    public void tearDown() throws Exception {
        driver.quit();
    }
}