FROM tomcat:9.0-jre17
RUN rm -rf /usr/local/tomcat/webapps/ROOT*
COPY target/ExamBackend.war /usr/local/tomcat/webapps/
RUN cd /usr/local/tomcat/webapps/ && unzip -q ExamBackend.war -d ROOT/
EXPOSE 8080
CMD ["catalina.sh", "run"]