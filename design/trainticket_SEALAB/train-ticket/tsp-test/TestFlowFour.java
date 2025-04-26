package test_case;

import org.openqa.selenium.*;
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

public class TestFlowFour {

    private WebDriver driver;
    private String baseUrl;



    public static void serviceLogin(WebDriver driver, String username, String password, String verificationCode){
        driver.findElement(By.id("flow_four_page")).click();
        driver.findElement(By.id("flow_advanced_reserve_login_email")).clear();
        driver.findElement(By.id("flow_advanced_reserve_login_email")).sendKeys(username);
        driver.findElement(By.id("flow_advanced_reserve_login_password")).clear();
        driver.findElement(By.id("flow_advanced_reserve_login_password")).sendKeys(password);
        driver.findElement(By.id("flow_advanced_reserve_login_verification_code")).clear();
        driver.findElement(By.id("flow_advanced_reserve_login_verification_code")).sendKeys(verificationCode);
        driver.findElement(By.id("flow_advanced_reserve_login_button")).click();
    }

    //获取指定位数的随机字符串(包含数字,0<length)
    public static String getRandomString(int length) {
        //随机字符串的随机字符库
        String KeyString = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        StringBuffer sb = new StringBuffer();
        int len = KeyString.length();
        for (int i = 0; i < length; i++) {
            sb.append(KeyString.charAt((int) Math.round(Math.random() * (len - 1))));
        }
        return sb.toString();
    }
    @BeforeClass
    public void setUp() throws Exception {
        System.setProperty("webdriver.chrome.driver", "D:/Program/chromedriver_win32/chromedriver.exe");
        driver = new ChromeDriver();
        baseUrl = "http://10.141.212.24/";
        driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
    }

    // step 1: login
    @Test
    public void login()throws Exception {
        driver.get(baseUrl + "/");
        //Go to flow_four_page

        //define username and password
        String username = "fdse_microservices@163.com";
        String password = "DefaultPassword";
        String verificationCode = "verificationCode";

        //call function login
        serviceLogin(driver,username,password, verificationCode);
        Thread.sleep(1000);

        //get login status
        String statusLogin = driver.findElement(By.id("flow_advanced_reserve_login_msg")).getText();
        if("".equals(statusLogin))
            System.out.println("Failed to Login! Status is Null!");
        else if(statusLogin.startsWith("Success"))
            System.out.println("Success to Login! Status:"+statusLogin);
        else
            System.out.println("Failed to Login! Status:"+statusLogin);
        Assert.assertEquals(statusLogin.startsWith("Success"),true);

    }

    // step 2: advanced ticket searching
    @Test (dependsOnMethods = {"login"})
    public void testAdvancedSearching() throws Exception{

        //  step 1:  login
        this.login();
        JavascriptExecutor js = (JavascriptExecutor) driver;

        js.executeScript("document.getElementById('flow_advanced_reserve_startingPlace').value='Nan Jing'");
        js.executeScript("document.getElementById('flow_advanced_reserve_terminalPlace').value='Shang Hai'");

        SimpleDateFormat sdf =new SimpleDateFormat("yyyy-MM-dd");
        Calendar newDate = Calendar.getInstance();
        Random randDate = new Random();
        int randomDate = randDate.nextInt(26); //int范围类的随机数
        newDate.add(Calendar.DATE, randomDate+5);//随机定5-30天后的票
        String date = sdf.format(newDate.getTime());
        js.executeScript("document.getElementById('flow_advanced_reserve_booking_date').value='" + date + "'");

        // simulate dropdown list
        Select searchType = new Select(driver.findElement(By.id("flow_advanced_reserve_select_searchType")));
        searchType.selectByValue("Quickest"); // 3rd: quickest

        driver.findElement(By.id("flow_advanced_reserve_booking_button")).click();

        List<WebElement> ticketsList = driver.findElements(By.xpath("//table[@id='flow_advanced_reserve_booking_list_table']/tbody/tr"));
        //Confirm ticket selection
        if (null == ticketsList || ticketsList.size() == 0) {
            driver.findElement(By.id("flow_advanced_reserve_booking_button")).click();
            ticketsList = driver.findElements(By.xpath("//table[@id='flow_advanced_reserve_booking_list_table']/tbody/tr"));
        }
        else {
            //Pick up a train at random and book tickets
            System.out.printf("Success to search tickets，the tickets list size is:%d%n",ticketsList.size());
            Random rand = new Random();
            int i = rand.nextInt(1000) % ticketsList.size(); //int范围类的随机数
            WebElement elementBookingSeat = ticketsList.get(i).findElement(By.xpath("td[11]/select"));
            Select selSeat = new Select(elementBookingSeat);
            selSeat.selectByValue("3"); //2st
            ticketsList.get(i).findElement(By.xpath("td[13]/button")).click();
            Thread.sleep(1000);
        }

        Assert.assertEquals(ticketsList.size() > 0,true);
    }

