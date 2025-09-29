FROM tomcat:9.0-jre17

# Install unzip first
RUN apt-get update && apt-get install -y unzip

# Remove default apps
RUN rm -rf /usr/local/tomcat/webapps/ROOT*

# Copy and manually explode WAR file
COPY target/ExamBackend.war /usr/local/tomcat/webapps/
RUN cd /usr/local/tomcat/webapps/ && \
    unzip -q ExamBackend.war -d ROOT/ && \
    rm ExamBackend.war

# Use default port 8080
EXPOSE 8080

# Start Tomcat
CMD ["catalina.sh", "run"]