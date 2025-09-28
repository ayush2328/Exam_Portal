FROM tomcat:9.0-jre17

# Remove default apps
RUN rm -rf /usr/local/tomcat/webapps/*

# Copy WAR file as ROOT.war (deploys to root context)
COPY target/ExamBackend/ExamBackend.war /usr/local/tomcat/webapps/ROOT.war

# Simple port change (this syntax works reliably)
RUN sed -i 's/8080/10000/g' /usr/local/tomcat/conf/server.xml

EXPOSE 10000

CMD ["catalina.sh", "run"]