    // step 3: select contacts
    @Test (dependsOnMethods = {"testAdvancedSearching"})
    public void testSelectContacts() throws Exception {

        List<WebElement> contactsList = driver.findElements(By.xpath("//table[@id='flow_advanced_reserve_contacts_booking_list_table']/tbody/tr"));

        //Confirm ticket selection
        if (null == contactsList || contactsList.size() == 0) {
            driver.findElement(By.id("flow_advanced_reserve_booking_contacts_button")).click();
            Thread.sleep(1000);
            contactsList = driver.findElements(By.xpath("//table[@id='flow_advanced_reserve_contacts_booking_list_table']/tbody/tr"));
        }

        if(contactsList.size() == 0)
            System.out.println("Show Contacts failed!");

        Assert.assertEquals(contactsList.size() > 0,true);

        if (contactsList.size() == 1){
            String contactName = getRandomString(5);
            String documentType = "1";//ID Card
            String idNumber = getRandomString(8);
            String phoneNumber = getRandomString(11);

            contactsList.get(0).findElement(By.xpath("td[2]/input")).sendKeys(contactName);
            WebElement elementContactstype = contactsList.get(0).findElement(By.xpath("td[3]/select"));
            Select selTraintype = new Select(elementContactstype);
            selTraintype.selectByValue(documentType); //ID type

            contactsList.get(0).findElement(By.xpath("td[4]/input")).sendKeys(idNumber);
            contactsList.get(0).findElement(By.xpath("td[5]/input")).sendKeys(phoneNumber);
            contactsList.get(0).findElement(By.xpath("td[6]/label/input")).click();
        }

        if (contactsList.size() > 1) {
            Random rand = new Random();
            int i = rand.nextInt(100) % (contactsList.size() - 1); //int范围类的随机数
            contactsList.get(i).findElement(By.xpath("td[6]/label/input")).click();
        }
        driver.findElement(By.id("flow_advanced_reserve_ticket_select_contacts_confirm_btn")).click();
        System.out.println("Ticket contacts selected btn is clicked");
        Thread.sleep(1000);
        }

    // step 4: Confirm Your Ticket Information
    @Test (dependsOnMethods = {"testAdvancedSearching"})
    public void testConfirmTicketInfo() throws Exception {

        String itemFrom = driver.findElement(By.id("flow_advanced_reserve_ticket_confirm_from")).getText();
        String itemTo = driver.findElement(By.id("flow_advanced_reserve_ticket_confirm_to")).getText();
        String itemTripId = driver.findElement(By.id("flow_advanced_reserve_ticket_confirm_tripId")).getText();
        String itemPrice = driver.findElement(By.id("flow_advanced_reserve_ticket_confirm_price")).getText();
        String itemDate = driver.findElement(By.id("flow_advanced_reserve_ticket_confirm_travel_date")).getText();
        String itemName = driver.findElement(By.id("flow_advanced_reserve_ticket_confirm_contactsName")).getText();
        String itemSeatType = driver.findElement(By.id("flow_advanced_reserve_ticket_confirm_seatType_String")).getText();
        String itemDocumentType = driver.findElement(By.id("flow_advanced_reserve_ticket_confirm_documentType")).getText();
        String itemDocumentNum = driver.findElement(By.id("flow_advanced_reserve_ticket_confirm_documentNumber")).getText();
        boolean bFrom = !"".equals(itemFrom);
        boolean bTo = !"".equals(itemTo);
        boolean bTripId = !"".equals(itemTripId);
        boolean bPrice = !"".equals(itemPrice);
        boolean bDate = !"".equals(itemDate);
        boolean bName = !"".equals(itemName);
        boolean bSeatType = !"".equals(itemSeatType);
        boolean bDocumentType = !"".equals(itemDocumentType);
        boolean bDocumentNum = !"".equals(itemDocumentNum);
        boolean bStatusConfirm = bFrom && bTo && bTripId && bPrice && bDate && bName && bSeatType && bDocumentType && bDocumentNum;

        if(!bStatusConfirm){
            driver.findElement(By.id("flow_advanced_reserve_ticket_confirm_cancel_btn")).click();
            System.out.println("Confirming Ticket Canceled!");
        }

        Assert.assertEquals(bStatusConfirm,true);

        driver.findElement(By.id("flow_advanced_reserve_ticket_confirm_confirm_btn")).click();
        Thread.sleep(1000);
        System.out.println("Confirm Ticket!");

        // get the  status alert
        Alert javascriptConfirm = driver.switchTo().alert();
        String statusAlert = driver.switchTo().alert().getText();
        System.out.println("The Alert information of Confirming Ticket：" + statusAlert);
        Assert.assertEquals(statusAlert.startsWith("Success"),true);
        javascriptConfirm.accept();
    }

