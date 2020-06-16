package pptam.driver;

import com.sun.faban.driver.*;
import com.sun.faban.driver.util.Random;
import com.sun.faban.driver.util.ContentSizeStats;

import javax.xml.xpath.XPathExpressionException;
import java.io.IOException;
import java.util.logging.Logger;
import java.util.HashMap;
import java.util.Map;

/**
 * Simple web driver example.
 */
@BenchmarkDefinition(name = "PPTAM-${TEST_NAME}", version = "0.2")
@BenchmarkDriver(name = "WebDriver", threadPerScale = 1)
// # Visitor: View Home -> View Catalogue -> View Details
// - [ home, getCatalogue, getCart, home, getCatalogue, getCart, catalogue,
// catalogueSize, tags, cataloguePage, getCart, getCustomer, showDetails,
// getItem, getCustomer, getCart, getRelated ]
// # Buyer: View Home -> Login -> View Catalogue -> View Details -> Add to Cart
// -> View Cart -> Create order
// - [ home, getCatalogue, getCart, login, home, getCatalogue, getCart, home,
// getCatalogue, getCart, catalogue, catalogueSize, tags, cataloguePage,
// getCart, getCustomer, showDetails, getItem, getCustomer, getCart, getRelated,
// addToCart, showDetails, getItem, getCustomer, getCart, getRelated, basket,
// getCart, getCard, getAddress, getCatalogue, getItem, getCart, getCustomer,
// getItem, createOrder, viewOrdersPage, getOrders, getCart, getCustomer,
// getItem ]
// # Orders visitor: View Home -> Login -> View orders
// - [ home, getCatalogue, getCart, login, home, getCatalogue, getCart,
// viewOrdersPage, getOrders, getCart, getCustomer, getItem ]
@FlatSequenceMix(mix = { 100 }, sequences = { @OperationSequence({ "home", "booking" }) }, deviation = 5)
// @NegativeExponential (
// cycleType = CycleType.THINKTIME,
// cycleDeviation = 5
// )
public class WebDriver {

    /** The driver context for this instance. */
    private DriverContext ctx;
    private HttpTransport http;
    private String home, login, booking, order_list, consign_list, advanced_search, ticket_collect, enter_station;
    Logger logger;
    Random random;

    /**
     * Constructs the web driver.
     * 
     * @throws XPathExpressionException An XPath error occurred
     */
    public WebDriver() throws XPathExpressionException {
        ctx = DriverContext.getContext();
        HttpTransport.setProvider("com.sun.faban.driver.transport.hc3.ApacheHC3Transport");
        http = HttpTransport.newInstance();
        logger = ctx.getLogger();
        random = ctx.getRandom();
        String host = ctx.getXPathValue("/webBenchmark${TEST_NAME}/serverConfig/host");
        String port = ctx.getXPathValue("/webBenchmark${TEST_NAME}/serverConfig/port");

        String basepath = "http://" + host + ":" + port;

        home = basepath + "/index.html";
        login = basepath + "/login";
        getCatalogue = basepath + "/catalogue?size=5";

    }

    /**
     * @throws IOException An I/O or network error occurred.
     */
    @BenchmarkOperation(name = "home", max90th = 20, timing = Timing.AUTO)
    @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
    public void doHome() throws IOException {
        logger.finest("Accessing " + home);
        http.fetchURL(home);
    }

}
