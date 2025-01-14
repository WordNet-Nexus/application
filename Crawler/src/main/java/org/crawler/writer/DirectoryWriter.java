package org.crawler.writer;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class DirectoryWriter implements Writer{
    private final String directoryPath;

    public DirectoryWriter(String directoryPath) {
        this.directoryPath = directoryPath;
        createDirectoryIfNotExists();
    }

    private void createDirectoryIfNotExists() {
        File directory = new File(directoryPath);
        if (!directory.exists()) {
            directory.mkdirs();
        }
    }

    @Override
    public void write(String fileName, String content) throws IOException {
        File file = new File(directoryPath, fileName);
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(file))) {
            writer.write(content);
        }
    }
}
