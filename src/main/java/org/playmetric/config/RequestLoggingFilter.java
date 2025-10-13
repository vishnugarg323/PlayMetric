package org.playmetric.config;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
// Removed @Component; will register as a bean in a config class
import org.springframework.web.filter.OncePerRequestFilter;
import org.springframework.web.util.ContentCachingRequestWrapper;
import org.springframework.web.util.ContentCachingResponseWrapper;

import java.io.IOException;
import java.nio.charset.StandardCharsets;

public class RequestLoggingFilter extends OncePerRequestFilter {
    private static final Logger log = LoggerFactory.getLogger(RequestLoggingFilter.class);

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        var requestWrapper = new ContentCachingRequestWrapper(request);
        var responseWrapper = new ContentCachingResponseWrapper(response);
        long start = System.currentTimeMillis();
        try {
            filterChain.doFilter(requestWrapper, responseWrapper);
        } finally {
            long duration = System.currentTimeMillis() - start;
            logRequestResponse(requestWrapper, responseWrapper, duration);
            responseWrapper.copyBodyToResponse();
        }
    }

    private void logRequestResponse(ContentCachingRequestWrapper request, ContentCachingResponseWrapper response, long duration) {
        try {
            String method = request.getMethod();
            String uri = request.getRequestURI();
            String query = request.getQueryString();
            String remote = request.getRemoteAddr();
            int status = response.getStatus();

            String requestBody = "";
            byte[] req = request.getContentAsByteArray();
            if (req != null && req.length > 0) {
                requestBody = new String(req, StandardCharsets.UTF_8);
                if (requestBody.length() > 2000) requestBody = requestBody.substring(0, 2000) + "...";
            }

            String responseBody = "";
            byte[] resp = response.getContentAsByteArray();
            if (resp != null && resp.length > 0) {
                responseBody = new String(resp, StandardCharsets.UTF_8);
                if (responseBody.length() > 2000) responseBody = responseBody.substring(0, 2000) + "...";
            }

            log.info("{} {}{} from={} status={} timeMs={} reqBody={} respBody={}",
                    method,
                    uri,
                    query == null ? "" : "?" + query,
                    remote,
                    status,
                    duration,
                    requestBody,
                    responseBody);
        } catch (Exception ex) {
            log.warn("Failed to log request/response", ex);
        }
    }
}
