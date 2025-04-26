package gateway;

import com.alibaba.csp.sentinel.adapter.gateway.common.rule.GatewayFlowRule;
import com.alibaba.csp.sentinel.adapter.gateway.common.rule.GatewayRuleManager;
import com.alibaba.csp.sentinel.adapter.gateway.sc.SentinelGatewayFilter;
import com.alibaba.csp.sentinel.adapter.gateway.sc.callback.BlockRequestHandler;
import com.alibaba.csp.sentinel.adapter.gateway.sc.callback.GatewayCallbackManager;
import com.alibaba.csp.sentinel.adapter.gateway.sc.exception.SentinelGatewayBlockExceptionHandler;
import com.alibaba.csp.sentinel.slots.block.RuleConstant;
import org.springframework.beans.factory.ObjectProvider;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerCodecConfigurer;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.server.ServerResponse;
import org.springframework.web.reactive.result.view.ViewResolver;

import javax.annotation.PostConstruct;
import java.util.*;

/**
 * 网关配置类
 *
 * <p>主要是<a href="https://sentinelguard.io/zh-cn/docs/api-gateway-flow-control.html">基于sentinel的网关限流策略配置</a></p>
 *
 * @author Akasaka Isami
 * @since 2022-06-30 15:13:58
 */

@Configuration
public class GatewayConfiguration {

    private final List<ViewResolver> viewResolvers;
    private final ServerCodecConfigurer serverCodecConfigurer;

    public GatewayConfiguration(ObjectProvider<List<ViewResolver>> viewResolversProvider,
                                ServerCodecConfigurer serverCodecConfigurer) {
        this.viewResolvers = viewResolversProvider.getIfAvailable(Collections::emptyList);
        this.serverCodecConfigurer = serverCodecConfigurer;
    }


    /**
     * 配置限流的异常处理器
     *
     * @return 限流的异常处理器
     */
    @Bean
    @Order(Ordered.HIGHEST_PRECEDENCE)
    public SentinelGatewayBlockExceptionHandler sentinelGatewayBlockExceptionHandler() {
        // Register the block exception handler for Spring Cloud Gateway.
        return new SentinelGatewayBlockExceptionHandler(viewResolvers, serverCodecConfigurer);
    }

    /**
     * 初始化一个限流的过滤器
     *
     * @return 限流过滤器
     */
    @Bean
    @Order(-1)
    public GlobalFilter sentinelGatewayFilter() {
        return new SentinelGatewayFilter();
    }

    /**
     * 配置初始化的限流参数
     */
    @PostConstruct
    public void doInit() {
        initGatewayRules();
//        initBlockHandlers();

        System.out.println("===== begin to do flow control");
        System.out.println("only 20 requests per second can pass");
    }

    /**
     * 注册函数用于实现自定义的逻辑处理被限流的请求
     *
     * <p>默认是返回错误信息： “Blocked by Sentinel: FlowException”。 这里自定义了异常处理，封装了自然语句。</p>
     */
    private void initBlockHandlers() {
        BlockRequestHandler blockRequestHandler = (serverWebExchange, throwable) -> {
            Map<Object, Object> map = new HashMap<>();
            map.put("code", 0);
            map.put("message", "接口被限流了");
            return ServerResponse.status(HttpStatus.OK).
                    contentType(MediaType.APPLICATION_JSON_UTF8).
                    body(BodyInserters.fromObject(map));
        };
        GatewayCallbackManager.setBlockHandler(blockRequestHandler);
    }


    /**
     * 初始化流量控制规则
     *
     * <p>Sentinal 的流量控制只能基于 route 或自定义 api 分组，这里的限流还是基于 application.yml 中定义的路由（即每个服务）采用 QPS 流量控制策略。
     * 当前是简单的对转发到 admin-basic-info-service 服务的流量做了QPS限制，每秒不超过20个请求。</p>
     */
    private void initGatewayRules() {
        Set<GatewayFlowRule> rules = new HashSet<>();

        // 对于转发到 admin-basic-info 的请求 set limit qps to 20
        // qps 超过 20 直接拒绝
        rules.add(new GatewayFlowRule("admin-basic-info") //资源名称，对应路由 id
                .setControlBehavior(RuleConstant.CONTROL_BEHAVIOR_DEFAULT)
                .setCount(20) // 限流qps阈值
                .setIntervalSec(1) // 统计时间窗口，单位是秒，默认是 1 秒
        );

        GatewayRuleManager.loadRules(rules);
    }
}
