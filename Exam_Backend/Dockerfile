FROM tomcat:9.0-jre17

# Remove default apps
RUN rm -rf /usr/local/tomcat/webapps/*

# Copy WAR file
COPY target/ExamBackend.war /usr/local/tomcat/webapps/ExamBackend.war

# Use environment variable for port
ENV PORT=10000

# Properly change the port in server.xml
RUN sed -i.bak "s/port=\"8080\"/port=\"${PORT}\"/g" /usr/local/tomcat/conf/server.xml

EXPOSE 10000

CMD ["catalina.sh", "run"]