FROM eclipse-temurin:21-jdk

WORKDIR /app

# Install gradle
RUN apt-get update && apt-get install -y wget unzip && \
    wget -q https://services.gradle.org/distributions/gradle-8.10.2-bin.zip -O /tmp/gradle.zip && \
    unzip -q /tmp/gradle.zip -d /opt && \
    rm /tmp/gradle.zip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH="/opt/gradle-8.10.2/bin:${PATH}"

# Copy project
COPY src/java_plugins /app

# Default: build
CMD ["gradle", "shadowJar", "--no-daemon"]
