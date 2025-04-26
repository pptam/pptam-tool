package example;


import java.io.File;
import java.net.MalformedURLException;
import java.net.URL;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.FutureTask;

import org.openqa.selenium.By;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.remote.Augmenter;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.support.ui.ExpectedCondition;
import org.openqa.selenium.support.ui.WebDriverWait;

public class sample1 {
    
	public static void main(String[] args) throws Exception {
		
		List<FutureTask<Integer>> futureTasks = new ArrayList<FutureTask<Integer>>();
		ExecutorService executorService = Executors.newFixedThreadPool(10);
		long start = System.currentTimeMillis();
		Callable<Integer> callable = new Callable<Integer>() {
			@Override
			public Integer call() throws Exception {
				WebDriver driver = new RemoteWebDriver(
                        new URL("http://localhost:4444/wd/hub"), 
                        DesiredCapabilities.chrome());

				driver.get("http://172.20.0.1:16006/hello6?cal=5");
				driver.get("http://172.20.0.1:16006/hello6?cal=6");
				driver.get("http://172.20.0.1:16006/hello6?cal=10");
				driver.get("http://172.20.0.1:16006/hello6?cal=25");
				driver.get("http://172.20.0.1:16006/hello6?cal=30");
				driver.get("http://172.20.0.1:16006/hello6?cal=50");
				driver.get("http://172.20.0.1:16006/hello6?cal=60");
				driver.get("http://172.20.0.1:16006/hello6?cal=80");
				driver.get("http://172.20.0.1:16006/hello6?cal=81");
				driver.get("http://172.20.0.1:16006/hello6?cal=90");
				driver.get("http://172.20.0.1:16006/hello6?cal=91");
				driver.get("http://172.20.0.1:16006/hello6?cal=95");
				driver.get("http://172.20.0.1:16006/hello6?cal=96");
				driver.get("http://172.20.0.1:16006/hello6?cal=97");
				driver.get("http://172.20.0.1:16006/hello6?cal=98");
				driver.get("http://172.20.0.1:16006/hello6?cal=100");
				
				driver.get("http://172.20.0.1:16006/hello6?cal=150");
				driver.get("http://172.20.0.1:16006/hello6?cal=120");
				driver.get("http://172.20.0.1:16006/hello6?cal=1000");
				
				
				System.out.println("Page title is: " + driver.getTitle());
				driver.quit();
				
				return Integer.valueOf(1);
			}
		};
		
		for (int i = 0; i < 6; i++) {
			FutureTask<Integer> futureTask = new FutureTask<Integer>(callable);
			futureTasks.add(futureTask);
			executorService.submit(futureTask);
		}

		int count = 0;
		for (FutureTask<Integer> futureTask : futureTasks) {
			count += futureTask.get();
		}
		long end = System.currentTimeMillis();
		System.out.println("result:" + count);
		System.out.println("time:" + (end - start) + "ms");
		// 清理线程池
		executorService.shutdown();
    }
}