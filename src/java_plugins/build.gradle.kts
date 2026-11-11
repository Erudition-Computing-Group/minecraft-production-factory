plugins {
    java
    id("com.github.johnrengelman.shadow") version "8.1.1"
}

group = "com.particlefactory"
version = "1.0.0"

repositories {
    mavenCentral()
    maven("https://repo.papermc.io/repository/maven-public/")
    maven("https://jitpack.io")
}

dependencies {
    compileOnly("io.papermc.paper:paper-api:1.21.4-R0.1-SNAPSHOT")
    compileOnly("com.github.retrooper:packetevents-spigot:2.3.0")
    compileOnly("net.luckperms:api:5.4")
}

java {
    toolchain.languageVersion.set(JavaLanguageVersion.of(21))
}

tasks.shadowJar {
    archiveClassifier.set("")
    minimize()
}

tasks.build {
    dependsOn(tasks.shadowJar)
}
