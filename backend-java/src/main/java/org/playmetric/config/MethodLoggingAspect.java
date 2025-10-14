package org.playmetric.config;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class MethodLoggingAspect {
    private static final Logger log = LoggerFactory.getLogger(MethodLoggingAspect.class);

    // Exclude filters from AOP proxying to avoid Tomcat startup errors
    @Pointcut("within(org.playmetric..*) && (execution(* *(..))) && !within(org.springframework.web.filter.OncePerRequestFilter+)")
    public void applicationPackagePointcut() {}

    @Around("applicationPackagePointcut()")
    public Object logAround(ProceedingJoinPoint joinPoint) throws Throwable {
        if (!log.isDebugEnabled()) {
            return joinPoint.proceed();
        }
        String signature = joinPoint.getSignature().toShortString();
        long start = System.currentTimeMillis();
        log.debug("ENTER {} args={}", signature, joinPoint.getArgs());
        try {
            Object result = joinPoint.proceed();
            long time = System.currentTimeMillis() - start;
            log.debug("EXIT {} timeMs={} result={}", signature, time, result);
            return result;
        } catch (Throwable t) {
            long time = System.currentTimeMillis() - start;
            log.error("EXCEPTION {} timeMs={} ex= {}", signature, time, t.toString());
            throw t;
        }
    }
}
