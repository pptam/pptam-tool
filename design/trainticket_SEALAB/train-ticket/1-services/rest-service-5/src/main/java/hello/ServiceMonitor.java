

package hello;

import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.After;
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.Aspect;

import org.springframework.stereotype.Component;

@Aspect
@Component
public class ServiceMonitor {

	@AfterReturning("execution(* hello..*Controller.*(..))")
	public void logServiceAccess(JoinPoint joinPoint) {
		System.out.println("AfterReturning: " + joinPoint);
	}

	@After("execution(* hello..*Controller.*(..))")
	public void logServiceAfter(JoinPoint joinPoint) {
		System.out.println("After: " + joinPoint.toLongString());
		System.out.println("After: " + joinPoint.toShortString());
		System.out.println("After: " + joinPoint.getArgs()[0].toString());
		System.out.println("After: " + joinPoint.getKind());
		System.out.println("After: " + joinPoint.getClass());
		System.out.println("After: " + joinPoint.getSignature());
		System.out.println("After: " + joinPoint.getSourceLocation());
		System.out.println("After: " + joinPoint.getStaticPart());
		System.out.println("After: " + joinPoint.getTarget());
	}

}