    // step 5: Pay for Preserve Ticket
    @Test (dependsOnMethods = {"testConfirmTicketInfo"})
    public void testPayTicket() throws Exception {

        String itemOrderId = driver.findElement(By.id("flow_advanced_reserve_pay_orderId")).getAttribute("value");
        String itemPrice = driver.findElement(By.id("flow_advanced_reserve_pay_price")).getAttribute("value");
        String itemTripId = driver.findElement(By.id("flow_advanced_reserve_pay_tripId")).getAttribute("value");
        boolean bOrderId = !"".equals(itemOrderId);
        boolean bPrice = !"".equals(itemPrice);
        boolean bTripId = !"".equals(itemTripId);
        boolean bStatusPay = bOrderId && bPrice && bTripId;

        if(!bStatusPay)
            System.out.println("Confirming Ticket failed!");
        Assert.assertEquals(bStatusPay,true);

        driver.findElement(By.id("flow_advanced_reserve_pay_btn")).click();
        Thread.sleep(1000);

        String itemCollectOrderId = driver.findElement(By.id("flow_advanced_reserve_collect_order_id")).getAttribute("value");
        Assert.assertEquals(!"".equals(itemCollectOrderId),true);

        System.out.println("Success to pay and book ticket!");
    }

    // step 6: Ticket Collect
    @Test (dependsOnMethods = {"testPayTicket"})
    public void testTicketCollect() throws Exception {

        String itemCollectOrderId = driver.findElement(By.id("flow_advanced_reserve_collect_order_id")).getAttribute("value");
        boolean bCollectOrderId = !"".equals(itemCollectOrderId);
        if(!bCollectOrderId)
            System.out.println("Ticket payment failed!");
        Assert.assertEquals(bCollectOrderId,true);

        driver.findElement(By.id("flow_advanced_reserve_collect_button")).click();
        Thread.sleep(1000);

        // need to check
        String statusCollectOrderId = driver.findElement(By.id("flow_advanced_reserve_collect_order_status")).getText();
        if("".equals(statusCollectOrderId))
            System.out.println("Failed to Collect Ticket! Status is Null!");
        else if(statusCollectOrderId.startsWith("Success"))
            System.out.println("Success to Collect Ticket! Status:"+statusCollectOrderId);
        else
            System.out.println("Failed to Collect Ticket! Status is:"+statusCollectOrderId);
        Assert.assertEquals(statusCollectOrderId.startsWith("Success"),true);
    }

    // step 7: Enter Station
    @Test (dependsOnMethods = {"testTicketCollect"})
    public void testEnterStation() throws Exception{

        String itemEnterOrderId = driver.findElement(By.id("advanced_reserve_execute_order_id")).getAttribute("value");
        if("".equals(itemEnterOrderId))
            System.out.println("Enter Station,No Order Id,failed");
        Assert.assertEquals(!"".equals(itemEnterOrderId),true);

        driver.findElement(By.id("flow_advanced_reserve_order_button")).click();
        Thread.sleep(1000);

        String statusEnterStation = driver.findElement(By.id("flow_advanced_reserve_order_status")).getText();
        if("".equals(statusEnterStation))
            System.out.println("Failed to Enter Station! Status is Null!");
        else if(statusEnterStation.startsWith("Success"))
            System.out.println("Success to Enter Station! Status:"+statusEnterStation);
        else
            System.out.println("Failed to Enter Station! Status is:"+statusEnterStation);

        Assert.assertEquals(statusEnterStation.startsWith("Success"),true);
    }

    @AfterClass
    public void tearDown() throws Exception {
        driver.quit();
    }
}
