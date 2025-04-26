

package hello;

import reactor.core.publisher.Mono;

import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;

@Component
public class EchoHandler {

	public Mono<ServerResponse> echo(ServerRequest request) {
		return ServerResponse.ok().body(request.bodyToMono(String.class), String.class);
	}

}
