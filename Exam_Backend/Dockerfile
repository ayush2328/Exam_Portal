FROM tomcat:9.0-jre17

# Remove default apps
RUN rm -rf /usr/local/tomcat/webapps/ROOT*

# Copy WAR file - Tomcat will auto-explode it
COPY target/ExamBackend.war /usr/local/tomcat/webapps/ROOT.war

# Use default port 8080
EXPOSE 8080

# Start Tomcat
CMD ["catalina.sh", "run"]